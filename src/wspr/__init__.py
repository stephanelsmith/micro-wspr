

from lib.compat import const

_ORD_0 = const(48)
_ORD_9 = const(57)
_ORD_A = const(65)
_ORD_Z = const(90)
_ORD_a = const(97)
_ORD_z = const(122)

class WSPR():

    def __init__(self, wsprstr    = b'', # aprs like wspr string, eg. b'KI5TOF>WSPR:=FN42:37'
                       src        = b'',
                       dst        = b'WSPR',
                       pos        = b'xxxx', # maiden head
                       pwr        = b'yy', # power level
                       verbose    = False,
                       ):
        self.src = src
        self.dst = dst
        self.pos = pos
        self.pwr = pwr

        self.verbose = verbose

        if wsprstr:
            self.from_wsprstr(wsprstr = wsprstr)

    def from_wsprstr(self, wsprstr):
        # from a string like b'KI5TOF>WSPR:=FN42:37'

        if isinstance(wsprstr, str):
            wsprstr = wsprstr.encode()

        i = wsprstr.find(b'>')
        if not i:
            raise Exception('could not find source {}'.format(wsprstr))

        for j in range(i):
            o = wsprstr[j]
            if o >= _ORD_A and o <= _ORD_Z or\
               o >= _ORD_a and o <= _ORD_z:
                break
        self.src = wsprstr[:i]
        j = i + 1

        i = wsprstr.find(b':=',j)
        self.dst = wsprstr[j:i]
        j = i + 2

        i = wsprstr.find(b':',j)
        self.pos = wsprstr[j:i]
        j = i + 1
        self.pwr = wsprstr[j:]

    def __repr__(self):
        return '{}>{}:={}:{}'.format(self.src, self.dst, self.pos, self.pwr)

    def __rich__(self):
        return "[bold bright_green]{}[/bold bright_green]>[bright_yellow]{}:=[magenta]{}[/magenta]:[blue]{}[blue]".format(self.src.decode(), self.dst.decode(), self.pos.decode(), self.pwr.decode())


