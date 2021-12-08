import config


from adafruit_matrixportal.matrix import Matrix
import displayio

class VisemePainterC:
    """This class can show visems on a led matrix"""

    def __init__(self):
        print("init viseme painter c")
        self.matrix = Matrix(width=32, height=32)
        self.display = self.matrix.display
        self.g = displayio.Group()
        self.display.show(self.g)

    def draw_viseme(self, viseme_code, mood):
        print("drawing viseme code ", viseme_code, " on matrix")

        # validate input
        if viseme_code not in range(0, 6):
            print("error: viseme unknown: ", viseme_code)
            return
        if mood not in ["normal"]:
            print("error: mood unknown: ", mood)
            return

        image_path = "/resources/" + mood.lower() + "Bmp/" +  str(viseme_code) + ".bmp"
        self.draw_image(image_path)

    def draw_image(self, image_file_path):
        odb = displayio.OnDiskBitmap(image_file_path)
        face = displayio.TileGrid(odb, pixel_shader=odb.pixel_shader)
        if self.g:
            self.g.pop()
        self.g.append(face)


    def clear(self):

        if self.g:
            self.g.pop()

    def loop(self):
        pass
