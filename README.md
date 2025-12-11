#  A lightweight python WSPR encoder

A python/micropython based library for encoding and modulating WSPR packets in AFSK audio.

The purpose of this library is to thread-the-needle of both enabling WSPR encoding and audio modulation from PC to microcontroller while maintaining portability and readability of python.  This library is optimized for embedded systems, especially [micropython supported targets and platforms ](https://github.com/micropython/micropython#supported-platforms--architectures) and small computers, not to mention Cpython and Pypy! 

In practice this means we:
* Avoid floating point and math libraries and dependencies in critical sections.  
	* :+1: Integer math only
	* :+1: NO external libraries (numpy/scipy/pandas).
* Special care for memory allocation
	* :+1: Pre-computing buffer/array sizes and modifying in place
	* :-1: Dynamically appending items to a list
* Single threaded, multitask friendly
	* :+1::+1: Asyncio

## :horse_racing: **Start here!**
### Build instructions
* [Micropython](docs/ports/upy/README.md) unix build instructions, and encode/decode examples via cli.
* [TinyS3](docs/ports/tinys3/README.md), ESP32S3 build isntructions on the TinyS3 (ESP32-S3).
* [TinyC6](docs/ports/tinyc6/README.md), ESP32C6 build isntructions on the TinyC6 (ESP32-C6).

### 🫰 Basic usage
From the ```micro-wspr/src``` folder, try
```
python wspr_mod.py -h
```
```
WSPR MOD
© Stéphane Smith (KI5TOF) 2025

wspr_mod.py parses input AX25 WSPR strings and outputs AFSK samples in signed 16 bit little endian format.

Usage:
wspr_mod.py [options] (-t outfile) (-t infile)
wspr_mod.py [options] (-t infile)
wspr_mod.py [options]
wspr_mod.py

OPTIONS:
-v, --verbose    verbose intermediate output to stderr
-r, --rate       22050 (default)
-foff            frequency offset, 1400 <= 1500 (default) <= 1600 Hz
-Tsym            Symbol period in ms.  default 0. Use 'wspr' for standard ~687ms period

-t INPUT TYPE OPTIONS:
infile       '-' (default)

-t OUTPUT TYPE OPTIONS:
outfile       '-' (default) | 'null' (no output)
```

### 📝 Encode AX25 APRS string in verbose mode
```-v``` verbose mode is designed to show the intermediate steps (on stderr).  For this example, we suppress output (setting stdout to null).
```
echo "KI5TOF>WSPR:=FN42:37" | python wspr_mod.py -v -t null -t -
```
```
# WSPR MOD
# IN   -
# OUT  null
===== WSPR ENCODE >>>>> KI5TOF>WSPR:=FN42:37
3 1 0 0 0 0  0 0 3 2 0 0  3 3 1 2 0 0
3 0 2 3 2 3  3 1 1 2 0 2  2 0 2 0 3 2
0 1 2 3 0 0  2 0 2 0 1 2  3 1 0 2 3 1
2 1 2 0 2 1  1 2 1 2 0 2  0 3 1 0 1 0
3 0 3 2 3 2  2 1 0 0 1 2  3 1 0 0 2 1
3 2 1 0 3 2  2 0 1 0 2 0  2 0 3 2 0 3
0 0 3 1 1 0  3 3 0 2 1 1  2 3 2 2 2 1
3 3 2 0 2 0  0 1 0 3 0 0  3 3 0 2 0 2
```


## :raised_hands: Acknowledgements
- [Micropython](https://github.com/micropython/micropython) project
- [WSPR protocol documentation by Andy Talbot (G4JNT)](docs/ack/wspr_coding_process.pdf)
- [WSPR 2.0 User’s Guide](docs/ack/WSPR_2.0_User.pdf) Very good WSPR Protocol dscription in Appendix.
- [WsprSharp](https://github.com/swharden/WsprSharp) a C# WSPR implmentation
    - [WSPR Code Generator](https://swharden.com/software/wspr-code-generator/) online code generator based on WsprSharp
- [FSKview](https://swharden.com/software/FSKview/wspr/) spectrogram for viewing frequency-shift keyed (FSK) signals in real time
- [genwspr.py](https://github.com/brainwagon/genwspr) Python 2 WSPR encoder by Mark VandeWettering K6HX.
	- [genwsprcode.py](https://github.com/PH0TRA/wspr) Converted genwspr to python3.
	- [Raspberry Pi version](https://blog.marxy.org/2024/09/python-code-to-generate-wspr-audio-tones.html)
		- [wsprgen.py](https://gist.github.com/peterbmarks/339e5ae83b5351151137679b8f527466)
- [wspr-cui](https://github.com/jj1bdx/wspr-cui) Wspr code

## License
MIT License


