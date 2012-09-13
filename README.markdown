# Installation #

This project will use the [Wand](http://dahlia.kr/wand/) library for python, which provides a python interface to the MagickWand library.

1. Download and install the x86 (32-bit) version of [python 2.7](http://www.python.org/download/).
2. Add the python installation directory (e.g. C:\Python27) and the Scripts subdirectory (e.g. C:\Python27\Scripts) to your $PATH environmental variable.
3. Install ImageMagick.
	- Windows: download and install [the binary](http://www.imagemagick.org/download/binaries/ImageMagick-6.7.9-5-Q16-windows-dll.exe).
	- Mac: Either use Homebrew or MacPorts to install ImageMagick.
		* Homebrew: `$ brew install imagemagick`
		* MacPorts: `$ sudo port install imagemagick`
4. Install easy_install.
	- Windows: download and install the [setuptools binary](http://pypi.python.org/packages/2.7/s/setuptools/setuptools-0.6c11.win32-py2.7.exe#md5=57e1e64f6b7c7f1d2eddfc9746bbaf20).
	- Mac: see [this guide](http://pypi.python.org/pypi/setuptools#files).
5. Add the default location for installing python scripts (Windows: C:\Python27\Scripts\) to your $PATH environmental variable.
6. Open up a terminal/dos prompt and do `$ easy_install Wand` to install Wand.

The Wand library should now be installed, and you should be able to run the program main.py with `$ python main.py`.
