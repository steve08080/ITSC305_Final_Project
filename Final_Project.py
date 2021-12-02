#IMPORTS
import gpiozero
import signal
import time
import I2C_LCD_Driver 
import Keypad

#GLOBAL VARIABLE INITIALIZATION
buzzer = LED(21) #set buzzer on/off switch
ledPin = 23
mSensor = MotionSensor(4)
mylcd = I2C_LCD_Driver.lcd()
mylcd.lcd_backlight(0)
mSensor.when_motion = set_alarm
alarm = 0
mykey = Keypad.Keypad()
signal.signal(signal.SIGALRM, alarm_handler)
users = {										#user/id pairs
				user1 : pass1,
        user2 : pass2
		}
class TimeOutException(Exception):
    pass
def alarm_handler(signum, frame):
    print("ALARM signal recieved")
    raise TimeOutException()

#FUNCTIONS
def write_screen(): #Write output to screen
		return 0

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
    		input = mykey.getKey()
        mylcd.lcd_display_string(input, pos=count, line=2)
        user+=input
        count+=1
    mylcd.lcd_clear()
    return user

def erase_mem():			#used when timeout reached
  	mylcd.lcd_display_string('ERASING')
    #STOP HERE UNTIL MEMORY IS ERASED
  	mylcd.lcd_backlight(0)
    return 0
  
def welcome_page():		#used when entries are valid
  	mylcd.lcd_display_string('WELCOME')
  	return 0

def set_alarm(): #set alarm when motion detected
  	global users
    buzzer.on()
    mylcd.backlight(1)
    signal.alarm(30)
    try:        #VERIFY
        while True:												#main loop, until timeout or valid user/id pair
        		while True:												#username loop, until existing user entered
        				user = get_keypad()
                if user in list(users):	
                  	mylcd.lcd_display_string('Valid user')
                		break
                else:
                  	mylcd.lcd_display_string('Invalid user')
            if rfid_read(user)==1:					#stop alarm if id matches user
                signal.alarm(0)
                buzzer.off()
                break
    except (TimeOutException, WrongPass):		#erase data if timeout encountered
        erase_mem()
    finally:																#Run welcome screen if login succesful
      	welcome_page()

    return 0