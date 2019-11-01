"""
    'KootNet Ethernet Testers' is a collection of scripts and programs
    to test Ethernet cables and or network routes.
    Copyright (C) 2018  Chad Ermacora  chad.ermacora@gmail.com

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""
from PIL import Image, ImageDraw, ImageFont


class CreateWaveShare27EPaper:
    def __init__(self):
        self.rpi_gpio_import = __import__("supported_displays.display_drivers.waveshare.epd2in7")
        self.esp = self.rpi_gpio_import.EPD()
        self.esp.init()

    def display_message(self, text_message):
        # 255 to clear the frame
        display_image = Image.new("1", (self.rpi_gpio_import.EPD_WIDTH, self.rpi_gpio_import.EPD_HEIGHT), 255)
        draw = ImageDraw.Draw(display_image)
        font18 = ImageFont.truetype("/usr/share/fonts/truetype/freefont/FreeSans.ttf", 16)
        draw.text((2, 0), text_message, font=font18, fill=0)
        print(text_message)
        self.esp.display(self.esp.getbuffer(display_image))
