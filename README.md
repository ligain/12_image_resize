
# Image Resizer  
  
Yet another simple tool to resize image. It can resize images of JPEG and PNG file formats.
Before using the tool it has to be installed python version=`3.5` and requirements from `requirements.txt` file.

You can specify both `--height` and `--width` or just `--scale` params to resize image.
## Simple run
```bash
$ python3.5 image_resize.py -i path/to/targe-image.jpg -o path/to/resized-image.jpeg --height 480 --width 640

$ python3.5 image_resize.py -i path/to/targe-image.jpg -o path/to/resized-image.jpeg --scale 2.5
```
To get more help just type in:
```bash
$ python3.5 image_resize.py -h
```
###
  
# Project Goals  
  
The code is written for educational purposes. Training course for web-developers - [DEVMAN.org](https://devman.org)