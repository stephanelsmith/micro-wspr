
import sys
import asyncio

from lib.compat import Queue

import lib.upydash as _
from lib.parse_args import mod_parse_args

from lib.utils import eprint # debug print to stderr, reserve stdout for pipe

#micropython/python compatibility
from lib.compat import IS_UPY
from lib.compat import print_exc
from lib.compat import get_stdin_streamreader

from wspr import WSPR
from wspr.encoder import GenWSPRCode

from afsk.func import create_afsk_tone_gen

try:
    from rich import print
except ImportError:
    pass

if not IS_UPY:
    import wave
    # from subprocess import check_output

async def read_wspr_from_pipe():
    try:
        reader = await get_stdin_streamreader()
        buf = bytearray(2048)
        idx = 0
        while True:
            try:
                buf[idx:idx+1] = await reader.readexactly(1)
            except EOFError:
                break #eof break
            if buf[idx] == 10: # \n
                return bytes(buf[:idx])
                idx = 0
            idx = (idx+1)%2048
        if idx:
            return bytes(buf[:idx])
    except asyncio.CancelledError:
        raise
    except Exception as err:
        print_exc(err)

async def output_audiosamples(codes,
                              out_file = '-', # - | null
                              Tsym     = 0,   # ms delay between each symbol
                              fs       = 22050,
                              foff     = 1500,
                              verbose  = False,
                              ):
    try:
        write = sys.stdout.buffer.write
        flush = sys.stdout.buffer.flush

        tsym = 8192/12000 # 8192/12000 symbol period is ~683ms
        fsym = 1/tsym     # symbol spacing is ~1.46Hz
        k = 0
        afsks = list(foff+i*fsym for i in range(4))
        tone_gen = create_afsk_tone_gen(fs     = fs,
                                        afsks  = afsks,
                                        signed = True,
                                        ampli  = 0x1ff,
                                        baud   = fsym,
                                        )
        
        # buffer 1 sec
        for i in range(fs):
            write(b'\x00\x00')

        # codes is byte array of codes 162 bits
        for i,b in enumerate(codes):
            for j,s in enumerate(tone_gen(b)):
                write(s.to_bytes(2, 'little', signed=True))
                k += 1
            flush()

        # buffer 1 sec
        for i in range(fs):
            write(b'\x00\x00')

    except asyncio.CancelledError:
        raise
    except Exception as err:
        print_exc(err)
        raise


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
            eprint('# bad wspr input string:{}\n{}'.format(wspr,err))
            return
        
        if verbose:
            eprint('===== WSPR ENCODE >>>>>',end=' ')
            eprint(wspr)
        async with GenWSPRCode(callsign = wspr.src, 
                               grid     = wspr.pos,
                               power    = wspr.pwr) as gen:
            bs = bytearray(s for s in gen)
            if verbose:
                for i,b in enumerate(bs):
                    eprint(b, end='\n' if (i+1)%18==0 else '  ' if (i+1)%6==0 else ' ')
            return bs

    except asyncio.CancelledError:
        raise
    except Exception as err:
        print_exc(err)


async def main():
    args = mod_parse_args(sys.argv)
    if args == None:
        return

    if args['args']['verbose']:
        eprint('# WSPR MOD')
        # eprint(args)
        eprint('# IN   {}'.format(args['in']['file']))
        eprint('# OUT  {}'.format(args['out']['file']))

    # WSPR queue, these items are queued in from stdin and out in wspr_encoder
    wspr_q = Queue()
    wsprcodes_q = Queue()

    tasks = []
    try:
        wspr  = await read_wspr_from_pipe()
        codes = await wspr_encoder(wspr = wspr,
                                   verbose = args['args']['verbose'],
                                   )
        if args['out']['file'] == '-':
            await output_audiosamples(codes    = codes,
                                      out_file = args['out']['file'],
                                      fs       = args['args']['rate'],
                                      foff     = args['args']['foff'],
                                      Tsym     = args['args']['Tsym'], 
                                      verbose  = args['args']['verbose'],
                                      )

    except Exception as err:
        print_exc(err)
    finally:
        for task in tasks:
            task.cancel()
        await asyncio.gather(*tasks, return_exceptions=True)
        sys.stdout.close()

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass

