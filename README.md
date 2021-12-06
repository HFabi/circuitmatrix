# ledmatrix
LED rgb pi bonnet for python 3.9

## Hardware setup
Follow the [adafruit tutorial](https://learn.adafruit.com/adafruit-rgb-matrix-bonnet-for-raspberry-pi/driving-matrices) to correctly connect the led panel and bonnet to your raspberry pie.

## Software setup

### Setup raspberry pie
- use an image without desktop, e.g. [Raspberry Pi OS Lite](https://www.raspberrypi.com/software/operating-systems/)
- add an empty file "ssh" on the sd containing the os image
- connect to pi via ssh


### Install necessary packages
```bash
# update sources and packages
sudo apt update
sudo apt upgrade

# for python 2
sudo apt install python2.7-dev python-pillow
sudo apt install python2.7-distutils

# for python 3 (3.9)
sudo apt install python3-venv python3-pip python3-dev python3-pillow
sudo apt install python3.9-distutils
```

### Use install-script to download rgb-matrix library
No error should occure
```bash
curl https://raw.githubusercontent.com/adafruit/Raspberry-Pi-Installer-Scripts/master/rgb-matrix.sh >rgb-matrix.sh
sudo bash rgb-matrix.sh
```

### Prepare python bindings build
There seems to be an issue with python 3.9 and cython. According to https://github.com/hzeller/rpi-rgb-led-matrix/issues/1298
there are two options to fix it:

#### Option 1 (the option I choose):
```bash
python3 -m pip install cython
cd path_to_repo/bindings/python/rgbmatrix/
python3 -m cython -2 --cplus *.pyx
```
#### Option 2:
```
rename tp_print to tp_vectorcall_offset in
/bindings/python/rgbmatrix/core.cpp
/bindings/python/rgbmatrix/graphics.cpp
```

### Build python bindings again
```
make build-python PYTHON=$(command -v python3)
sudo make install-python PYTHON=$(command -v python3)
```

### Clone this repeository
in any directory next to the rpi-rgb-led-matrix directory


## Helpful resources
- adafruit: https://learn.adafruit.com/adafruit-rgb-matrix-bonnet-for-raspberry-pi/driving-matrices
- led-matrix library: https://github.com/hzeller/rpi-rgb-led-matrix


## Bugs
- only working on system python, not working with pip -> but why?
- I need to pass false in image_painter but not in library?
- the system is locked to an older commit of the library?

