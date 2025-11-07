

from micropython import const

# Internal constants:
_SI5351_ADDRESS = const(0x60)  # Assumes ADDR pin = low
_SI5351_READBIT = const(0x01)
_SI5351_CRYSTAL_FREQUENCY = 25000000.0  # Fixed 25mhz crystal on board.
_REG_0_DEVICE_STATUS = const(0)
_REG_1_INTERRUPT_STATUS_STICKY = const(1)
_REG_2_INTERRUPT_STATUS_MASK = const(2)
_REG_3_OUTPUT_ENABLE_CONTROL = const(3)
_REG_9_OEB_PIN_ENABLE_CONTROL = const(9)
_REG_15_PLL_INPUT_SOURCE = const(15)
_REG_16_CLK0_CONTROL = const(16)
_REG_17_CLK1_CONTROL = const(17)
_REG_18_CLK2_CONTROL = const(18)
_REG_19_CLK3_CONTROL = const(19)
_REG_20_CLK4_CONTROL = const(20)
_REG_21_CLK5_CONTROL = const(21)
_REG_22_CLK6_CONTROL = const(22)
_REG_23_CLK7_CONTROL = const(23)
_REG_24_CLK3_0_DISABLE_STATE = const(24)
_REG_25_CLK7_4_DISABLE_STATE = const(25)
_REG_092_CLOCK_6_7_OUTPUT_DIVIDER = const(92)
_REG_165_CLK0_INITIAL_PHASE_OFFSET = const(165)
_REG_166_CLK1_INITIAL_PHASE_OFFSET = const(166)
_REG_167_CLK2_INITIAL_PHASE_OFFSET = const(167)
_REG_168_CLK3_INITIAL_PHASE_OFFSET = const(168)
_REG_169_CLK4_INITIAL_PHASE_OFFSET = const(169)
_REG_170_CLK5_INITIAL_PHASE_OFFSET = const(170)
_REG_177_PLL_RESET = const(177)
_REG_183_CRYSTAL_INTERNAL_LOAD_CAPACITANCE = const(183)

_PLL_A = const(26)
_PLL_B = const(34)
_SYNTH_0 = const(42)
_SYNTH_1 = const(50)
_SYNTH_2 = const(58)


def init_si(i2c):
    # init xtal load
    i2c.writeto_mem(_SI5351_ADDRESS, _REG_183_CRYSTAL_INTERNAL_LOAD_CAPACITANCE, b'\xd2')

    i2c.writeto_mem(_SI5351_ADDRESS, _REG_3_OUTPUT_ENABLE_CONTROL, b'\x00') # enable all outputs



def init_pll(i2c, 
             pll = b'a',
             a = 30, b = 0, c = 1,
             ):
    # Set VCOs of PLLA and PLLB to 900 MHz 
    # a = 36;           # Division factor 900/25 MHz 
    # b = 0;            # Numerator, sets b/c=0 
    # c = 1;            
    if a < 15 or a > 90:
        raise Exception('multiplier 15-90')
    
    # Formula for splitting up the numbers to register data, see AN619 
    p1 = 128 * a +  (128 * b // c) - 512; 
    p2 = 128 * b - c * (128 * b // c); 
    p3  = c; 

    # Write data to registers PLLA and PLLB so that both VCOs are set to 900MHz intermal freq 
    buf = bytearray(8)
    buf[0] = (p3 & 0x0000FF00) >> 8
    buf[1] = p3 & 0x000000FF
    buf[2] = (p1 & 0x00030000) >> 16
    buf[3] = (p1 & 0x0000FF00) >> 8
    buf[4] = p1 & 0x000000FF
    buf[5] = ((p3 & 0x000F0000) >> 12) | ((p2 & 0x000F0000) >> 16)
    buf[6] = (p2 & 0x0000FF00) >> 8
    buf[7] = p2 & 0x000000FF

    rpll = None
    if pll == b'a':
        rpll = _PLL_A
    elif pll == b'b':
        rpll = _PLL_B
    if rpll:
        i2c.writeto_mem(_SI5351_ADDRESS, rpll, buf);
        i2c.writeto_mem(_SI5351_ADDRESS, _REG_177_PLL_RESET, b'\xa0')


def init_clk(i2c, 
             clk = 0,
             pll = b'a',
             a   = 30, b = 0, c = 1,
             ):
    # Valid Multisynth divider ratios are 4, 6, 8, and any fractional value between 8 + 1/1,048,575 and 2048. This
    # means that if any output is greater than 112.5 MHz (900 MHz/8), then this output frequency sets one of the
    # VCO frequencies.
    clkctrl = None
    clkpll  = None
    synth = None
    if clk == 0:
        synth = _SYNTH_0
        clkctrl = _REG_16_CLK0_CONTROL
    elif clk == 1:
        synth = _SYNTH_1
        clkctrl = _REG_17_CLK1_CONTROL
    elif clk == 2:
        synth = _SYNTH_2
        clkctrl = _REG_18_CLK2_CONTROL
    if pll == b'a':
        clkpll = b'\x0F'
    elif pll == b'b':
        clkpll = b'\x2F'

    if clkctrl and clkpll:
        i2c.writeto_mem(_SI5351_ADDRESS, clkctrl, clkpll)

    if a < 4 or a > 2048:
        raise Exception('multiplier 4-2048')
    
    # Formula for splitting up the numbers to register data, see AN619 
    p1 = 128 * a +  (128 * b // c) - 512; 
    p2 = 128 * b - c * (128 * b // c); 
    p3  = c; 

    buf = bytearray(8)
    buf[0] = (p3 & 0x0000FF00) >> 8
    buf[1] = p3 & 0x000000FF
    buf[2] = (p1 & 0x00030000) >> 16
    buf[3] = (p1 & 0x0000FF00) >> 8
    buf[4] = p1 & 0x000000FF
    buf[5] = ((p3 & 0x000F0000) >> 12) | ((p2 & 0x000F0000) >> 16)
    buf[6] = (p2 & 0x0000FF00) >> 8
    buf[7] = p2 & 0x000000FF
    if synth and buf:
        i2c.writeto_mem(_SI5351_ADDRESS, synth, buf);



# def outen(i2c, en, clk=None):
    # if en:
        # i2c.writeto_mem(_SI5351_ADDRESS, _REG_3_OUTPUT_ENABLE_CONTROL, b'\x00')
    # else:
        # i2c.writeto_mem(_SI5351_ADDRESS, _REG_3_OUTPUT_ENABLE_CONTROL, b'\xff')


