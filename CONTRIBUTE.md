# Wanna help ?

## development environnement

Some day there may be a packaging tool configuration to handle dependencies and deployment, in the meantime you may want to 
1. fork this repository
1. clone your fork locally
1. update your python install
```
pip3 install --upgrade pip
pip3 install jupyter kivy kivymd kivy_garden matplotlib seaborn 
```
4. run the notebooks with
```
cd notebooks
jupyter notebook
```
5. run the various other scripts (usually) from command line ``python3 ./script.py``, check the
various README for more infos.


## UI and graphics

UI discussions happen at [balsamiq](https://balsamiq.cloud/szax2i8/pfszbl1), [🗪 give us a shout](https://github.com/jwnigel/permaculture/issues/new/choose) to explain how you want to join and get access.

Graphics assets are more than welcome, preferably in opensource format (Inkscape's SVG, Gimp's rasterized).

And if you wanna share some great music or your own design for the world to get some inspiration you're welcome too.

## install troubleshoot

various errors may happen depending on your development environment. Maybe someday we'll fix them with a proper package management system (you're welcome to help). In the meantime there as the few trouble we met, and ways to fix them:


### Some .kv file not found Error on running a script that needs kivymd
    FileNotFoundError: [Errno 2] No such file or directory: python3.8/site-packages/kivymd/uix/label/label.kv

possible fix : update your local version of kivymd with the command:

    pip install https://github.com/kivymd/KivyMD/archive/refs/tags/1.1.0.zip

### some AssertionError on running Jupyter Notebook
Seems like readthedocs is specifically requesting an incompatible version of pygments [> source](https://github.com/jupyterlab/jupyterlab_pygments/issues/5).

possible fix: upgrade your local Pygments library:

    pip3 install --upgrade Pygments