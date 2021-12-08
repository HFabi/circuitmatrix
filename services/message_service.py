from models.messages.speak_message import SpeakMessage
from models.messages.status_message import StatusMessage
from models.viseme import Viseme
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

    def __init__(self, client_name, host, port, socket, esp):

        mqtt.set_socket(socket, esp)
        # Set up a MiniMQTT Client
        self.mqtt_client = mqtt.MQTT(
            broker="192.168.2.103",
            port=1883,
            client_id=client_name,
            is_ssl=False,
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

    def subscribe_mycroft_speak(self, on_speak_message):
        print("MqttService - subscribe_mycroft_speak")
        self.mqtt_client.subscribe("webtec/#", 0)
        self.on_speak_message = on_speak_message

    def subscribe(self, topic):
        self.mqtt_client.subscribe(topic, 0)

    def disconnect(self):
        self.mqtt_client.disconnect()

    def publish(self, topic, message):
        self.mqtt_client.publish(topic, message)

    def on_message_received(self, client, topic, message):
        print("MqttService - on_message_received")
        if topic == config.TOPIC_STATUS:
            if self.on_status_message is not None:
                self.on_status_message(self.parse_status(message))
        elif topic == config.TOPIC_SPEAK:
            if self.on_speak_message is not None:
                self.on_speak_message(self.parse_speak(message))
        else:
            print("MqttService - error message unknown")

    def on_connect(self, client, userdata, flags, rc):
        print("MqttService - on_connect")

    def on_disconnect(self, client, userdata, rc):
        print("MqttService - on_disconnect")

    # json parsing

    def parse_speak(self, json_string):
        json_dict = json.loads(json_string)
        visemes = []
        for viseme in json_dict['visemes']:
            visemes.append(Viseme(viseme['code'], viseme['duration']))
        return SpeakMessage(json_dict['text'], json_dict['mood'], json_dict['startTime'], visemes)

    def parse_status(self, json_string):
        json_dict = json.loads(json_string)
        return StatusMessage(json_dict['status'])

    def loop(self):
        print("loop")
        self.mqtt_client.loop()
