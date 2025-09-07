
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

async def pwm_test():
    duty = 32768
    freq = _FPWM
    sreader = asyncio.StreamReader(sys.stdin)
    pwm = PWM(Pin(_AFSK_OUT_PIN), freq=freq, duty_u16=duty) # resolution = 26.2536 - 1.4427 log(fpwm)
    try:
        while True:
            print('DUTY:{} FREQ:{}'.format(duty, freq))
            pwm.freq(freq)
            pwm.duty_u16(duty)
            cin = await sreader.read(1)
            if cin == 'q':
                duty -= 100
            elif cin == 'w':
                duty -= 1
            elif cin == 'e':
                duty += 1
            elif cin == 'r':
                duty += 100

            if cin == 'a':
                freq -= 100
            elif cin == 's':
                freq -= 1
            elif cin == 'd':
                freq += 1
            elif cin == 'f':
                freq += 100
    except Exception as err:
        sys.print_exception(err)
    finally:
        pwm.deinit()

async def start():

    try:
        # gc_task = asyncio.create_task(gc_coro())
        await pwm_test()
        await Event().wait()

    except Exception as err:
        sys.print_exception(err)
    finally:
        # pwm.deinit()
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

