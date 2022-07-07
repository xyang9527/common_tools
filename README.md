<!-- @created at 2022-07-07 -->

# Contents

- [Contents](#contents)
- [Install](#install)
- [Tools](#tools)

<!-- ========= ========= =========  ========= ========= ========= -->

# Install

```shell
# conda info --envs
conda create --name common_tools python=3.10.0 -y
conda activate common_tools
conda install pip -y
pip install -U pip

pip install gitpython
pip install numpy
pip install opencv-python
pip install pdf2image
pip install termcolor
```

# Tools

- [pdf2png](tools/pdf2png.py)

  ```shell
  conda activate common_tools
  python tools/pdf2png.py \
      --input_pdf_path data/latex_symbols.pdf \
      --output_png_path temp/latex_symbols.png
  ```

<!-- End of File -->
