import adafruit_datetime as datetime
import time
import config

from adafruit_esp32spi import adafruit_esp32spi
from adafruit_esp32spi import adafruit_esp32spi_wifimanager
import adafruit_esp32spi.adafruit_esp32spi_socket as socket
from adafruit_ntp import NTP
from digitalio import DigitalInOut
import board
import busio

from models.messages.speak_message import SpeakMessage
from models.viseme import Viseme
from presentation.viseme_painter_c import VisemePainterC
from services.message_service import MessageService

try:
    from secrets import secrets
except ImportError:
    print("WiFi secrets are kept in secrets.py, please add them there!")
    raise
    
    

def handle_speak_message(msg):
    message_queue.append(msg)
    print(message_queue)
    print("--")


if __name__ == '__main__':

    # setup wifi
    esp32_cs = DigitalInOut(board.ESP_CS)
    esp32_ready = DigitalInOut(board.ESP_BUSY)
    esp32_reset = DigitalInOut(board.ESP_RESET)

    spi = busio.SPI(board.SCK, board.MOSI, board.MISO)
    esp = adafruit_esp32spi.ESP_SPIcontrol(spi, esp32_cs, esp32_ready, esp32_reset)
    

    wifi = adafruit_esp32spi_wifimanager.ESPSPI_WiFiManager(esp, secrets)
    print("Connecting to %s" % secrets["ssid"])
    wifi.connect()
    print("Connected to %s!" % secrets["ssid"])
    
    # setup time with ntp
    ntp = NTP(esp)
    ntp.set_time(1)
    while not ntp.valid_time:
        ntp.set_time()
        print("Failed to obtain time, retrying in 5 seconds...")
        time.sleep(5)
    print("time:" + str(esp.get_time()))

    painter = VisemePainterC()
    message_service = MessageService(config.MQTT_CLIENT_NAME, config.MQTT_HOST, config.MQTT_PORT, socket, esp)
    #message_service.subscribe_mycroft_status(handle_message)
    message_service.subscribe_mycroft_speak(handle_speak_message)

    message_queue = []
    draw_queue = []
    draw_msg_start_time = -1

    visemes1 = [Viseme(1, 3), Viseme(2, 10), Viseme(3, 12)]
    message1 = SpeakMessage("Hello World", "normal", time.time() + 5, visemes1)
    message_queue.append(message1)

    #visemes2 = [Viseme(1, 5), Viseme(2, 8)]
    #message2 = SpeakMessage("Hello World 2", "normal", time.monotonic()+ 30, visemes2)
    #message_queue.append(message2)


    # main loop
    while True:
        print(message_queue)
        updated_queue = []
        now = time.time()
        print("time:" + str(time.time()))
        painter.loop()
        message_service.loop()

        for msg in message_queue:
            print(str(msg.startTime) + " " + str(now) + "       " + str(msg.startTime <= now))
            if msg.startTime <= now:
                draw_queue = msg.visemes
                draw_msg_start_time = msg.startTime
            else:
                updated_queue.append(msg)

        message_queue = updated_queue

        # wenn timestamps bis wann?
        if draw_queue:
            if draw_msg_start_time + draw_queue[0].duration > now:
                painter.draw_viseme(draw_queue[0].code, "normal")
            else:
                draw_queue.pop(0)
        else:
            painter.clear()
