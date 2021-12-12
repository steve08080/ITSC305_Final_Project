#!/usr/bin/env python3
import RPi.GPIO as GPIO
import Keypad       #import module Keypad

GPIO.setwarnings(False)

ROWS = 4        # number of rows of the Keypad
COLS = 4        #number of columns of the Keypad
keys =  [   '1','2','3','A',    #key code
            '4','5','6','B',
            '7','8','9','C',
            '*','0','#','D'     ]
rowsPins = [5,6,13,19]        #connect to the row pinouts of the keypad
colsPins = [24,22,27,17]        #connect to the column pinouts of the keypad

def loop():
    keypad = Keypad.Keypad(keys,rowsPins,colsPins,ROWS,COLS)    #creat Keypad object
    keypad.setDebounceTime(50)      #set the debounce time
    while(True):
      try:
        key = keypad.getKey()       #obtain the state of keys
        if(key != keypad.NULL):     #if there is key pressed, print its key code.
            print ("You Pressed Key : %c "%(key))
            return key
      except KeyboardInterrupt:
        return -1