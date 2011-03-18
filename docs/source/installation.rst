============
Installation
============

Pycha needs PyCairo to works since it uses the Cairo graphics library. If you
use Linux you will probably already have it installed so you don't have to do
anything. If you use Windows these are the recommended steps for installing
PyCairo:

1. Grab the latest PyCairo Windows installer from
   http://ftp.gnome.org/pub/GNOME/binaries/win32/pycairo/ You need to use the
   one that matches your Python version so take the one ending in -py2.4.exe
   for Python 2.4 or the one ending in -py2.5.exe for Python 2.5
2. Install it in your Python environment (just follow the installation
   program instructions)
3. Put the Cairo dlls inside the pycairo directory inside your site-packages
   directory or anywhere in your path. You can find the dlls at
   http://www.gimp.org/%7Etml/gimp/win32/downloads.html Go there and download
   the following packages:

   1. cairo.zip. You just need the libcairo-2.dll file inside that zip
   2. libpng.zip. You just need the libpng13.dll file inside that zip
   3. zlib.zip. You just need the zlib1.dll file inside that zip

Pycha is distributed as a Python Egg so is quite easy to install. You just need
to type the following command::

  easy_install pycha

And Easy Install will go to the Cheeseshop and grab the last pycha for you. If
will also install it for you at no extra cost :-)


Alternate method: buildout
--------------------------

You can use ``buildout`` to compile and build pycha dependencies automatically. To do so just type a couple of commands::

  python bootstrap.py --distribute
  bin/buildout

At the end of the process you will have a python interpreter at ``bin/py``
with pycha in its ``PYTHONPATH`` ready to be imported.
