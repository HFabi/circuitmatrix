# ledmatrix matrixportal


## Setup

create a secrets.py
```python
# This file is where you keep secret settings, passwords, and tokens!
# If you put them in the code you risk committing that info or sharing it

secrets = {
    'ssid' : 'XXXXXXX',
    'password' : 'XXXXXXXX',
    'timezone' : "Europe/Berlin", # http://worldtimeapi.org/timezones currently not used
    }
```

helpful links with tutorials, specifications, ...

### matrix portal
- https://learn.adafruit.com/rgb-led-matrices-matrix-panels-with-circuitpython/matrixportal
- https://learn.adafruit.com/adafruit-matrixportal-m4

### circuit python
- https://learn.adafruit.com/welcome-to-circuitpython/installing-circuitpython

### display io
- https://learn.adafruit.com/circuitpython-display-support-using-displayio/library-overview

### example
- https://learn.adafruit.com/weather-display-matrix/code-the-weather-display-matrix
- https://learn.adafruit.com/pyportal-titano-weather-station/code-walkthrough-openweather-graphics-py
- https://learn.adafruit.com/rgb-led-matrices-matrix-panels-with-circuitpython/matrixportal

### adafruit library sources
- https://github.com/adafruit/Adafruit_CircuitPython_MatrixPortal/blob/main/adafruit_matrixportal/matrixportal.py
- https://github.com/adafruit/Adafruit_CircuitPython_PortalBase/blob/main/adafruit_portalbase/__init__.py
- https://github.com/adafruit/Adafruit_CircuitPython_ESP32SPI/blob/main/adafruit_esp32spi/adafruit_esp32spi_wifimanager.py

# Basics of circuit python

- CircuitPython looks for code.py (or code.txt, main.txt, main.py) and executes the code within the file automatically when the board starts up or resets.
- Note that all changes to the contents of CIRCUITPY, such as saving a new file, renaming a current file, or deleting an existing file will trigger a reset of the board.
- Adafruit CircuitPython Library Bundle 

```
minimum required: 

adafruit_matrixportal - this library is the main library used with the MatrixPortal.
adafruit_portalbase - This is the base library that adafruit_matrixportal is built on top of.
adafruit_esp32spi - this is the library that gives you internet access via the ESP32 using (you guessed it!) SPI transport. You need this for anything Internet
neopixel - for controlling the onboard neopixel
adafruit_bus_device - low level support for I2C/SPI
adafruit_requests - this library allows us to perform HTTP requests and get responses back from servers. GET/POST/PUT/PATCH - they're all in here!
adafruit_fakerequests.mpy  - This library allows you to create fake HTTP requests by using local files.
adafruit_io - this library helps connect the PyPortal to our free data logging and viewing service
adafruit_bitmap_font - we have fancy font support, and it's easy to make new fonts. This library reads and parses font files.
adafruit_display_text - not surprisingly, it displays text on the screen
adafruit_lis3dh - this library is used for the onboard accelerometer to detect the orientation of the MatrixPortal

additionally required for this project:
adafruit_datetime
adafruit_display_shapes
adafruit_display_text
adafruit_minimqtt
adafruit_ntp
```




#  Faq
Mosquitto
```
mosquitto_pub -m "{\"text\":\"Hello World\", \"mood\":\"normal\", \"startTime\": 1638973552, \"visemes\": [{\"code\":1,\"duration\":5}]}" -t webtec/lab/mycroft/viseme
```

Error: Expected 01 but got 00
- https://github.com/adafruit/Adafruit_CircuitPython_MiniMQTT/issues/60
- solution: disable ssl and specify correct port

Error: time out of range, ppen issue date_time
- https://circuitpython.org/contributing/open-issues
- https://github.com/adafruit/Adafruit_CircuitPython_datetime/issues/10
- https://github.com/adafruit/Adafruit_CircuitPython_NTP/pull/3/files
- solution: do not use date_time until fixed