#IMPORTS
import gpiozero
import signal
import time

#GLOBAL VARIABLE INITIALIZATION
buzzer = LED(21) #set buzzer on/off switch
mSensor = MotionSensor(4)
mSensor.when_motion = set_alarm
alarm = 0
signal.signal(signal.SIGALRM, alarm_handler)
users = (user1, user2)

class TimeOutException(Exception):
    pass
def alarm_handler(signum, frame):
    print("ALARM signal recieved")
    raise TimeOutException()

#FUNCTIONS
def write_screen(): #Write output to screen
    return 0

def rfid_read(): #read from rfid to check for valid card
    global users
    id = rfid.read()
    for user in users:
        if id==user:
            return 1
    return 0

def get_keypad(): #get values from keypad
    return 0

def erase_mem():
    return 0

def set_alarm(): #set alarm when motion detected
    signal.alarm(30)
    try:        #VERIFY
        while True:
            if rfid_read()==1:
                signal.alarm(0)
                break
    except (TimeOutException, WrongPass):
        erase_mem()

    return 0
