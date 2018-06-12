# Setup the dependencies

~~~
pip3 install opencv-python
pip3 install tensorflow
pip3 install keras
pip3 install pyclipper
pip3 install matplotlib
pip3 install sklearn
sudo apt-get install libatlas-base-dev libjasper-dev
sudo apt-get install libqtgui4
sudo apt-get install libhdf5-dev
~~~


# Error: ImportError: cairo backend requires that cairocffi or pycairo is installed

Try this: install libffi6 and libffi-dev using apt:
~~~
sudo apt install libffi-dev libffi6
~~~
Rerun pip install
~~~
pip3 install cairocffi
~~~


