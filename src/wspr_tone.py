
import sys
import asyncio

from lib.compat import Queue

import lib.upydash as _
from lib.parse_args import tone_parse_args

from lib.utils import eprint # debug print to stderr, reserve stdout for pipe

from lib.compat import IS_UPY
from lib.compat import print_exc
from lib.compat import get_stdin_streamreader


async def read_wspr_codes_from_pipe(codes_q, 
                                    verbose = False
                                    ):
    try:
        reader = await get_stdin_streamreader()
        while True:
            try:
                b = await reader.readexactly(2)
                v = int.from_bytes(b, 'little', signed=False)
                await codes_q.put(v)
                # eprint(v,end=' ')
            except EOFError:
                break #eof break
    except asyncio.CancelledError:
        raise
    except Exception as err:
        print_exc(err)

async def wspr_code_to_afsk(codes_q,
                            rate,
                            foff,
                            verbose = False,
                            ):
    try:
        while True:
            c = await codes_q.get()
            eprint(c)
            codes_q.task_done()
    except asyncio.CancelledError:
        raise
    except Exception as err:
        print_exc(err)

async def main():
    args = tone_parse_args(sys.argv)
    if args == None:
        return

    eprint('# WSPR TONE')
    # eprint(args)
    eprint('# RATE {}Hz'.format(args['args']['rate']))
    eprint('# FOFF {}Hz'.format(args['args']['foff']))
    eprint('# IN   {}'.format(args['in']['file']))
    eprint('# OUT  {}'.format(args['out']['file']))

    codes_q = Queue()

    tasks = []
    try:
        tasks.append(asyncio.create_task(wspr_code_to_afsk(codes_q = codes_q,
                                                           rate    = args['args']['rate'],
                                                           foff    = args['args']['foff'],
                                                           verbose = args['args']['verbose'],
                                                           )))

        # read all items from pipe, returns EOF
        await read_wspr_codes_from_pipe(codes_q,
                                        verbose  = args['args']['verbose'],
                                        )

        # wait until queues are done
        await codes_q.join()

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

