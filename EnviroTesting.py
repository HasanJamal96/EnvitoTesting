from time import sleep
from enviroplus import gas
from bme280 import BME280
from pms5003 import PMS5003
import ST7735
from PIL import Image, ImageDraw, ImageFont
from fonts.ttf import RobotoMedium as UserFont
import requests
'''
BME_API = ''
Gas_API = ''
Light_API = ''
Proximity_API = ''
Particulate_API = ''
'''

disp = ST7735.ST7735(
    port=0,
    cs=1,
    dc=9,
    backlight=12,
    rotation=270,
    spi_speed_hz=10000000
)

disp.begin()

WIDTH = disp.width
HEIGHT = disp.height

img = Image.new('RGB', (WIDTH, HEIGHT), color=(0, 0, 0))
draw = ImageDraw.Draw(img)


try:
    from smbus2 import SMBus
except ImportError:
    from smbus import SMBus

bus = SMBus(1)
bme280 = BME280(i2c_dev=bus)

    
try:
    from ltr559 import LTR559
    ltr559 = LTR559()
except ImportError:
    import ltr559

gas.enable_adc()
gas.set_adc_gain(4.096)


pms5003 = PMS5003(
    device='/dev/ttyAMA0',
    baudrate=9600,
    pin_enable=22,
    pin_reset=27
)

def ReadPariculate():
    data = ""
    try:
        print("Reading pariculate sensor")
        data = pms5003.read()
        data = str(data.pm_ug_per_m3(1.0)) + ',' + str(data.pm_ug_per_m3(2.5)) + ','  + str(data.pm_ug_per_m3(10))
        UpdateDisplay(msg, 0, 41, 3)
    except:
        print("Error reading pariculate sensor")
    
    data = 

def ReadMICS6814():
    data = ""
    try:
        print("Reading gas sensor values")
        readings = gas.read_all()
        data = str(float(readings.oxidising/1000)) + ',' + str(float(readings.reducing /1000)) + ',' + str(float(readings.nh3/1000)) + ',' + str(readings.adc)
        UpdateDisplay(msg, 0, 21, 2)
    except:
        print("Error reading gas sensor values")
    
    return data

def ReadLTR559():
    data = ""
    try:
        print("Reading light intensity and proximity values")
        LUX = ltr559.get_lux()
        Proximity = ltr559.get_proximity()
        data = str(LUX) + ',' + str(Proximity)
        UpdateDisplay(msg, 0, 11, 1)
    except:
        print("Error reading light intensity and proximity values")


def ReadBME():
    data = ""
    try:
        print("Reading temperature, humidity and pressure values")
        temperature = bme280.get_temperature()
        pressure = bme280.get_pressure()
        humidity = bme280.get_humidity()
        data = str(temperature) + ',' + str(humidity) + ',' + str(pressure)
        UpdateDisplay(msg, 0, 0, 0)
    except:
        print("Error reading temperature, humidity and pressure values")
    
    return data


def UpdateDisplay(msg, xpos, ypos, mode):
    global img
    font_size = 10
    text_colour = (255, 255, 255)
    back_colour = (0, 170, 170)
    font = ImageFont.truetype(UserFont, font_size)
    
    if(mode == 0):
        draw.rectangle((0, 0, WIDTH, 10), back_colour)
        msg = msg.split(",") 
        message = str(msg[0]) + "*C, " + str(msg[1]) + "rh%, " + str(msg[2]) + "hpa"
        draw.text((xpos, ypos), message, font=font, fill=text_colour)

    elif(mode == 1):
        draw.rectangle((0, 11, WIDTH, 20), back_colour)
        msg = msg.split(",") 
        message = str(msg[0]) + "LUX, Proxmity: " + str(msg[1])
        draw.text((xpos, ypos), message, font=font, fill=text_colour)

    elif(mode == 2):
        draw.rectangle((0, 21, WIDTH, 40), back_colour)
        msg = msg.split(",") 
        message = "Oxi: " + str(msg[0]) + " Red: " + str(msg[1])
        draw.text((xpos, ypos), message, font=font, fill=text_colour)
        message = "NH3: " + str(msg[2]) + " O3: " + str(msg[3])
        draw.text((xpos, ypos+10), message, font=font, fill=text_colour)

    elif(mode == 3):
        draw.rectangle((0, 41, WIDTH, 50), back_colour)
        msg = msg.split(",") 
        message = "PM1: " + str(msg[0]) + " PM2.5: " + str(msg[1]) + " PM10: " + str(msg[2])
        draw.text((xpos, ypos), message, font=font, fill=text_colour)
    
    disp.display(img)
    

def ClearDisplay():
    global img
    img = Image.new('RGB', (WIDTH, HEIGHT), color=(0, 0, 0))
    draw = ImageDraw.Draw(img)

while True:
    try:
        ClearDisplay()
        data_BME = ReadBME()
        '''if(data_BME != ''):
            response = requests.post(BME_API, data = data_BME)'''
        sleep(1)
        
        data_LTR559 = ReadLTR559()
        '''if(data_LTR559 != ""):
            data_LTR = data_LTR559.split(",")  
            response = requests.post(Light_API, data = data_LTR[0])
            response = requests.post(Proximity_API, data = data_LTR[1])'''
        sleep(1)
        
        data_MICS6814 = ReadMICS6814()
        '''if(data_MICS6814 != ''):
            response = requests.post(Gas_API, data = data_MICS6814)'''
        sleep(1)
        
        data_pariculate = ReadPariculate()
        '''if(data_pariculate != ''):
            response = requests.post(Particulate_API, data = data_pariculate)'''
        sleep(1)
        
    except KeyboardInterrupt:
        disp.set_backlight(0)    
    
    
    