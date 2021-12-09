#!/usr/bin/env python3
import I2C_LCD_Driver as i2c
import threading
import time
import eeprom
import Key
import RPi.GPIO as GPIO
import math

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
        return

    else:
        return


def getid():
    global lockedOut
    posit = 5
    id = ''
    while posit < 11 and not lockedOut:
        digit = Key.loop()
        #digit = input()
        if digit is '#':
            posit = 5
            id = ''
            screen.lcd_display_string(' '*16,line=2,pos=0)
            continue
        if not lockedOut:
            id = id + digit
            screen.lcd_display_string(digit,line=2,pos=posit)
            posit = posit+1

    if lockedOut:
        return
    else:
        authenticate(id)
        return


def getaddress():
    posit = 6
    address = ''
    while posit < 10:
        digit = Key.loop()
        #digit = input()
        if digit is '#':
            posit = 6
            address = ''
            screen.lcd_display_string(' '*16,line=2,pos=0)
            continue
        elif digit is '*':
            return -1
        address = address + digit
        screen.lcd_display_string(digit,pos=posit,line=2)
        posit = posit+1

    return int(address,16)


def getmenu():
    global menu
    global option
    option = None

    if menu is 'welcome':
        options = {'1':addressSelect,'2':addressSelect,'3':cloud}
        while option is None:
            option = Key.loop()
            #option = input()
        try:
            options[option]()
        except KeyError:
            print('Bad option')
            return

    elif menu is 'cloud':
        while option is None:
            option = Key.loop()
            #option = input()
            if option is '1' or option is '2':
                break
            elif option is '*':
                return
            else:
                print('Bad option')
                option = None

        addressSelect()


def login():
    screen.lcd_display_string(' '*16,line=2)
    screen.lcd_display_string('Enter ID',line=1,pos=4)
    getid()
    return


def welcome():
    global menu
    menu = 'welcome'
    screen.lcd_clear()
    screen.lcd_display_string('Welcome!',line=1,pos=4)
    screen.lcd_display_string('1.Rd 2.Wrt 3.Cld',line=2)
    getmenu()


def addressSelect():
    screen.lcd_clear()
    screen.lcd_display_string('Address to ')
    if option is '2':
        write = True
    else:
        write = False

    if write:
        screen.lcd_display_string('Write',pos=11)
    else:
        screen.lcd_display_string('Read',pos=11)

    address = getaddress()
    if address < 0:
        return

    if menu is 'welcome':
        if write:
            scanScreen(address)
        else:
            readOutput(address)
    else:
        print('TODO')  # TODO cloud

def readOutput(address):
    screen.lcd_clear()
    screen.lcd_display_string(f'Read from {hex(address)}:')
    lock.acquire()
    output = mem.read(address,3)
    lock.release()
    screen.lcd_display_string(str(output),line=2)
    x = None
    while x is None:
        # x = Key.loop()
        x = input()
    return


def scanScreen(address):
    screen.lcd_clear()
    screen.lcd_display_string('Waiting for RFID...')
    screen.lcd_display_string('...',line=2,pos=6)
    x = None
    while x is None:  # TODO scan
        x = Key.loop()
        # x = input()
    return


def cloud():
    global menu
    menu = 'cloud'
    screen.lcd_clear()
    screen.lcd_display_string('Cloud Operations')
    screen.lcd_display_string('1.Pblsh 2.Sbscrb',line=2)
    getmenu()
    return


def lockout():
    screen.lcd_clear()
    screen.lcd_display_string('***LOCKED***',line=1,pos=2)
    while 1:
        alertor()
        pass
        # key = thingspeak.subscribe()
        # if key = localkey:
        #   break

mem = eeprom.EEPROM(0,0)
screen = i2c.lcd()
lock = threading.Lock()
userids = ('111111', '845312', '682758', '853192')
t = 8
loggedIn = False
lockedOut= False
menu = None
option = None
buzzer = 40
ledPin = 16
sensorPin = 12
GPIO.setwarnings(False)
countdownThread = threading.Thread(None,countdown)
countdownThread.start()

while True:
    setup()
    if GPIO.input(sensorPin)==GPIO.HIGH:
        break
    else:
        GPIO.output(ledPin,GPIO.LOW)
        stopAlertor()
GPIO.output(ledPin,GPIO.HIGH)
alertor()
stopAlertor()
login()

while loggedIn:
    welcome()