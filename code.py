import adafruit_datetime as datetime
import time
import config


from models.messages.speak_message import SpeakMessage
from models.viseme import Viseme
from presentation.viseme_painter_c import VisemePainterC
#from services.message_service import MessageService

if __name__ == '__main__':
    
    # setup   

    painter = VisemePainterC()
    #message_service = MessageService(config.MQTT_CLIENT_NAME, config.MQTT_HOST, config.MQTT_PORT)
    #message_service.subscribe_mycroft_status(handle_message)
    #message_service.subscribe_mycroft_speak(handle_speak_message)

    message_queue = []
    draw_queue = []
    draw_msg_start_time = -1

    visemes1 = [Viseme(1, 3), Viseme(2, 10), Viseme(3, 12)]
    message1 = SpeakMessage("Hello World", "normal", time.monotonic() + 5, visemes1)
    message_queue.append(message1)

    visemes2 = [Viseme(1, 5), Viseme(2, 8)]
    message2 = SpeakMessage("Hello World 2", "normal", time.monotonic()+ 30, visemes2)
    message_queue.append(message2)

  
    # main loop
    while True:
        updated_queue = []
        now = time.monotonic()
        painter.loop()
        
        for msg in message_queue:
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
