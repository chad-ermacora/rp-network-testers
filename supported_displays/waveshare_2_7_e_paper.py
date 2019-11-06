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
from time import strftime
from PIL import Image, ImageDraw, ImageFont
from operations_modules import file_locations

key1 = 5
key2 = 6
key3 = 13
key4 = 19


class CreateWaveShare27EPaper:
    def __init__(self):
        self.rpi_gpio_import = __import__('RPi.GPIO')
        self.epd2in7_import = __import__("supported_displays.display_drivers.waveshare.epd2in7")
        self.esp = self.epd2in7_import.EPD()
        self.esp.init()

        self.rpi_gpio_import.setmode(self.rpi_gpio_import.BCM)

        self.rpi_gpio_import.setup(key1, self.rpi_gpio_import.IN, pull_up_down=self.rpi_gpio_import.PUD_UP)
        self.rpi_gpio_import.setup(key2, self.rpi_gpio_import.IN, pull_up_down=self.rpi_gpio_import.PUD_UP)
        self.rpi_gpio_import.setup(key3, self.rpi_gpio_import.IN, pull_up_down=self.rpi_gpio_import.PUD_UP)
        self.rpi_gpio_import.setup(key4, self.rpi_gpio_import.IN, pull_up_down=self.rpi_gpio_import.PUD_UP)

        self.key_states = [self.rpi_gpio_import.input(key1), self.rpi_gpio_import.input(key1),
                           self.rpi_gpio_import.input(key1), self.rpi_gpio_import.input(key1)]

    def display_message(self, text_message):
        # 255 to clear the frame
        display_image = Image.new("1", (self.epd2in7_import.EPD_WIDTH, self.epd2in7_import.EPD_HEIGHT), 255)
        draw = ImageDraw.Draw(display_image)
        font18 = ImageFont.truetype(file_locations.location_truetype_font, 16)
        draw.text((2, 0), text_message, font=font18, fill=0)
        print(text_message)
        self.esp.display(self.esp.getbuffer(display_image))

    @staticmethod
    def get_start_message():
        start_message = "Device Ready\n\nBe sure to\nGive 15 Seconds\nFor Remote\nDevice to boot\n\n" + \
                        "  Day/Month/Year\n\nDate: " + str(strftime("%d/%m/%y")) + "\nTime: " + str(strftime("%H:%M"))

        return start_message

    @staticmethod
    def get_mtr_message(cli_results):
        if cli_results[-45:-41] != "Loss":
            message = "MTR Results\n" + \
                      "Sent: " + cli_results[-36:-30] + "\n" + \
                      "Loss: " + cli_results[-45:-38] + "\n" + \
                      "Avg: " + cli_results[-26:-20] + "ms\n" + \
                      "Worst: " + cli_results[-12:-8] + "ms\n" + \
                      "Best: " + cli_results[-19:-14] + "ms\n" + \
                      "Last: " + cli_results[-31:-26] + "ms\n" + \
                      "StDev: " + cli_results[-6:-3] + " ms\n\n" + \
                      "  Day/Month/Year\n\n" + \
                      "Date: " + strftime("%d/%m/%y") + "\n" + \
                      "Time: " + strftime("%H:%M")
        else:
            message = "MTR Failed\n" + \
                      "Remote Unit Offline?\n" + \
                      "  Or\n" + \
                      "Bad Network\n\n" + \
                      "  Day/Month/Year\n\n" + \
                      "Date: " + str(strftime("%d/%m/%y")) + "\n" + \
                      "Time: " + str(strftime("%H:%M"))
        return message

    @staticmethod
    def get_iperf_message(cli_results, cli_ok=True):
        if cli_ok:
            message = "iPerf3 Results\n" + \
                      "Max device Bandwidth:\n" + \
                      "  220Mbps-230Mbps\n\n" + \
                      "Transferred:\n  " + \
                      cli_results[-71:-57] + "\n" + \
                      "Bandwidth:\n  " + \
                      cli_results[-58:-42] + "\n" + \
                      "Over " + cli_results[-83:-70] + "\n\n" + \
                      "  Day/Month/Year\n\n" + \
                      "Date: " + str(strftime("%d/%m/%y")) + "\n" + \
                      "Time: " + str(strftime("%H:%M"))
        else:
            message = "iPerf3 Failed\n" + \
                      "Remote Unit Offline?\n" + \
                      "  Or\n" + \
                      "Bad Network\n\n" + \
                      "  Day/Month/Year\n\n" + \
                      "Date: " + str(strftime("%d/%m/%y")) + "\n" + \
                      "Time: " + str(strftime("%H:%M"))
        return message

    @staticmethod
    def shutdown_remote_unit_message(cli_ok):
        if cli_ok:
            message = "Shutting Down\n" + \
                      "Remote Unit\n\n" + \
                      "  Day/Month/Year\n\n" + \
                      "Date: " + str(strftime("%d/%m/%y")) + "\n" + \
                      "Time: " + str(strftime("%H:%M"))
        else:

            message = "Shut Down Failed\n" + \
                      "Remote Unit Offline\n\n" + \
                      "  Day/Month/Year\n\n" + \
                      "Date: " + str(strftime("%d/%m/%y")) + "\n" + \
                      "Time: " + str(strftime("%H:%M"))
        return message

    @staticmethod
    def shutdown_local_unit_message():
        message = "Shutting Down\n" + \
                  "Local Unit\n\n" + \
                  "  Day/Month/Year\n\n" + \
                  "Date: " + str(strftime("%d/%m/%y")) + "\n" + \
                  "Time: " + str(strftime("%H:%M"))
        return message
