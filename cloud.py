from time import sleep
import paho.mqtt.client as mqtt

#MQTT FUNCTIONS
def on_connect(client, userdata, flags, rc):
    print("Connected ", rc)

def on_publish(client, userdata, result):
    print("Published ", result)

def on_log(client, userdata, level, buf):
    print("log:", buf)

# **1 = send access_log
# **2 = send data

def getField(data):
    thedata = input("Enter somethin: ")
    if data[0:1]=='**':
	    return 'field2=' #alert
    elif data[0:1]=='>>':
        return 'field3=' #access_log
    else:
        return 'field1=' #data

def getData(user,data):
    if data=='>>1':
        return 'ATTEMPTED ACCESS'
    if data=='>>2':
        logstr = str(user)+' LOGGED IN'
        return logstr
    if data=='>>3':
        logstr = str(user)+' LOGGED OUT'
        return logstr
    if data=='>>4':
        return 'FAILED ACCESS ATTEMPT'
    else:
        return 0

#connects to ThingSpeak+updates values until keyboard interrupt
def cloudconnect(user,data):
	try:
		client = mqtt.Client(client_id=user, clean_session=True, userdata=None, protocol=mqtt.MQTTv311, transport="tcp")

		client.on_connect = on_connect
		client.on_publish = on_publish
		client.username_pw_set(MQTT_USERNAME[currUser], password=MQTT_PASSWD[currUser])
		client.connect(MQTT_HOST, port=MQTT_PORT, keepalive=60)
		client.loop_start()

		while True:
			if not client.is_connected:
				print("Client disconnected. Trying to reconnect.")
				client.reconnect()
			#create publish info packet
            WriteString = getData(user,data)
	        WriteField = getField(data)
            pub_topic = str(WriteField) + str(WriteString)
			client.publish(MQTT_PUBLISH_TOPIC, pub_topic)
			print('pub_topic:', pub_topic)
            sleep(15)
        client.disconnect()
        print('DISCONNECTED')

	'''except KeyboardInterrupt:
		client.disconnect()
		print('DISCONNECTED')'''

#INITIALIZATION/VARIABLE
MQTT_USERNAMES = ["mwa0000024515092","",""] #This is the ThingsSpeak's Author
MQTT_PASSWD = ["0BC799CO0TV1B2OL","",""] #This is the MQTT API Key found under My Profile in ThingSpeak

MQTT_HOST = "mqtt.thingspeak.com" #This is the ThingSpeak hostname
MQTT_PORT = 1883 #Typical port # for MQTT protocol. If using TLS -> 8883
CHANNEL_ID = "1600475" #Channel ID found on ThingSpeak website
MQTT_WRITE_APIKEY = "4N3CRBN1QP0RRFOD" # Write API Key found under ThingSpeak Channel Settings
MQTT_PUBLISH_TOPIC = "channels/" + CHANNEL_ID + "/publish/" + MQTT_WRITE_APIKEY