#!/usr/bin/env python3
import RPi.GPIO as GPIO
import math
import I2C_LCD_Driver as i2c
import threading
import time
import Key
"""
login
welcome
address select
read output
write
cloud
    publish
    subscribe
success
fail
lockout
"""
screen = i2c.lcd()
userids = ('111111', '845312', '682758', '853192')
t = 60
loggedIn = False
lockedOut= False
menu = 'login'
option = 0
buzzer = 40
ledPin = 16
sensorPin = 12
GPIO.setwarnings(False)

def alertor():
    p.start(50)
    for x in range(0,361):
        sinVal = math.sin(x * (math.pi / 180.0))
        toneVal = 2000 + sinVal * 500
        p.ChangeFrequency(toneVal)
        time.sleep(0.001)

def stopAlertor():
    p.stop()

def setup():
    global p
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(buzzer, GPIO.OUT)
    GPIO.setup(ledPin, GPIO.OUT)
    GPIO.setup(sensorPin, GPIO.IN)
    p = GPIO.PWM(buzzer, 1)
    p.start(0);

def countdown():
    global t
    global loggedIn
    global lockedOut
    while t:
        if loggedIn:
            print("Quitting countdown: logged in")
            return
        time.sleep(1)
        t -=1
    lockedOut = True
    lockout()

def authenticate(id):
    global loggedIn
    if id in userids:
        loggedIn = True
        print("Yay")
        welcome()
        return
    else:
        print("Fail")
        login()
        return

def getid():
    global lockedOut
    posit = 5
    id = ''
    while posit < 11 and not lockedOut:
        digit = Key.loop()
        if digit is '#':
            posit = 5
            id = ''
            screen.lcd_display_string(' '*16,line=2,pos=0)
            continue
        if not lockedOut:
            id = id + digit
            print(f'id is {id}')
            screen.lcd_display_string(digit,line=2,pos=posit)
            posit = posit+1

    if lockedOut:
        return
    else:
        return authenticate(id)

def getmenu():
    global menu
    global option
    option = 0
    if menu is 'home':
        while option is not 1 or 2 or 3:
            option = Key.loop()
        if option is 1:
            addressSelect()
        elif option is 2:
            addressSelect()
        elif option is 3:
            cloud()



def login():
    menu = 'login'
    screen.lcd_display_string(' '*16,line=2)
    inputThread = threading.Thread(None,getid)
    screen.lcd_display_string('Enter ID',line=1,pos=4)
    inputThread.start()

def welcome():
    menu = 'welcome'
    screen.lcd_clear()
    screen.lcd_display_string('Welcome!',line=1,pos=4)
    screen.lcd_display_string('1.Rd 2.Wrt 3.Cld',line=2)
    getmenu()


def addressSelect():
    pass
def readOutput():
    screen.lcd_clear()
    screen.lcd_display_string('address')
def write():
    pass
def cloud():
    screen.lcd_clear()
    screen.lcd_display_string('cloud')
def success():
    pass
def fail():
    pass
def lockout():
    screen.lcd_clear()
    screen.lcd_display_string('***LOCKED***',line=1,pos=2)
screenfuncs = {0:login,1:welcome,2:addressSelect,3:readOutput,4:write,5:cloud,6:success,7:fail,8:lockout}
countdownThread = threading.Thread(None,countdown)
countdownThread.start()
while True:
    setup()
    if GPIO.input(sensorPin)==GPIO.HIGH:
        #print("got it")
        break
    else:
        GPIO.output(ledPin,GPIO.LOW)
        stopAlertor()
GPIO.output(ledPin,GPIO.HIGH)
alertor()
login()
stopAlertor()