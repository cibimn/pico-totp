import time
from machine import Pin, I2C

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
        time = "20%x %02x %02x %02x %02x %02x" %(t[6],t[5],t[4],t[2],t[1],t[0])
        tim = time.split(" ")
        tim = [int(x) for x in tim] 
        print(tim)
        return tim
rtc = ds3231(I2C_PORT,I2C_SCL,I2C_SDA)
def create_synchronised_time(display):
    datetime = rtc.read_time()
    print(type(datetime))
    selected_idx = 0

    display_width = display.get_width()
    display_height = display.get_height()

    delta = time.mktime(datetime + [0, 0]) - int(time.time())

    def synchronised_time():
        return int(time.time()) + delta

    return synchronised_time

