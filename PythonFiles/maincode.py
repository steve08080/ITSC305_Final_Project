#!/usr/bin/env python3
import I2C_LCD_Driver as i2c
import threading
import time
import eeprom
import Key
import RPi.GPIO as GPIO
import math
import nrfid
import cloud
import os
import sys
import cloudsub

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
    try:
     p.start(50)
     for x in range(0,361):
         sinVal = math.sin(x * (math.pi / 180.0))
         toneVal = 2000 + sinVal * 500
         p.ChangeFrequency(toneVal)
         time.sleep(0.001)
    except KeyboardInterrupt:
     stopAlertor()
     return
def stopAlertor():
    p.stop()

def setup():
    global p
    #print("mode: " + str(GPIO.getmode()))
    GPIO.setmode(GPIO.BCM)
    #print(GPIO.getmode())
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
    global session
    if id in userids:
       scanScreen(0)
       tag = 0
       tag = nrfid.rfidReadLoop()
       print('tag is ' + str(tag) +  ' and userids[id] is ' + str(userids[id]))
       if str(tag) == str(userids[id]):
           loggedIn = True
           tagstring = ''
           for i in userids[id]:
              tagstring = tagstring + str(i)
              print('tagstring:', tagstring)
           session = tagstring
           cloud.cloudpub(id,tagstring,'>>1')
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
        options = {'1':addressSelect,'2':addressSelect,'3':cloudScreens,'*':logout}
        while option is None:
            option = Key.loop()
            #option = input()
        try:
            options[option]()
        except KeyError:
            print('Bad option')
            return

    elif menu is 'cloudScreens':
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
    screen.lcd_clear()
    screen.lcd_display_string('Enter ID',line=1,pos=4)
    getid()
    return

def logout():
    global session
    cloud.cloudpub('0',session,'>>2')
    os.execl(sys.executable,sys.executable,*sys.argv)


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
            writeScreen(address)
        else:
            readOutput(address)
    else:
        print('TODO')  # TODO cloud


def writeScreen(address):
    passw = ''
    posit = 0
    digit = ''
    screen.lcd_clear()
    screen.lcd_display_string('Enter a pass')
    while posit < 15:
       digit = Key.loop()
       if digit is '#':
          screen.lcd_display_string(' '*16,line=2)
          posit = 0
          continue
       elif digit is '*':
          passw = bytes(passw.encode('ascii'))
          if len(passw) < 15:
             passw = passw + b'\x00'
          lock.acquire()
          mem.write(address,passw)
          lock.release()
          break
       passw = passw + digit
       screen.lcd_display_string(digit,line=2,pos=posit)
       posit = posit + 1

def readOutput(address):
    screen.lcd_clear()
    screen.lcd_display_string(f'Read from {hex(address)}:')
    lock.acquire()
    output = mem.read(address,8)
    lock.release()
    printout = []
    for i in output:
        if i == 0:
           break
        printout.append(i)
    screen.lcd_display_string(''.join(map(str,printout)),line=2) #  str(output),line=2)
    x = None
    while x is None:
        x = Key.loop()
        #x = input()
    return


def scanScreen(address):
    screen.lcd_clear()
    screen.lcd_display_string('Waiting for RFID...')
    screen.lcd_display_string('...',line=2,pos=6)
    x = None
    #while x is None:  # TODO scan
        #x = Key.loop()
        # x = input()
    return


def cloudScreens():
    global menu
    menu = 'cloudScreens'
    screen.lcd_clear()
    screen.lcd_display_string('Cloud Operations')
    screen.lcd_display_string('1.Pblsh 2.Sbscrb',line=2)
    getmenu()
    return


def lockout():
    screen.lcd_clear()
    screen.lcd_display_string('***LOCKED***',line=1,pos=2)
    cloud.cloudpub('1','1','>>3')
    try:
      alertor()
      print('locked out')
      cloudsub.subloop()
      stopAlertor()
      os.execl(sys.executable,sys.executable,*sys.argv)
    except KeyboardInterrupt:
      stopAlertor()
        # key = thingspeak.subscribe()
        # if key = localkey:
        #   break

mem = eeprom.EEPROM(0,1)
screen = i2c.lcd()
lock = threading.Lock()
userids = {'845312':[136,4,190,199], '682758':[136,4,136,199], '853192':[136,4,184,199]}
session = None
t = 5
loggedIn = False
lockedOut= False
menu = None
option = None
buzzer = 21
ledPin = 23
sensorPin = 18
GPIO.setwarnings(False)
countdownThread = threading.Thread(None,countdown)
countdownThread.start()
setup()
while True:

    if GPIO.input(sensorPin)==GPIO.HIGH:
        break
    else:
        GPIO.output(ledPin,GPIO.LOW)
        stopAlertor()
GPIO.output(ledPin,GPIO.HIGH)
alertor()
stopAlertor()

while True:
     while not loggedIn and not lockedOut:
        login()
     while loggedIn:
        welcome()