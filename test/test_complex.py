
import pytest
from pytest_report import log


def test_complex_procedure():
    # Power & Reset
    log.step('Power & Reset sequence', procedure_info={
        'note': 'Bring up supplies and issue a clean reset before peripheral configuration'
    })
    log.substep(f'Write: micro.power.vdd[EN] = {1}', procedure_info={
        'writeop': True, 'reg': 'micro.power.vdd[EN]', 'value': 1, 'readback': 1
    })
    log.substep(f'Write: micro.power.vddio[EN] = {1}', procedure_info={
        'writeop': True, 'reg': 'micro.power.vddio[EN]', 'value': 1, 'readback': 1
    })
    log.substep(f'Write: micro.reset[ASSERT] = {1}', procedure_info={
        'writeop': True, 'reg': 'micro.reset[ASSERT]', 'value': 1, 'readback': 1
    })
    log.substep(f'Write: micro.reset[ASSERT] = {0}', procedure_info={
        'writeop': True, 'reg': 'micro.reset[ASSERT]', 'value': 0, 'readback': 0
    })

    # Clock configuration
    log.step('Clock configuration', procedure_info={
        'note': 'Configure PLL and dividers prior to enabling interfaces that depend on system clock'
    })
    log.substep(f'Write: micro.clk.pll[CTRL] = {0x1A}', procedure_info={
        'writeop': True, 'reg': 'micro.clk.pll[CTRL]', 'value': 0x1A, 'readback': 0x1A
    })
    log.substep(f'Write: micro.clk.sys[DIV] = {2}', procedure_info={
        'writeop': True, 'reg': 'micro.clk.sys[DIV]', 'value': 2, 'readback': 2
    })

    # GPIO / I/O registers (expanded)
    log.step('Configure I/O pins', procedure_info={
        'note': 'Establish directions and default output levels; odd pins as inputs, even pins as outputs'
    })
    for pin in range(1, 9):
        en = 1
        dir_val = 1 if pin % 2 == 0 else 0
        out_val = 0x80 + pin
        log.substep(f'Write: micro.io.io{pin}[EN] = {en}', procedure_info={
            'writeop': True, 'reg': f'micro.io.io{pin}[EN]', 'value': en, 'readback': en
        })
        log.substep(f'Write: micro.io.io{pin}[DIR] = {dir_val}', procedure_info={
            'writeop': True, 'reg': f'micro.io.io{pin}[DIR]', 'value': dir_val, 'readback': dir_val
        })
        if dir_val == 1:
            log.substep(f'Write: micro.io.io{pin}[OUT] = {hex(out_val)}', procedure_info={
                'writeop': True, 'reg': f'micro.io.io{pin}[OUT]', 'value': out_val, 'readback': out_val
            })

    # UART
    log.step('Write into UART registers', procedure_info={
        'note': 'UART2 not present on this device; only UART1 is configured'
    })
    log.substep(f'Write: micro.io.uart1[BAUD] = {115200}', procedure_info={
        'writeop': True, 'reg': 'micro.io.uart1[BAUD]', 'value': 115200, 'readback': 115200
    })
    log.substep(f'Write: micro.io.uart1[CTRL] = {0x03}', procedure_info={
        'writeop': True, 'reg': 'micro.io.uart1[CTRL]', 'value': 0x03, 'readback': 0x03
    })
    log.substep(f'Write: micro.io.uart1[TX] = {0x00}', procedure_info={
        'writeop': True, 'reg': 'micro.io.uart1[TX]', 'value': 0x00, 'readback': 0x00
    })

    # SPI
    log.step('Configure SPI interface', procedure_info={
        'note': 'SPI set to Mode 0 with CS idle high; adjust per attached device requirements'
    })
    log.substep(f'Write: micro.io.spi[CTRL] = {0x5}', procedure_info={
        'writeop': True, 'reg': 'micro.io.spi[CTRL]', 'value': 0x5, 'readback': 0x5
    })
    log.substep(f'Write: micro.io.spi[CS] = {1}', procedure_info={
        'writeop': True, 'reg': 'micro.io.spi[CS]', 'value': 1, 'readback': 1
    })
    log.substep(f'Write: micro.io.spi[TXN] = {0xDE}', procedure_info={
        'writeop': True, 'reg': 'micro.io.spi[TXN]', 'value': 0xDE, 'readback': 0xDE
    })

    # I2C
    log.step('Configure I2C bus', procedure_info={
        'note': 'I2C enabled with a placeholder target address; bus speed not tuned in this sample'
    })
    log.substep(f'Write: micro.io.i2c[EN] = {1}', procedure_info={
        'writeop': True, 'reg': 'micro.io.i2c[EN]', 'value': 1, 'readback': 1
    })
    log.substep(f'Write: micro.io.i2c[TIMEOUT] = {100}', procedure_info={
        'writeop': True, 'reg': 'micro.io.i2c[TIMEOUT]', 'value': 100, 'readback': 100
    })
    log.substep(f'Write: micro.io.i2c[ADDR] = {0x50}', procedure_info={
        'writeop': True, 'reg': 'micro.io.i2c[ADDR]', 'value': 0x50, 'readback': 0x50
    })
    log.substep(f'Write: micro.io.i2c[TX] = {0xA0}', procedure_info={
        'writeop': True, 'reg': 'micro.io.i2c[TX]', 'value': 0xA0, 'readback': 0xA0
    })

    # ADC
    log.step('ADC configuration and kicks', procedure_info={
        'note': 'Channels configured with a simple pattern; conversion results are not sampled in this mock'
    })
    for ch in range(0, 4):
        cfg = 0x10 | ch
        log.substep(f'Write: micro.adc.ch{ch}[CFG] = {hex(cfg)}', procedure_info={
            'writeop': True, 'reg': f'micro.adc.ch{ch}[CFG]', 'value': cfg, 'readback': cfg
        })
        log.substep(f'Write: micro.adc.ch{ch}[START] = {1}', procedure_info={
            'writeop': True, 'reg': f'micro.adc.ch{ch}[START]', 'value': 1, 'readback': 1
        })

    # Timers / PWM
    log.step('Timers and PWM setup', procedure_info={
        'note': 'Timers started with nominal values; PWM configured for a mid-duty reference'
    })
    log.substep(f'Write: micro.timer.timer0[LOAD] = {0xFFFE}', procedure_info={
        'writeop': True, 'reg': 'micro.timer.timer0[LOAD]', 'value': 0xFFFE, 'readback': 0xFFFE
    })
    log.substep(f'Write: micro.timer.timer0[CTRL] = {0x1}', procedure_info={
        'writeop': True, 'reg': 'micro.timer.timer0[CTRL]', 'value': 0x1, 'readback': 0x1
    })
    log.substep(f'Write: micro.pwm.pwm0[DUTY] = {128}', procedure_info={
        'writeop': True, 'reg': 'micro.pwm.pwm0[DUTY]', 'value': 128, 'readback': 128
    })

    # Interrupts
    log.step('Interrupt controller configuration', procedure_info={
        'note': 'Mask carefully; enabling all sources here is for demonstration only'
    })
    log.substep(f'Write: micro.int.ENABLE = {0xFFFF}', procedure_info={
        'writeop': True, 'reg': 'micro.int.ENABLE', 'value': 0xFFFF, 'readback': 0xFFFF
    })
    log.substep(f'Write: micro.int.CLEAR = {0xFFFF}', procedure_info={
        'writeop': True, 'reg': 'micro.int.CLEAR', 'value': 0xFFFF, 'readback': 0xFFFF
    })

    # Security / Misc
    log.step('Security and identification', procedure_info={
        'note': 'Locking security configuration prevents accidental changes during runtime'
    })
    log.substep(f'Write: micro.sec.cfg[LOCK] = {1}', procedure_info={
        'writeop': True, 'reg': 'micro.sec.cfg[LOCK]', 'value': 1, 'readback': 1
    })

    # Final process remarks
    log.step('Process summary', procedure_info={
        'note': 'Bring-up order: power → reset → clocks → GPIO → serial buses → converters → timers → interrupts → security'
    })