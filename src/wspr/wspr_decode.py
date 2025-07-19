



class WSPR():

    def __init__(self, wsprstr    = b'', # aprs like wspr string, eg. b'KI5TOF>WSPR:=FN42:37'
                       src        = b'',
                       dst        = b'WSPR',
                       pos        = b'', # maiden head
                       pwr        = b'', # power level
                       verbose    = False,
                       ):
        self.verbose = verbose
        self.wsprstr = wsprstr


    def __repr__(self):
        return self.wsprstr.decode()
