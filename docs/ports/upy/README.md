# <img src="https://github.com/stephanelsmith/micro-aprs/blob/master/docs/ports/upy/micropython-icon.jpg?raw=true" alt="" width="25"> Micropython

Running micropython can be run directly from the command line, interchangeable with all python and pypy examples.  For micropython, tight loops have been optimized using [viper optimization](https://docs.micropython.org/en/latest/reference/speed_python.html#the-viper-code-emitter).  If you build the firmware, you can also benefit from [C level optimizations](https://docs.micropython.org/en/latest/develop/cmodules.html).

Try any of the examples below!

## :hammer: Building Micropython Firware (optional)

[The process is actually quite painless](https://github.com/micropython/micropython/tree/master/ports/unix).

#### Install pre-reqs
```
apt install build-essential git python3 pkg-config libffi-dev
```
#### Clone micropython
```
git clone git@github.com:micropython/micropython.git
cd micropython
git submodule update --init --recursive
make -C mpy-cross
cd ports/unix
```
#### Build micropython with C modules
```
make USER_C_MODULES=~/micro-aprs/upy/c_modules
```
#### If using bash, link the micropython executable into your home/bin folder.
```
mkdir ~/bin
ln -sf ~/micropython/ports/unix/build-standard/micropython ~/bin/.
```

