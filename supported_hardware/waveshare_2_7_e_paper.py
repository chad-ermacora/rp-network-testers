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
import os
from time import strftime, sleep
from PIL import Image, ImageDraw, ImageFont
from operations_modules import file_locations
from operations_modules.app_generic_functions import get_raspberry_pi_model


class CreateHardwareAccess:
    def __init__(self):
        self.full_system_text = get_raspberry_pi_model()
        self.band_width_message = "Expected Bandwidth:\n Unknown"
        if self.full_system_text == "Raspberry Pi 3 Model B Plus":
            self.band_width_message = "Expected Bandwidth:\n 290-298 Mbps"
        elif self.full_system_text == "Raspberry Pi 4 Model B":
            self.band_width_message = "Expected Bandwidth:\n 935-955 Mbps"

        try:
            os.system("raspi-config nonint do_spi 0")
            print("\nEnabled SPI for WaveShare 2.7 E-Paper\n")
        except Exception as error:
            print("\nError Enabling SPI for WaveShare 2.7 E-Paper: " + str(error) + "\n")

        # GPIO key to Pin #s
        self.key1 = 5
        self.key2 = 6
        self.key3 = 13
        self.key4 = 19
        self.rpi_gpio_import = __import__('RPi.GPIO', fromlist=["setmode", "BCM", "setup",
                                                                "IN", "PUD_UP", "input"])
        self.epd2in7_import = __import__("supported_hardware.drivers.waveshare.epd2in7",
                                         fromlist=["EPD", "EPD_WIDTH", "EPD_HEIGHT"])
        self.esp = self.epd2in7_import.EPD()
        self.esp.init()

        self.rpi_gpio_import.setmode(self.rpi_gpio_import.BCM)

        self.rpi_gpio_import.setup(self.key1, self.rpi_gpio_import.IN, pull_up_down=self.rpi_gpio_import.PUD_UP)
        self.rpi_gpio_import.setup(self.key2, self.rpi_gpio_import.IN, pull_up_down=self.rpi_gpio_import.PUD_UP)
        self.rpi_gpio_import.setup(self.key3, self.rpi_gpio_import.IN, pull_up_down=self.rpi_gpio_import.PUD_UP)
        self.rpi_gpio_import.setup(self.key4, self.rpi_gpio_import.IN, pull_up_down=self.rpi_gpio_import.PUD_UP)

    def get_key_states(self):
        return [self.rpi_gpio_import.input(self.key1), self.rpi_gpio_import.input(self.key2),
                self.rpi_gpio_import.input(self.key3), self.rpi_gpio_import.input(self.key4)]

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
        start_message = "Device Ready\n\nBe sure to\nGive 15 Seconds\nFor Remote\nDevice to boot\n\n"
        return start_message

    @staticmethod
    def get_mtr_message(cli_results):
        if cli_results[-42:-38] != "Loss":
            message = " MTR Results\n" + \
                      " Sent: " + cli_results[-33:-27] + "\n" + \
                      " Lost: " + cli_results[-42:-35] + "\n" + \
                      " Avg: " + cli_results[-23:-17] + "ms\n" + \
                      " Worst: " + cli_results[-9:-5] + "ms\n" + \
                      " Best: " + cli_results[-16:-11] + "ms\n" + \
                      " Last: " + cli_results[-28:-23] + "ms\n" + \
                      " StDev: " + cli_results[-3:] + " ms\n\n" + \
                      "   Day/Month/Year\n" + \
                      "     Date: " + strftime("%d/%m/%y") + "\n" + \
                      "       Time: " + strftime("%H:%M")
        else:
            message = " MTR Failed\n" + \
                      " Remote Unit Offline?\n" + \
                      "   Or\n" + \
                      " Bad Network\n\n" + \
                      "   Day/Month/Year\n\n" + \
                      " Date: " + str(strftime("%d/%m/%y")) + "\n" + \
                      " Time: " + str(strftime("%H:%M"))
        return message

    def get_iperf_message(self, cli_results, cli_ok=True):
        if cli_ok:
            print(cli_results)
            message = " iPerf3 Results\n" + \
                      self.band_width_message + "\n" + \
                      " Amount Transferred:\nIn:" + \
                      cli_results[-68:-54] + "\nOut:" + \
                      cli_results[-144:-130] + "\n" + \
                      " Average Bandwidth:\nIn:" + \
                      cli_results[-55:-39] + "\nOut:" + \
                      cli_results[-131:-115] + "\n" + \
                      " Over: " + cli_results[-80:-67] + "\n\n" + \
                      "   Day/Month/Year\n" + \
                      "     Date: " + str(strftime("%d/%m/%y")) + "\n" + \
                      "       Time: " + str(strftime("%H:%M"))
        else:
            message = " iPerf3 Failed\n" + \
                      " Remote Unit Offline?\n" + \
                      "   Or\n" + \
                      " Bad Network\n\n" + \
                      "   Day/Month/Year\n\n" + \
                      " Date: " + str(strftime("%d/%m/%y")) + "\n" + \
                      " Time: " + str(strftime("%H:%M"))
        return message

    @staticmethod
    def shutdown_remote_unit_message(cli_ok):
        if cli_ok:
            message = " Shutting Down\n" + \
                      " Remote Unit\n\n" + \
                      "   Day/Month/Year\n\n" + \
                      " Date: " + str(strftime("%d/%m/%y")) + "\n" + \
                      " Time: " + str(strftime("%H:%M"))
        else:

            message = " Shut Down Failed\n" + \
                      " Remote Unit Offline\n\n" + \
                      "   Day/Month/Year\n\n" + \
                      " Date: " + str(strftime("%d/%m/%y")) + "\n" + \
                      " Time: " + str(strftime("%H:%M"))
        return message

    @staticmethod
    def shutdown_local_unit_message():
        message = " Shutting Down\n" + \
                  " Local Unit\n\n" + \
                  "   Day/Month/Year\n\n" + \
                  " Date: " + str(strftime("%d/%m/%y")) + "\n" + \
                  " Time: " + str(strftime("%H:%M"))
        return message
