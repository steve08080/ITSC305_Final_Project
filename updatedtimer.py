#!/usr/bin/env python3

import RPi.GPIO as GPIO
import time
import math
import I2C_LCD_Driver

buzzer = 40       # define buzzer
ledPin = 16       # define ledPin
sensorPin = 12    # define sensorPin
GPIO.setwarnings(False)
mylcd = I2C_LCD_Driver.lcd()
mylcd.backlight(0)
t = 60

def countdown(t):
    while t:
        if t >= 10:
            mylcd.lcd_display_string(str(t),pos=14,line=1)
        else:
            mylcd.lcd_display_string(' ',pos=14,line=1)
            mylcd.lcd_display_string(str(t), pos=15,line=1)
        time.sleep(1)
        t -=1

def setup():
    global p
    GPIO.setmode(GPIO.BOARD)        # use PHYSICAL GPIO Numbering
    GPIO.setup(buzzer, GPIO.OUT)    # set buzzer to OUTPUT mode
    GPIO.setup(ledPin, GPIO.OUT)    # set ledPin to OUTPUT mode
    GPIO.setup(sensorPin, GPIO.IN)  # set sensorPin to INPUT mode
    p = GPIO.PWM(buzzer, 1)
    p.start(0);

def loop():
    while True:
        if GPIO.input(sensorPin)==GPIO.HIGH:
            break
        else :
            GPIO.output(ledPin,GPIO.LOW) # turn off led
            stopAlertor()
            #print ('alertor turned off <<<')
            #mylcd.backlight(0)
    GPIO.output(ledPin,GPIO.HIGH) # turn on led
    alertor()
    login()
    countdown(t)
    #mylcd.lcd_display_string('Enter ID: ')
    stopAlertor()

def login():
    mylcd.lcd_display_string('Enter ID: ',pos=3,line=1)

def destroy():
    GPIO.output(buzzerPin, GPIO.LOW)    #Turns off the buzzer
    GPIO.cleanup()                     # Release GPIO resource

def alertor():
    p.start(50)
    for x in range(0,361):      #Makes the frequency of the alertor consistent with sine wave
        sinVal = math.sin(x * (math.pi / 180.0))
        toneVal = 2000 + sinVal * 500
        p.ChangeFrequency(toneVal)
        time.sleep(0.001)

def stopAlertor():
    p.stop()

if __name__ == '__main__':     # Program entrance
    print ('Program is starting...')
    setup()
    try:
        loop()
    except KeyboardInterrupt:  # Press ctrl-c to end the program.
        destroy()
