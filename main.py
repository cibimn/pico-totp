import time
import json
import picodisplay as display
from totp import totp
from machine import Pin, I2C
from synchronised_time import create_synchronised_time

LED_BLINK_UNDER_SECONDS = 6

I2C_PORT = 0
I2C_SDA = 20
I2C_SCL = 21

ALARM_PIN = 3

class ds3231(object):
#            13:45:00 Mon 24 May 2021
#  the register value is the binary-coded decimal (BCD) format
#               sec min hour week day month year
    NowTime = b'\x00\x45\x13\x02\x24\x05\x21'
    w  = ["Sunday","Monday","Tuesday","Wednesday","Thursday","Friday","Saturday"];
    address = 0x68
    start_reg = 0x00
    alarm1_reg = 0x07
    control_reg = 0x0e
    status_reg = 0x0f
    
    def __init__(self,i2c_port,i2c_scl,i2c_sda):
        self.bus = I2C(i2c_port,scl=Pin(i2c_scl),sda=Pin(i2c_sda))
    
    def read_time(self):
        t = self.bus.readfrom_mem(int(self.address),int(self.start_reg),7)
        a = t[0]&0x7F  #second
        b = t[1]&0x7F  #minute
        c = t[2]&0x3F  #hour
        d = t[3]&0x07  #week
        e = t[4]&0x3F  #day
        f = t[5]&0x1F  #month
        print("20%x/%02x/%02x %02x:%02x:%02x %s" %(t[6],t[5],t[4],t[2],t[1],t[0],self.w[t[3]-1]))
        print("20%x"%(t[6]))
        time = "20%x/%02x/%02x %02x:%02x:%02x" %(t[6],t[5],t[4],t[2],t[1],t[0])
        return(time)
    
def hex_to_rgb(hex):
    return tuple(int(hex[i:i+2], 16) for i in (1, 3, 5))

rtc = ds3231(I2C_PORT,I2C_SCL,I2C_SDA)
codes = json.loads(open("codes.json", "r").read())
selected_idx = 0

display_width = display.get_width()
display_buffer = bytearray(display_width * display.get_height() * 2)
display.init(display_buffer)
display.set_backlight(0.8)

synchronised_time = create_synchronised_time(display)

while True:
    if display.is_pressed(display.BUTTON_X):
        selected_idx = (selected_idx + 1) % len(codes)
    if display.is_pressed(display.BUTTON_Y):
        selected_idx = (selected_idx - 1) % len(codes)
    code = codes[selected_idx]
    if display.is_pressed(display.BUTTON_A):
        display.set_pen(0, 0, 0)
        display.clear()
    (password, expiry) = totp(synchronised_time(),
                              code['key'],
                              step_secs=code['step'],
                              digits=code['digits'])

    colour = hex_to_rgb(code['colour'])
    display.set_pen(*colour)
    display.clear()
    display.set_led(*colour
                    if expiry <= LED_BLINK_UNDER_SECONDS and expiry % 2
                    else (0, 0, 0))

    display.set_pen(0, 0, 0)
    display.text(code['name'], 10, 10, display_width - 10, 4)
    display.text(password, 10, 60, display_width - 10, 6)

    progress_width = display_width - \
        (display_width // code['step'] * (expiry - 1))
    display.rectangle(0, 125, progress_width, 10)

    display.update()
    time.sleep(0.5)
    
