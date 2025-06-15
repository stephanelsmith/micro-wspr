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

## :mortar_board: Tutorials

## :horse_racing: **Start here!**

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

## License
MIT License


