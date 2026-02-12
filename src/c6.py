
import sys
import asyncio
import gc

from array import array

from asyncio import Event
from micropython import const

from lib.compat import Queue
from asyncio import ThreadSafeFlag

import lib.upydash as _

from wspr import WSPR
from wspr.encoder import GenWSPRCode

async def gc_coro():
    try:
        while True:
            gc.collect()
            await asyncio.sleep(5)
    except asyncio.CancelledError:
        raise
    except Exception as err:
        sys.print_exception(err)

async def wspr_encoder(wspr,
                       verbose = False,
                       ):
    try:
        # get wspr from input
        src,pos,pwr = wspr.split()

        try:
            wspr = WSPR(src      = src,
                        pos      = pos,
                        pwr      = pwr,
                        verbose  = True,
                        )

        except asyncio.CancelledError:
            raise
        except Exception as err:
            print('# bad wspr input string:{}\n{}'.format(wspr,err))
            return
        
        if verbose:
            print('===== WSPR ENCODE >>>>>',end=' ')
            print(wspr)
        async with GenWSPRCode(callsign = wspr.src, 
                               grid     = wspr.pos,
                               power    = wspr.pwr) as gen:
            bs = bytearray(s for s in gen)
            if verbose:
                for i,b in enumerate(bs):
                    print(b, end='\n' if (i+1)%18==0 else '  ' if (i+1)%6==0 else ' ')
            return bs

    except asyncio.CancelledError:
        raise
    except Exception as err:
        print_exc(err)


async def start():
    try:
        gc_task = asyncio.create_task(gc_coro())
        wspr = 'KI5TOF FN42 37'
        codes = await wspr_encoder(wspr    = wspr,
                                   verbose = True,
                                   )
    except Exception as err:
        sys.print_exception(err)
    finally:
        gc_task.cancel()


def main():
    try:
        asyncio.run(start())
    except KeyboardInterrupt:
        pass
    except Exception as err:
        sys.print_exception(err)
    finally:
        asyncio.new_event_loop()  # Clear retained state

main()
