
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

try:
    from rich import print
except ImportError:
    pass

if not IS_UPY:
    import wave
    # from subprocess import check_output

async def read_wspr_from_pipe(wspr_q, 
                              ):
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
                await wspr_q.put(bytes(buf[:idx]))
                idx = 0
                continue
            idx = (idx+1)%2048
        if idx:
            await wspr_q.put(bytes(buf[:idx]))
    except asyncio.CancelledError:
        raise
    except Exception as err:
        print_exc(err)

async def outputter(code_q,
                    out_file = '-', # - | null
                    Tsym     = 0,   # ms delay between each symbol
                    verbose  = False,
                    ):
    write = sys.stdout.buffer.write
    flush = sys.stdout.buffer.flush
    try:
        while True:
            b = await code_q.get()
            for i,s in enumerate(b):
                if verbose:
                    eprint(s, end='\n' if (i+1)%18==0 else '  ' if (i+1)%6==0 else ' ')
                write(s.to_bytes(2, 'little', signed=False))
                flush()
                await asyncio.sleep(Tsym/1000)
            code_q.task_done()
    except asyncio.CancelledError:
        raise
    except Exception as err:
        print_exc(err)


async def wspr_encoder(wspr_q,
                       code_q,
                       verbose = False,
                       ):
    try:
        while True:
            # get wspr from input
            wsprstr = await wspr_q.get()

            try:
                wspr = WSPR(wsprstr  = wsprstr,
                            verbose  = True,
                            )

            except asyncio.CancelledError:
                raise
            except Exception as err:
                eprint('# bad wspr input string:{}\n{}'.format(wsprstr,err))
                continue
           
            eprint('===== WSPR ENCODE >>>>>',end=' ')
            eprint(wspr)
            async with GenWSPRCode(callsign = wspr.src, 
                                   grid     = wspr.pos,
                                   power    = wspr.pwr) as gen:
                b = bytearray(s for s in gen)
                await code_q.put(b)

            # wait until queues are done
            await code_q.join()

            wspr_q.task_done()

    except asyncio.CancelledError:
        raise
    except Exception as err:
        print_exc(err)


async def main():
    args = mod_parse_args(sys.argv)
    if args == None:
        return

    eprint('# WSPR MOD')
    eprint(args)
    eprint('# IN   {}'.format(args['in']['file']))
    eprint('# OUT  {}'.format(args['out']['file']))

    # WSPR queue, these items are queued in from stdin and out in wspr_encoder
    wspr_q = Queue()
    code_q = Queue()

    tasks = []
    try:
        tasks.append(asyncio.create_task(outputter(code_q,
                                                   out_file = args['out']['file'],
                                                   Tsym     = args['args']['Tsym'], 
                                                   verbose  = args['args']['verbose'],
                                                   )))
        # wspr_encoder, convert WSPR messages into AFSK samples
        tasks.append(asyncio.create_task(wspr_encoder(wspr_q, 
                                                      code_q,
                                                      verbose = args['args']['verbose'],
                                                      )))

        # read all items from pipe, returns EOF
        await read_wspr_from_pipe(wspr_q)

        # wait until queues are done
        await wspr_q.join()

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

