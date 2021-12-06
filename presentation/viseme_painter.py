import os
import sys

import config
from models.mood import Mood

sys.path.append(os.path.abspath(os.path.dirname(__file__) + '/../../rpi-rgb-led-matrix/bindings/python/'))
from rgbmatrix import RGBMatrix, RGBMatrixOptions
from PIL import Image


class VisemePainter:
    """This class can show visems on a led matrix"""

    def __init__(self):
        print("init viseme painter")
        options = RGBMatrixOptions()
        options.hardware_mapping = config.HARDWARE_MAPPING
        options.rows = 32
        options.cols = 32
        options.chain_length = 1
        options.parallel = 1
        options.row_address_type = 0
        options.multiplexing = 0
        options.pwm_bits = 11
        options.brightness = 100
        options.pwm_lsb_nanoseconds = 130
        options.led_rgb_sequence = "RGB"
        options.pixel_mapper_config = ""
        
        # options.show_refresh_rate = 0
        options.gpio_slowdown = 1
        #options.disable_hardware_pulsing = True
        #options.drop_privileges=False # self.parser.set_defaults(drop_privileges=True)
        
        self.matrix = RGBMatrix(options=options)

    def draw_viseme(self, viseme_code, mood):
        print("drawing viseme code ", viseme_code, " on matrix")

        # validate input
        if viseme_code not in range(0, 6):
            print("error: viseme unknown: ", viseme_code)
            return
        if mood not in ["normal"]:
            print("error: mood unknown: ", mood)
            return
        print("cwd:", os.getcwd())
        print("listdir:", os.listdir("."))
        image_path = os.getcwd() + "/resources/" + mood.lower() + "/" +  str(viseme_code)+".png"
        self.draw_image(image_path)

    def draw_image(self, image_file_path):
        image = Image.open(image_file_path)
        print("image size: ", image.size)
        
        image.thumbnail((self.matrix.width, self.matrix.height), Image.ANTIALIAS)
        width, height = image.size
        print("image size: ", width, height)
        
        # Why do I need False here? It seems to work in the example without false?
        self.matrix.SetImage(image.convert('RGB'), 0,0,False)


    def clear(self):
        print("clear matrix")
        self.matrix.Clear()
