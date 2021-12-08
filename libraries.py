#IMPORTS
#import gpiozero
import signal
import time
import I2C_LCD_Driver
#from gpiozero import LED, MotionSensor
import RPi.GPIO as GPIO
import Key

#GLOBAL VARIABLE INITIALIZATION
#buzzer = LED(21) #set buzzer on/off switch
ledPin = 23
#mSensor = MotionSensor(4)
mylcd = I2C_LCD_Driver.lcd()
mylcd.backlight(0)
menuflag = 0
###
# menuFlag will be used in inputLoop to determine which screen to enter
# 0 = login
# 1 = welcome
# 2 = address select
# 3 = read output
# 4 = write
# 5 = cloud
#       1 = publish
#       2 = subscribe
# 6 = success
# 7 = fail
# 8 = lockout
###
def login():
  print("test worked")
  mylcd.lcd_display_string("Enter ID: ")
  inputLoop()

screenfuncs = {0:login}

GPIO.setwarnings(False)

def inputLoop():
  key = Key.loop()
  print(f"got key {key}")
  screenfuncs[int(key)]()

def set_alarm(): #set alarm when motion detected
        global users
        #buzzer.on()
        mylcd.backlight(1)
        signal.alarm(30)
        try:            #VERIFY
                while True:                                                    #main loop, until timeout or valid user/id pair
                        while True:                                            #username loop, until existing user entered
                                        user = get_keypad()
                                        if user in list(users):
                                                mylcd.lcd_display_string('Valid user')
                                                break
                                        else:
                                                mylcd.lcd_display_string('Invalid user')
                                        if rfid_read(user)==1:                                  #stop alarm if id matches use
                                                signal.alarm(0)
                                                #buzzer.off()
                                                break
        except (TimeOutException, WrongPass):           #erase data if timeout encountered
                erase_mem()
        finally:                               #Run inputloop for data menu if login succesful
                inputloop()
        return 0

#mSensor.when_motion = set_alarm
def alarm_handler(signum, frame):
        print("ALARM signal recieved")
        raise TimeOutException()
alarm = 0
signal.signal(signal.SIGALRM, alarm_handler)
'''
users = {                                              #user(student id #) + password
                853192 : pass1,
                user2 : pass2
                }
'''
class TimeOutException(Exception):
        pass
'''
def alarm_handler(signum, frame):
        print("ALARM signal recieved")
        raise TimeOutException()
'''
def rfid_read(user): #read from rfid to check for valid card
        global users
        my.lcd_display_string('Scan id for %s' % user)
        id = rfid.read()
        mylcd.clear()
        if id==users.get(user):
                mylcd.lcd_display_string('Login success')
                return 1
        mylcd.lcd_display_string('Login failed')
        return 0

def get_keypad(): #get values from keypad
        count = 0
        mylcd.lcd_display_string('Enter user:')
        while input!='#' and count<8:
                input = Key.loop() #or something
                mylcd.lcd_display_string(input, pos=count, line=2)
                user+=input
                count+=1
                mylcd.lcd_clear()
        return user

def erase_mem():                        #used when timeout reached
        mylcd.lcd_display_string('ERASING')
        #STOP HERE UNTIL MEMORY IS ERASED
        mylcd.lcd_backlight(0)
        return 0

inputLoop()