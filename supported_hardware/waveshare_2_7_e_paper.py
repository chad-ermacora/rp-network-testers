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
from time import strftime
from PIL import Image, ImageDraw, ImageFont
from operations_modules import file_locations
from operations_modules import app_variables
from operations_modules.config_primary import current_config
from operations_modules.app_generic_functions import get_raspberry_pi_model, get_network_ip, get_os_name_version


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
        start_message = "Kootnet Tester\nVersion: " + current_config.app_version + \
                        "\n\nDevice Ready\n\nBe sure to\nGive 15 Seconds\nFor Remote\nDevice to boot\n\n"
        return start_message

    def get_mtr_message(self):
        cli_results = app_variables.previous_mtr_results
        if cli_results[-42:-38] != "Loss":
            mtr_results_list = self._get_real_lines_mtr(cli_results)
            message = " MTR Results\n  " + \
                      mtr_results_list[0][2] + "  " + mtr_results_list[0][5] + "  " + mtr_results_list[0][7] + "\n"

            for line in mtr_results_list[1:]:
                message += "  IP: " + line[1] + \
                           "\n  " + line[2] + "  " + line[5] + "ms  " + line[7] + "ms\n"
        else:
            message = " MTR Failed\n" + \
                      " Remote Unit Offline?\n" + \
                      " Or\n" + \
                      " Bad Network\n\n"

        message += "\n   Day/Month/Year\n" + \
                   "     Date: " + strftime("%d/%m/%y") + "\n" + \
                   "       Time: " + strftime("%H:%M")
        return message

    def _get_real_lines_mtr(self, mtr_results):
        mtr_results_lines = mtr_results.strip().split("\n")
        return_results = []
        for line in mtr_results_lines:
            return_results.append(self._get_mtr_or_iperf_real_list(line.split(" ")))
        return return_results

    @staticmethod
    def _get_mtr_or_iperf_real_list(mtr_results_lines):
        real_first_list = []
        for line in mtr_results_lines:
            if line.strip() == "":
                pass
            else:
                real_first_list.append(line.strip())
        return real_first_list

    def get_iperf_message(self, cli_ok=True):
        cli_results = app_variables.previous_iperf_results
        iperf_results_lines = cli_results.strip().split("\n")
        send_results_list = self._get_real_lines_mtr(iperf_results_lines[-4].split(" "))
        receive_line_list = self._get_real_lines_mtr(iperf_results_lines[-3].split(" "))
        if cli_ok and len(send_results_list) > 7 and len(receive_line_list) > 7:
            print(cli_results)
            message = " iPerf3 Results\n" + \
                      self.band_width_message + "\n" + \
                      " Amount Transferred:\nIn:" + \
                      str(receive_line_list[-3]) + str(receive_line_list[-2]) + "\nOut:" + \
                      str(send_results_list[-3]) + str(send_results_list[-2]) + "\n" + \
                      " Average Bandwidth:\nIn:" + \
                      str(receive_line_list[-5]) + str(receive_line_list[-4]) + "\nOut:" + \
                      str(send_results_list[-5]) + str(send_results_list[-4]) + "\n" + \
                      " Over: " + str(receive_line_list[-7]) + str(receive_line_list[-6]) + "\n\n" + \
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

    def _get_real_lines_iperf(self, iperf_results):
        results_lines = iperf_results.strip().split("\n")
        sender_line_list = self._get_mtr_or_iperf_real_list(results_lines[0].split(" "))
        receiver_line_list = self._get_mtr_or_iperf_real_list(results_lines[1].split(" "))
        return [sender_line_list, receiver_line_list]

    @staticmethod
    def get_sys_info_message():
        date_now = strftime("%d/%m/%y")
        time_now = strftime("%H:%M")
        net_ip = get_network_ip()
        os_text = get_os_name_version()

        if current_config.running_on_rpi:
            lines = os_text.split(" ")
            os_text = lines[0] + " " + lines[2]

        text_msg = "Version: " + current_config.app_version + "\nOS: " + os_text + \
                   "\nDate: " + date_now + " (D/M/Y)\nTime: " + time_now + \
                   "\n\nLocal IP\n" + net_ip + "\nRemote Test Server IP\n" + current_config.remote_tester_ip
        return text_msg

    @staticmethod
    def shutdown_local_unit_message():
        message = " Shutting Down\n" + \
                  " Local Unit\n\n" + \
                  "   Day/Month/Year\n\n" + \
                  " Date: " + str(strftime("%d/%m/%y")) + "\n" + \
                  " Time: " + str(strftime("%H:%M"))
        return message
