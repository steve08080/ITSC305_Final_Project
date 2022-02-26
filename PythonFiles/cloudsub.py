from time import sleep
import paho.mqtt.client as mqtt

MQTT_CLIENT_ID = '' # This is for your own client identification. Can be anything
MQTT_USERNAME = '' #This is the ThingsSpeak's Author
MQTT_PASSWD = '' #This is the MQTT API Key found under My Profile in ThingSpeak
MQTT_HOST = "mqtt3.thingspeak.com" #This is the ThingSpeak hostname
MQTT_PORT = 1883 #Typical port # for MQTT protocol. If using TLS -> 8883
CHANNEL_ID = '' #Channel ID found on ThingSpeak website
MQTT_READ_APIKEY = '' # Read API Key found under ThingSpeak Channel Settings
MQTT_SUBSCRIBE_TOPIC = "channels/" + CHANNEL_ID + "/subscribe/fields/field4"#/" + MQTT_READ_APIKEY

received = None

"""
Standard callback functions. See Phao MQTT documentation for more
This will be called on receipt of a message from the subscribed topic(s)
"""

def on_message(client, userdata, message):
    global received
    print('yay')
    print("Message topic: ", message.topic)
    print("Message payload: ", message.payload)
    print("Message QoS: ", message.qos)
    received = message.payload

def on_subscribe(client_id, userdata, mid, granted_qos):
    print('subscribed')
    print(granted_qos)

"""
This function will be called upon connection
"""

def on_connect(client, userdata, flags, rc):
    print("Connected ", rc)

def subloop():
    global received
    try:
        """ create client instance"""
        client = mqtt.Client(client_id=MQTT_CLIENT_ID, clean_session=True, userdata=None, protocol=mqtt.MQTTv311, transport="tcp")
        print('client created ', client)

        """ standard callback bindings """

        client.on_connect = on_connect
        client.on_message = on_message
        client.on_subscribe = on_subscribe


        """ Set the conneciton authentication. """
        client.username_pw_set(MQTT_USERNAME, password=MQTT_PASSWD)
        """ Connect client """
        client.connect(MQTT_HOST, port=MQTT_PORT, keepalive=60)
        """ start the looping of client connection. This needs to be done otherwise the connection will only happen once and expire """
        client.loop_start()

        """
        subscribe to the predefined topic(s). To subscribe to multiple topics, define a List of Tuples:
        client.subscribe([(topic1, qos),(topic2, qos),...])
        """
        client.subscribe(MQTT_SUBSCRIBE_TOPIC, qos=0)
        print('sublooping')
        while True:
            sleep(1)
            if received != None:
               client.disconnect()
               print('disconnect')
               break
            if not client.is_connected:
                print("Client disconnected. Trying to reconnect.")
                client.reconnect()

    except KeyboardInterrupt:
        print('bye')
        client.unsubscribe(MQTT_SUBSCRIBE_TOPIC)
        client.disconnect()
