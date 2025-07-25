
import sys
import asyncio
import struct

from lib.compat import Queue

import lib.upydash as _
from lib.parse_args import mod_parse_args
from lib.utils import pretty_binary

from lib.utils import eprint # debug print to stderr, reserve stdout for pipe

#micropython/python compatibility
from lib.compat import IS_UPY
from lib.compat import print_exc
from lib.compat import get_stdin_streamreader

from wspr.wspr_decode import WSPR

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

async def afsk_mod(wspr_q,
                   afsk_q,
                   rate    = 22050,
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
            
            print(wspr)

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
    # eprint(args)
    eprint('# RATE {}'.format(args['args']['rate']))
    eprint('# IN   {}'.format(args['in']['file']))
    eprint('# OUT  {}'.format(args['out']['file']))

    # WSPR queue, these items are queued in from stdin and out in afsk_mod
    wspr_q = Queue()

    # AFSK queue, the samples, each item is a tuple: (array['i'], size), queued in from afsk_mod and out in afsk_out
    afsk_q = Queue() # afsk output queue

    # print("Hello, [bold magenta]World[/bold magenta]!")

    tasks = []
    try:

        # afsk_mod, convert WSPR messages into AFSK samples
        tasks.append(asyncio.create_task(afsk_mod(wspr_q, 
                                                  afsk_q, 
                                                  rate    = args['args']['rate'],
                                                  verbose = args['args']['verbose'],
                                                  )))


        # read all items from pipe, returns EOF
        await read_wspr_from_pipe(wspr_q)

        # wait until queues are done
        await wspr_q.join()
        # await afsk_q.join()

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

