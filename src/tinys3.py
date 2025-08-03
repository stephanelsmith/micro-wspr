
import sys
import asyncio
import gc

from machine import Pin, PWM, Timer
from array import array

from asyncio import Event
from micropython import const

from lib.compat import Queue
from asyncio import ThreadSafeFlag

import lib.upydash as _


# pwm frequency
_FPWM = const(7_038_600)

# afsk sample frequency
_FOUT = const(11_025)

_AFSK_OUT_PIN = const(1)

async def gc_coro():
    try:
        while True:
            gc.collect()
            await asyncio.sleep(5)
    except asyncio.CancelledError:
        raise
    except Exception as err:
        sys.print_exception(err)

async def out_afsk(pwm,
                   fout = 11_025,
                   ):
    try:
        pwm.duty_u16(32768)
    except Exception as err:
        sys.print_exception(err)

async def start():

    try:
        pwm = PWM(Pin(_AFSK_OUT_PIN), freq=_FPWM, duty_u16=32768) # resolution = 26.2536 - 1.4427 log(fpwm)
        # gc_task = asyncio.create_task(gc_coro())
        await out_afsk(pwm = pwm,)
        await Event().wait()

    except Exception as err:
        sys.print_exception(err)
    finally:
        pwm.deinit()
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

