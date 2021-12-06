from ledmatrix.models.messages.speak_message import SpeakMessage
from ledmatrix.models.messages.status_message import StatusMessage
from ledmatrix.models.viseme import Viseme
import adafruit_minimqtt.adafruit_minimqtt as mqtt

try:
    from secrets import secrets
except ImportError:
    print("WiFi secrets are kept in secrets.py, please add them there!")
    raise

import json
import config


class MessageService:
    """Receive and send MQTT messages"""

    def __init__(self, client_name, host, port):
        print("Connecting to %s" % secrets["ssid"])
        wifi.radio.connect(secrets["ssid"], secrets["password"])
        print("Connected to %s!" % secrets["ssid"])

        # Create a socket pool
        pool = socketpool.SocketPool(wifi.radio)

        # Set up a MiniMQTT Client
        self.mqtt_client = MQTT.MQTT(
            broker=secrets["broker"],
            port=secrets["port"],
            username=secrets["aio_username"],
            password=secrets["aio_key"],
            socket_pool=pool,
            ssl_context=ssl.create_default_context(),
        )
        self.mqtt_client.on_connect = self.on_connect
        self.mqtt_client.on_disconnect = self.on_disconnect
        self.mqtt_client.on_message = self.on_message_received
        self.mqtt_client.connect()

        self.on_status_message = None
        self.on_speak_message = None

    def subscribe_mycroft_status(self, on_status_message):
        self.mqtt_client.subscribe(config.TOPIC_STATUS, 0)
        self.on_status_message = on_status_message
        self.mqtt_client.loop_forever()

    def subscribe_mycroft_speak(self, on_speak_message):
        self.mqtt_client.subscribe(config.TOPIC_SPEAK, 0)
        self.on_speak_message = on_speak_message
        self.mqtt_client.loop_forever()

    def subscribe(self, topic):
        self.mqtt_client.subscribe(topic, 0)
        self.mqtt_client.loop_forever()

    def disconnect(self):
        self.mqtt_client.disconnect()

    def publish(self, topic, message):
        self.mqtt_client.publish(topic, message)

    def on_message_received(self, client, userdata, message):
        print("MqttService - on_message_received")
        if message.topic == config.TOPIC_SPEAK:
            if self.on_status_message is not None:
                self.on_status_message(self.parse_speak(message))
        elif message.topic == config.TOPIC_STATUS:
            if self.on_speak_message is not None:
                self.on_speak_message(self.parse_status(message))
        else:
            print("MqttService - error message unknown")

    def on_connect(self, client, userdata, flags, rc):
        print("MqttService - on_connect")

    def on_disconnect(self, client, userdata, rc):
        print("MqttService - on_disconnect")

    # json parsing

    def parse_speak(json_string):
        json_dict = json.loads(json_string)
        visemes = []
        for viseme in json_dict['visemes']:
            visemes.append(Viseme(viseme['code'], viseme['duration']))
        return SpeakMessage(json_dict['text'], json_dict['mood'], json_dict['startTime'], visemes)

    def parse_status(json_string):
        json_dict = json.loads(json_string)
        return StatusMessage(json_dict['status'])

    def loop(self):
        pass