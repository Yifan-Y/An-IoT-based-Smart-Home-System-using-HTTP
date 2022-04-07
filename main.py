from machine import UART, Pin
from esp8266 import ESP8266
from lcd1602 import LCD
import machine
import utime
import math
import time
import sys

## ONBOARD COMPONENTS
lcd = LCD() # Create a LCD instance
thermistor = machine.ADC(28) # The thermistor connects to the GPIO 28
led_user = machine.PWM(machine.Pin(15)) # The LED connects to the GPIO 15
photoRes = machine.ADC(machine.Pin(26)) # The Photoresistor connects to the GPIO 26
led = Pin(25,Pin.OUT) # The onboard LED connects to the GPIO 25
led_user.freq(1000) # Set the LED frequency at 1000 Hz

## WIFI MODUAL (ESP8266)
esp01 = ESP8266() # Create an ESP8266 instance
esp8266_at_ver = None # Create an variable to record the AT version
wifi_ssid = "VIDEOTRON2830" # Configure the ssid of wifi ap
wifi_pswd = "M9KFU4MK7VCJU" # Configure the password of wifi ap

## GET TEMPERATURE (ADC)
def tempCalculate():
    temperature_value = thermistor.read_u16()
    Vr = 3.3 * float(temperature_value) / 65535
    Rt = 10000 * Vr / (3.3 - Vr)
    temp = 1/(((math.log(Rt / 10000)) / 3950) + (1 / (273.15+25)))
    Cel = temp - 273.15
    Fah = Cel * 1.8 + 32
    #print ('Celsius: %.2f C  Fahrenheit: %.2f F' % (Cel, Fah))
    cel = str('{:.2f}'.format(Cel))
    fah = str('{:.2f}'.format(Fah))
    return cel, fah

## DISPLAY TEMPERATURE ON LCD
def lcdDisplay(temp):
    string = " Temperature is \n    " + temp + " C    "
    lcd.message(string)
    #utime.sleep(1)
    #lcd.clear()

## LIGHT INTENSITY ADJUSTMENT
def ledAdjustment(photoGP):
    light = round(photoGP.read_u16()/65535*100, 2)
    #print ("light: " + str(light) +"%")
    lightstr = str(light)
    utime.sleep_ms(200)
    if light <= 40:
        led_user.duty_u16(65535)
        utime.sleep_ms(10)
    elif light > 40 and light <= 60:
        led_user.duty_u16(32768)
        utime.sleep_ms(10)
    elif light > 60 and light <= 80:
        led_user.duty_u16(16383)
        utime.sleep_ms(10)
    else:
        led_user.duty_u16(0)
        utime.sleep_ms(10)
    return lightstr

## START UP WIFI MODUAL
print("StartUP",esp01.startUP()) ## Checking the communication between MCU and ESP 8266
lcd.message("Starting Up...")
print("Echo-Off",esp01.echoING()) ## Enabling the AT command echo off
print("\r\n")

## Print ESP8266 AT comand version and SDK details
esp8266_at_ver = esp01.getVersion()
if(esp8266_at_ver != None):
    print(esp8266_at_ver)

## Set the current WiFi in SoftAP+STA mode
esp01.setCurrentWiFiMode()
print("\r\n")

## Connect with the WiFi
print("Try to connect with the WiFi...")
lcd.clear()
lcd.message("Connecting WIFI")
while (1):
    if "WIFI CONNECTED" in esp01.connectWiFi(wifi_ssid, wifi_pswd):
        print("CONNECTION SUCCESSFUL...")
        lcd.clear()
        lcd.message("Seccessful!")
        time.sleep(2)
        break;
    else:
        print("CONNECTION FAILED...")
        lcd.clear()
        lcd.message("Failed!")
        time.sleep(2)

print("Now it's time to start HTTP Post Operation.......\r\n")

lcd.clear()

while(1):    
    # Toggle the onboard LED to indicate working status
    led.toggle()
    time.sleep(1)
    
    # Fetch data from sensors
    postCal, postFah = tempCalculate()
    lcdDisplay(postCal)
    postLight = ledAdjustment(photoRes)

    # Build up JSON statement
    post_json = "{\"Temperature in Celsius\":\"" + postCal + "\",\"Temperature in Fahrenheit\":\"" + postFah + "\",\"Light Intensity\":\"" + postLight + "\"}"
    print ("Posting JSON statement: " + post_json + "\n")
    
    ## Starting HTTP Post Operations    
    httpCode, httpRes = esp01.doHttpPost("thingsboard.cloud","/api/v1/ACCESSTOKEN/telemetry","7fea98e0-b3bb-11ec-97ae-79978f9d7342", "application/json",post_json,port=80)
    print("-------------------------- HTTP Post Operation Result -----------------------")
    print("HTTP Code:",httpCode) ## If HTTP Code == 200, Operation OK, otherwise failed.
    print("HTTP Response:",httpRes)
    print("-----------------------------------------------------------------------------\r\n\r\n")
    if httpCode == "200":
        print("HTTP post operation successful!")
    else:
        print("HTTP post operation failed! Error Code: " + httpCode + "\n")

    





