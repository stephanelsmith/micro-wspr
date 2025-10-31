# genwspr
#
# A program which generates the tone sequence needed for a particular 
# beacon message.
#
##Very little error checking is done on this, so you better make sure
##that the callsign and gridsquare are of the appropriate form.
##
##Callsigns must be 2x3, 1x3, 2x1, or 1x2 for the purposes of this 
##code.
##
##Original code written by Mark VandeWettering K6HX https://github.com/brainwagon/genwspr

# converted to module for Python3 july 2017 by Marc Burgmeijer PH0TRA
# refactored and optimized july 2025 by Stephane Smith KI5TOF

import sys, string
import asyncio
from array import array

WSPR_SYMBOL_COUNT = 162

SYNCV = array('B',[1, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 1, 1, 0, 0, 0, 1, 0, 0, 1, 0, 1,
         1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0,
         1, 1, 0, 0, 1, 1, 0, 1, 0, 0, 0, 1, 1, 0, 1, 0, 0, 0, 0, 1, 1, 0, 1, 0,
         1, 0, 1, 0, 1, 0, 0, 1, 0, 0, 1, 0, 1, 1, 0, 0, 0, 1, 1, 0, 1, 0, 1, 0,
         0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 1, 1, 1, 0, 1, 1, 0, 0, 1, 1,
         0, 1, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 1, 1, 0, 0, 0, 0,
         0, 0, 0, 1, 1, 0, 1, 0, 1, 1, 0, 0, 0, 1, 1, 0, 0, 0])

# Precompute reverse index for interleaving
# self.ridx = list(filter(lambda x: x < 162, map(self.bitreverse, range(256))))
RIDX = array('H', [0, 128, 64, 32, 160, 96, 16, 144, 80, 48, 112, 8, 136, 72, 40, 104, 24, 152, 88, 56, 120, 4, 132, 68, 36, 100, 20, 148, 84, 52, 116, 12, 140, 76, 44, 108, 28, 156, 92, 60, 124, 2, 130, 66, 34, 98, 18, 146, 82, 50, 114, 10, 138, 74, 42, 106, 26, 154, 90, 58, 122, 6, 134, 70, 38, 102, 22, 150, 86, 54, 118, 14, 142, 78, 46, 110, 30, 158, 94, 62, 126, 1, 129, 65, 33, 161, 97, 17, 145, 81, 49, 113, 9, 137, 73, 41, 105, 25, 153, 89, 57, 121, 5, 133, 69, 37, 101, 21, 149, 85, 53, 117, 13, 141, 77, 45, 109, 29, 157, 93, 61, 125, 3, 131, 67, 35, 99, 19, 147, 83, 51, 115, 11, 139, 75, 43, 107, 27, 155, 91, 59, 123, 7, 135, 71, 39, 103, 23, 151, 87, 55, 119, 15, 143, 79, 47, 111, 31, 159, 95, 63, 127])


class GenWSPRCode:

    def __init__(self, callsign, 
                       power, 
                       grid   = None,
                       latlon = None):
        if isinstance(callsign, (bytes, bytearray)):
            self.callsign = callsign.decode()
        elif isinstance(callsign, str):
            self.callsign = callsign
        else:
            raise Exception('callsign should be str, byte, bytearray')

        if isinstance(grid, bytes) or isinstance(grid, bytearray):
            self.grid = grid.decode()
        elif isinstance(grid, str):
            self.grid = grid
        if isinstance(latlon, (list,tuple)):
            self.latlon = latlon

        self.power = power

        # Validate and encode inputs
        self.callsign_bin = self.encode_callsign(self.callsign)

        if self.grid:
            self.latlon = self.encode_grid(self.grid)
        self.latlon_bin = self.encode_latlon(*self.latlon)

        self.power_bin = self.encode_power(self.power)


    async def __aenter__(self):
        return self

    async def __aexit__(self, *args):
        pass

    # iterable of symbols of len 162
    def __iter__(self):
        message = self.callsign_bin + self.latlon_bin + self.power_bin + 31 * '0'
        encoded = self.encode(message)

        # Interleave
        msg = array('b', [0 for x in range(WSPR_SYMBOL_COUNT)])
        for i in range(WSPR_SYMBOL_COUNT):
            msg[RIDX[i]] = encoded[i]
        for i in range(WSPR_SYMBOL_COUNT):
            yield 2*msg[i]+SYNCV[i]
    def __len__(self):
        return WSPR_SYMBOL_COUNT

    @staticmethod
    def normalize_callsign(callsign):
        callsign = list(callsign)
        idx = next((i for i, ch in enumerate(callsign) if ch in string.digits), None)
        newcallsign = 6 * [" "]
        newcallsign[2 - idx:2 - idx + len(callsign)] = callsign
        return ''.join(newcallsign)

    @classmethod
    def encode_callsign(cls, callsign):
        callsign = callsign.upper()
        callsign = cls.normalize_callsign(callsign)
        lds = string.digits + string.ascii_uppercase + " "
        ld = string.digits + string.ascii_uppercase
        d = string.digits
        ls = string.ascii_uppercase + " "
        acc = lds.find(callsign[0])
        acc = acc * len(ld) + ld.find(callsign[1])
        acc = acc * len(d) + d.find(callsign[2])
        acc = acc * len(ls) + ls.find(callsign[3])
        acc = acc * len(ls) + ls.find(callsign[4])
        acc = acc * len(ls) + ls.find(callsign[5])
        return cls.tobin(acc, 28)

    @classmethod
    def encode_grid(cls, grid):
        grid = grid.upper()
        lat, lon = cls.grid2ll(grid)
        return lat, lon

    @classmethod
    def encode_latlon(cls, lat, lon):
        lon = int((180 - lon) / 2.0)
        lat = int(lat + 90)
        return cls.tobin(lon * 180 + lat, 15)

    @classmethod
    def encode_power(cls, power):
        try:
            return cls.tobin(int(power) + 64, 7)
        except:
            raise RuntimeError('Malformed power value', power)

    @classmethod
    def encode(cls, bitstr):
        f = []
        acc = 0
        for x in map(int, bitstr):
            b0, b1, acc = cls.convolver(x, acc)
            f.extend([b0, b1])
        return f

    @staticmethod
    def tobin(v, l):
        return f'{v:0{l}b}'

    @staticmethod
    def grid2ll(grid):
        p = (ord(grid[0]) - ord('A')) * 10 + (ord(grid[2]) - ord('0'))
        p = p * 24 + (12 if len(grid) == 4 else (ord(grid[4]) - ord('a')) + 0.5)
        lon = (p / 12) - 180.0

        p = (ord(grid[1]) - ord('A')) * 10 + (ord(grid[3]) - ord('0'))
        p = p * 24 + (12 if len(grid) == 4 else (ord(grid[5]) - ord('a')) + 0.5)
        lat = (p / 24) - 90.0
        return lat, lon

    @classmethod
    def convolver(cls, bit, acc):
        acc = ((acc << 1) & 0xFFFFFFFF) | bit
        return (cls.parity(acc & 0xf2d05351),
                cls.parity(acc & 0xe4613c47),
                acc)

    @staticmethod
    def parity(x):
        even = 0
        while x:
            even ^= 1
            x = x & (x - 1)
        return even

    @staticmethod
    def bitstring(x):
        # return ''.join(str((x >> i) & 1) for i in range(7, -1, -1))
        return ''.join(['01'[(x >> i) & 1] for i in range(7, -1, -1)])

    @classmethod
    def bitreverse(cls, x):
        bs = cls.bitstring(x)
        return int(bs[::-1], 2)

async def main():

    callsign = 'K1ABC'
    grid = 'FN42'
    latlon = (42.5, -71.0)
    power = '37'

    async with GenWSPRCode(callsign = callsign, 
                        grid     = grid,
                        power    = power) as gen:
        syms = [sym for sym in gen]
        print('BY GRID')
        print(syms)

    async with GenWSPRCode(callsign = callsign, 
                        latlon   = latlon,
                        power    = power) as gen:
        syms = [sym for sym in gen]
        print('BY LATLON')
        print(syms)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass


