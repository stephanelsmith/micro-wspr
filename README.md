#  A lightweight python WSPR encoder

A python/micropython based library for encoding and modulating WSPR packets in AFSK audio.

The purpose of this library is to enabe WSPR encoding and audio modulation from PC to microcontroller while maintaining portability and readability of python.  This library is optimized for embedded systems, especially [micropython supported targets and platforms ](https://github.com/micropython/micropython#supported-platforms--architectures) and small computers, not to mention Cpython and Pypy! 

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
#### 📝 Generate WSPR codes only
```
echo "KI5TOF FN42 37" | python wspr_mod.py -v -t null -t -
```
```
# WSPR MOD
# IN   -
# OUT  null
===== WSPR ENCODE >>>>> KI5TOF FN42 37
3 1 0 0 0 0  0 0 3 2 0 0  3 3 1 2 0 0
3 0 2 3 2 3  3 1 1 2 0 2  2 0 2 0 3 2
0 1 2 3 0 0  2 0 2 0 1 2  3 1 0 2 3 1
2 1 2 0 2 1  1 2 1 2 0 2  0 3 1 0 1 0
3 0 3 2 3 2  2 1 0 0 1 2  3 1 0 0 2 1
3 2 1 0 3 2  2 0 1 0 2 0  2 0 3 2 0 3
0 0 3 1 1 0  3 3 0 2 1 1  2 3 2 2 2 1
3 3 2 0 2 0  0 1 0 3 0 0  3 3 0 2 0 2
0 0 2 3 3 0  3 2 1 1 2 0  2 3 3 2 0 0
```

#### 📝 Generate WSPR wave file for wsprd decode
[Thank you to wspr-cui](https://github.com/jj1bdx/wspr-cui/tree/main) for documenting wsprd requires the wav file to have the following properties.
* WAV header (first 22 bytes) are ignored
* Format: fixed to S16\_LE, 12000Hz, monaural (1 channel)
* Length: 114 seconds (see `readwavfile()` in wsprd.c) 
```
echo "KI5TOF FN42 37" | python wspr_mod.py -r 12000 | sox -t raw -b 16 -e signed-integer -c 1 -v 1.0 -r 12000 - -t wav test.wav
wsprd test.wav
```
```
test   9  0.0   0.001498  0  KI5TOF FN42 37
test  40 -0.0   0.001502  0  KI5TOF FN42 37
test -21 -0.4   0.001572  0  KI5TOF FN42 37
<DecodeFinished>
```


#### 📝 Generate WSPR wave file for transmission
Unlike the `wsprd` version, we'll generate a higher quality and more typical wave files sampled at 22050.  This file will *not* properly be decoded by wsprd!
```
echo "KI5TOF FN42 37" | python wspr_mod.py -r 22050 | sox -t raw -b 16 -e signed-integer -c 1 -v 1.0 -r 22050 - -t wav test.wav
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


