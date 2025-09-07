# TinyC6

<p align="center">
  <img src="https://github.com/stephanelsmith/micro-wspr/blob/master/docs/ports/tinyc6/3960737589.jpg?raw=true" alt="" width="600"/>
</p>

## :hammer: Building Micropython Firware for TinyC6
#### Install pre-reqs
```
apt install cmake python3-libusb1
```
### ESP-IDF v5.4
#### Clone the Espressif ESP-IDF repo
```
git clone --depth 1 --branch v5.4 https://github.com/espressif/esp-idf.git esp-idf-v5.4
cd esp-idf-v5.4
git submodule update --init --recursive
./install.sh
source export.sh
```
From here on, you will need to source ```export.sh``` to setup your environment.

#### Clone the Micropython repo
```
git clone git@github.com:micropython/micropython.git micropython
cd micropython
git submodule update --init --recursive
make -C mpy-cross
cd ports/esp32
```
From here, the commands assume the current working directory is ```micropython/ports/esp32```.

#### Add the board file from the micro-wspr folder into the micropython build folder
```
ln -sf ~/micro-wspr/upy/boards/SS_WSPR_TINYC6 boards/.
```

#### Build micropython port with C modules
```
make BOARD=SS_WSPR_TINYC6 USER_C_MODULES=~/micro-wspr/upy/c_modules/esp32.cmake
```


#### Flash the esp32 chip.
Before flashing the ESP32C6 needs to be in the bootloader.  This is done by holding the ```boot``` button and clicking ```reset```.  You can find the right comm port with ```py -m serial.tools.list_ports```.  You may need to ```py -m pip install pyserial``` first.
```
py -m esptool --chip esp32c6 --port COM23 write_flash -z 0 .\micropython\ports\esp32\build-SS_WSPR_TINYC6\firmware.bin
```


## :runner: Trying the TinyC6 Port
Fire up a terminal and connect to the device (use ```py -m serial.tools.list_ports``` to find the COM port)
```
py -m serial.tools.miniterm COM23
```

