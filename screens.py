#!/usr/bin/env python3
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
t = 8
loggedIn = False
lockedOut= False

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
    menu = 0
    while menu is not 1 or 2 or 3:
        menu = Key.loop()
    if menu is 1:
        readOutput()
    elif menu is 2:
        write()
    elif menu is 3:
        cloud()



def login():
    #screen.lcd_clear()
    screen.lcd_display_string(' '*16,line=2)
    inputThread = threading.Thread(None,getid)
    screen.lcd_display_string('Enter ID',line=1,pos=4)
    #screen.lcd_display_string('60',line=1,pos=14)  # Placeholder
    inputThread.start()
    

def welcome():
    screen.lcd_clear()
    screen.lcd_display_string('Welcome!',line=1,pos=4)
    screen.lcd_display_string('1.Rd 2.Wrt 3.Cld',line=2)
def addressSelect():
    pass
def readOutput():
    pass
def write():
    pass
def cloud():
    pass
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
login()
