

from lib.compat import const

_ORD_0 = const(48)
_ORD_9 = const(57)
_ORD_A = const(65)
_ORD_Z = const(90)
_ORD_a = const(97)
_ORD_z = const(122)

class WSPR():

    def __init__(self, wspraprs    = b'', # aprs like wspr string, eg. b'KI5TOF>WSPR:=FN42:37'
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

        if wspraprs:
            self.from_wspraprs(wspraprs = wspraprs)

    def from_wspraprs(self, wspraprs):
        # from a string like b'KI5TOF>WSPR:=FN42:37'

        if isinstance(wspraprs, str):
            wspraprs = wspraprs.encode()

        i = wspraprs.find(b'>')
        if not i:
            raise Exception('could not find source {}'.format(wspraprs))

        for j in range(i):
            o = wspraprs[j]
            if o >= _ORD_A and o <= _ORD_Z or\
               o >= _ORD_a and o <= _ORD_z:
                break
        self.src = wspraprs[:i]
        j = i + 1

        i = wspraprs.find(b':=',j)
        self.dst = wspraprs[j:i]
        j = i + 2

        i = wspraprs.find(b':',j)
        self.pos = wspraprs[j:i]
        j = i + 1
        self.pwr = wspraprs[j:]

    def __repr__(self):
        return '{} {} {}'.format(self.src, self.pos, self.pwr)

    def __rich__(self):
        return "[bold bright_green]{}[/bold bright_green] [magenta]{}[/magenta] [blue]{}[blue]".format(self.src.decode(), self.pos.decode(), self.pwr.decode())


