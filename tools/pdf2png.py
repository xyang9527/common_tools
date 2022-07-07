# -*- coding=utf-8 -*-

import sys
import os
import os.path as osp
lib_dir = osp.dirname(osp.dirname(osp.abspath(__file__)))
sys.path.append(lib_dir)

import argparse
import logging
import numpy as np
import subprocess
import time

import cv2
import pdf2image

from common.setup_log import setup_log, pcolor, print0, get_basename


def parse_args():
    parser = argparse.ArgumentParser(description='common_tools convert to single png file')
    parser.add_argument('--input_pdf_path', required=True, type=str, help='path of input pdf file')
    parser.add_argument('--output_png_path', required=True, type=str, help='path of output png file')
    args = parser.parse_args()
    return args


def highlight(string):
    print0(pcolor(f'{string}', 'magenta'))


def main(args):
    input_pdf = args.input_pdf_path
    output_png = args.output_png_path

    temp_save_dir = osp.join(osp.dirname(output_png), f'subfigs_{get_basename(output_png)}')
    if not osp.exists(temp_save_dir):
        os.makedirs(temp_save_dir)

    highlight(f'input_pdf_path:  {input_pdf}')
    highlight(f'output_png_path: {output_png}')
    highlight(f'temp_save_dir:   {temp_save_dir}')

    # pdf to png list
    # ref: https://pdf2image.readthedocs.io/en/latest/reference.html
    pages = pdf2image.convert_from_path(input_pdf, dpi=200)
    str_ext = '.png'
    for idx, page in enumerate(pages):
        page_name = f'{idx:04d}{str_ext}'
        page.save(f'{osp.join(temp_save_dir, page_name)}', 'PNG')

    # check size
    is_first_frame = True
    prev_shape = None
    sub_png_list = []
    for item in sorted(os.listdir(temp_save_dir)):
        if not item.endswith(str_ext):
            continue
        sub_png = cv2.imread(osp.join(temp_save_dir, item))
        sub_png_list.append(sub_png)
        if is_first_frame:
            prev_shape = sub_png.shape
            is_first_frame = False
            continue
        else:
            if prev_shape != sub_png.shape:
                raise ValueError

    highlight(f'shape:           {prev_shape}')

    # merge image
    num = len(sub_png_list)
    assert num > 0
    canvas = np.zeros((prev_shape[0]*num, prev_shape[1], prev_shape[2]), dtype=sub_png_list[0].dtype)
    for i in range(num):
        row_beg = i  * prev_shape[0]
        row_end = (i+1) * prev_shape[0]
        canvas[row_beg:row_end, ...] = sub_png_list[i]

    cv2.imwrite(output_png, canvas)
    path_cwd = os.getcwd()
    os.chdir(osp.dirname(output_png))
    subprocess.call(['rm', '-rf', f'{osp.basename(temp_save_dir)}'])
    os.chdir(path_cwd)


if __name__ == '__main__':
    setup_log(__file__)
    t_beg = time.time()

    args = parse_args()
    main(args)

    t_end = time.time()
    logging.warning(f'{osp.basename(__file__)} elapsed {t_end - t_beg:.3f} seconds')
    print0(pcolor(f'{osp.basename(__file__)} elapsed {t_end - t_beg:.3f} seconds', 'yellow'))

'''
python tools/pdf2png.py \
    --input_pdf_path data/latex_symbols.pdf \
    --output_png_path temp/latex_symbols.png
'''

# <!-- End of File -->
