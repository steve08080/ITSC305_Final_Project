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
    global payload
    payload = message.payload
    print("Message topic: ", message.topic)
    print("Message payload: ", message.payload)
    print("Message QoS: ", message.qos)

# **1 = send access_log email
# **2 = send data email

def getField(data):
    if data[0:3]=='>>1':
        return 'field1=' #login
    elif data[0:3]=='>>2':
        return 'field2=' #logout
    elif data[0:3]=='>>3':
        return 'field3=' #lockedout
    else:
        return 0 #'field1=' #data

#connects to ThingSpeak+updates values until keyboard interrupt
def cloudpub(user,userid,data):
        client = mqtt.Client(client_id=user, clean_session=True, userdata=None, protocol=mqtt.MQTTv311, transport="tcp")

        client.on_connect = on_connect
        client.on_publish = on_publish
        client.username_pw_set(MQTT_USERNAME, password=MQTT_PASSWD)
        client.connect(MQTT_HOST, port=MQTT_PORT, keepalive=60)
        client.loop_start()

        if not client.is_connected:
            print("Client disconnected. Trying to reconnect.")
            client.reconnect()
    #create publish info packet
        WriteString = userid #getData(user,userid,data)
        WriteField = getField(data)
        pub_topic = str(WriteField) + str(WriteString)
        client.publish(MQTT_PUBLISH_TOPIC, pub_topic)
        print('pub_topic:', pub_topic)
        sleep(1)
        client.disconnect()
        print('DISCONNECTED')

#gets data from field2 and returns  it
def cloudsub(user,data):
    global payload
    client = mqtt.Client(client_id=user, clean_session=True, userdata=None, protocol=mqtt.MQTTv311, transport="tcp")

    client.on_connect = on_connect
    client.on_message = on_message
    client.username_pw_set(MQTT_USERNAME, password=MQTT_PASSWD)
    client.connect(MQTT_HOST, port=MQTT_PORT, keepalive=60)
    client.loop_start()
    client.subscribe(MQTT_SUBSCRIBE_TOPIC, qos=0)

    if not client.is_connected:
        print("Client disconnected. Trying to reconnect.")
        client.reconnect()

    sleep(15)
    client.unsubscribe(MQTT_SUBSCRIBE_TOPIC)
    client.disconnect()
    return payload

#INITIALIZATION/VARIABLE
MQTT_USERNAME = 'ED0QNQgrHRw6CicuOggLOx8' #This is the ThingsSpeak's Author
MQTT_PASSWD = '8qxnTOcr7SH+FeuBPw2LwwoN' #This is the MQTT API Key found under My Profile in ThingSpeak
MQTT_HOST = "mqtt.thingspeak.com" #This is the ThingSpeak hostname
MQTT_PORT = 1883 #Typical port # for MQTT protocol. If using TLS -> 8883
CHANNEL_ID = "1600475" #Channel ID found on ThingSpeak website
MQTT_READ_APIKEY = "VL80D7RG3043TO7C" # Read API Key
MQTT_WRITE_APIKEY = "4N3CRBN1QP0RRFOD" # Write API Key
MQTT_PUBLISH_TOPIC = "channels/" + CHANNEL_ID + "/publish/" + MQTT_WRITE_APIKEY
MQTT_SUBSCRIBE_TOPIC = "channels/" + CHANNEL_ID + "/subscribe/fields/field2/" + MQTT_READ_APIKEY
payload = None