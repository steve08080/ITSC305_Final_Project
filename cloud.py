from time import sleep
import paho.mqtt.client as mqtt

#MQTT FUNCTIONS
def on_connect(client, userdata, flags, rc):
    print("Connected ", rc)

def on_publish(client, userdata, result):
    print("Published ", result)

def on_log(client, userdata, level, buf):
    print("log:", buf)

def on_message(client, userdata, message):
    print("Message topic: ", message.topic)    
    print("Message payload: ", message.payload)
    print("Message QoS: ", message.qos)
    return message.payload

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

#get user # to reference thingspeak credentials from list
def getUser(user):
    if user=='853192':
        return 2
    elif user=='':
        return 1
    elif user=='':
        return 0

#connects to ThingSpeak+updates values until keyboard interrupt
def cloudpub(user,data):
    currUser = getUser(user)
	try:
		client = mqtt.Client(client_id=user, clean_session=True, userdata=None, protocol=mqtt.MQTTv311, transport="tcp")

		client.on_connect = on_connect
		client.on_publish = on_publish
		client.username_pw_set(MQTT_USERNAME[currUser], password=MQTT_PASSWD[currUser])
		client.connect(MQTT_HOST, port=MQTT_PORT, keepalive=60)
		client.loop_start()

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

#gets data from field2 and returns  it
def cloudsub(user,data):
    currUser = getUser(user)
    try:
        client = mqtt.Client(client_id=user, clean_session=True, userdata=None, protocol=mqtt.MQTTv311, transport="tcp")

        client.on_connect = on_connect
        client.on_message = on_message
        client.username_pw_set(MQTT_USERNAME[currUser], password=MQTT_PASSWD[currUser])
        client.connect(MQTT_HOST, port=MQTT_PORT, keepalive=60)
        client.loop_start()
        client.subscribe(MQTT_SUBSCRIBE_TOPIC, qos=0)
        
        if not client.is_connected:
            print("Client disconnected. Trying to reconnect.")
            client.reconnect()

        sleep(15)
        client.unsubscribe(MQTT_SUBSCRIBE_TOPIC)
        client.disconnect()
        return client.on_message

    '''except KeyboardInterrupt:
        client.unsubscribe(MQTT_SUBSCRIBE_TOPIC)
        client.disconnect()'''


#INITIALIZATION/VARIABLE
MQTT_USERNAMES = ["","","mwa0000024515092"] #This is the ThingsSpeak's Author
MQTT_PASSWD = ["","","0BC799CO0TV1B2OL"] #This is the MQTT API Key found under My Profile in ThingSpeak
MQTT_HOST = "mqtt.thingspeak.com" #This is the ThingSpeak hostname
MQTT_PORT = 1883 #Typical port # for MQTT protocol. If using TLS -> 8883
CHANNEL_ID = "1600475" #Channel ID found on ThingSpeak website
MQTT_READ_APIKEY = "VL80D7RG3043TO7C" # Read API Key
MQTT_WRITE_APIKEY = "4N3CRBN1QP0RRFOD" # Write API Key
MQTT_PUBLISH_TOPIC = "channels/" + CHANNEL_ID + "/publish/" + MQTT_WRITE_APIKEY
MQTT_SUBSCRIBE_TOPIC = "channels/" + CHANNEL_ID + "/subscribe/fields/field2/" + MQTT_READ_APIKEY