
import sys
import asyncio
import gc

from array import array

from asyncio import Event
from micropython import const

from lib.compat import Queue
from asyncio import ThreadSafeFlag

import lib.upydash as _

async def gc_coro():
    try:
        while True:
            gc.collect()
            await asyncio.sleep(5)
    except asyncio.CancelledError:
        raise
    except Exception as err:
        sys.print_exception(err)


async def start():
    try:
        gc_task = asyncio.create_task(gc_coro())
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

# main()
