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
import socket
import subprocess
from time import sleep, strftime
from operations_modules import config_pi
from supported_displays import save_to_file

mtr_cli_command = "mtr -c 10 -r -n " + config_pi.remote_tester_ip
iperf_cli_command = "iperf3 -c " + config_pi.remote_tester_ip + " -O 1 -p " + config_pi.iperf_port
server_address = (config_pi.remote_tester_ip, 10062)


def start_display_server():
    rpi_gpio_import = __import__('RPi.GPIO')
    display_access = get_initialized_display()

    key1 = 5
    key2 = 6
    key3 = 13
    key4 = 19

    rpi_gpio_import.setmode(rpi_gpio_import.BCM)
    rpi_gpio_import.setup(key1, rpi_gpio_import.IN, pull_up_down=rpi_gpio_import.PUD_UP)
    rpi_gpio_import.setup(key2, rpi_gpio_import.IN, pull_up_down=rpi_gpio_import.PUD_UP)
    rpi_gpio_import.setup(key3, rpi_gpio_import.IN, pull_up_down=rpi_gpio_import.PUD_UP)
    rpi_gpio_import.setup(key4, rpi_gpio_import.IN, pull_up_down=rpi_gpio_import.PUD_UP)

    display_access.display_message(get_start_message())
    while True:
        key1state = rpi_gpio_import.input(key1)
        key2state = rpi_gpio_import.input(key2)
        key3state = rpi_gpio_import.input(key3)
        key4state = rpi_gpio_import.input(key4)

        if not key1state:
            display_access.display_message("Starting MTR\n\nPlease Wait ...")
            cli_results = subprocess.check_output(mtr_cli_command, shell=True)
            if str(cli_results)[-45:-41] != "Loss":
                message = "MTR Results\n" + \
                          "Sent: " + str(cli_results)[-36:-30] + "\n" + \
                          "Loss: " + str(cli_results)[-45:-38] + "\n" + \
                          "Avg: " + str(cli_results)[-26:-20] + "ms\n" + \
                          "Worst: " + str(cli_results)[-12:-8] + "ms\n" + \
                          "Best: " + str(cli_results)[-19:-14] + "ms\n" + \
                          "Last: " + str(cli_results)[-31:-26] + "ms\n" + \
                          "StDev: " + str(cli_results)[-6:-3] + " ms\n\n" + \
                          "  Day/Month/Year\n\n" + \
                          "Date: " + str(strftime("%d/%m/%y")) + "\n" + \
                          "Time: " + str(strftime("%H:%M"))
                display_access.display_message(message)
            else:
                display_access.display_message("MTR Failed\n" +
                                               "Remote Unit Offline?\n" +
                                               "  Or\n" +
                                               "Bad Network\n\n" +
                                               "  Day/Month/Year\n\n" +
                                               "Date: " + str(strftime("%d/%m/%y")) + "\n" +
                                               "Time: " + str(strftime("%H:%M")))

        elif not key2state:
            display_access.display_message("Starting iPerf\n\n" +
                                           "Please Wait ...")
            try:
                cli_results = subprocess.check_output(iperf_cli_command, shell=True)
                message = "iPerf3 Results\n" + \
                          "Max device Bandwidth:\n" + \
                          "  220Mbps-230Mbps\n\n" + \
                          "Transferred:\n  " + \
                          str(cli_results)[-71:-57] + "\n" + \
                          "Bandwidth:\n  " + \
                          str(cli_results)[-58:-42] + "\n" + \
                          "Over " + str(cli_results)[-83:-70] + "\n\n" + \
                          "  Day/Month/Year\n\n" + \
                          "Date: " + str(strftime("%d/%m/%y")) + "\n" + \
                          "Time: " + str(strftime("%H:%M"))
                display_access.display_message(message)
            except Exception as error:
                print(str(error))
                display_access.display_message("iPerf3 Failed\n" +
                                               "Remote Unit Offline?\n" +
                                               "  Or\n" +
                                               "Bad Network\n\n" +
                                               "  Day/Month/Year\n\n" +
                                               "Date: " + str(strftime("%d/%m/%y")) + "\n" +
                                               "Time: " + str(strftime("%H:%M")))

        elif not key3state:
            try:
                socket_connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                socket_connection.connect(server_address)
                display_access.display_message("Shutting Down\n" +
                                               "Remote Unit\n\n" +
                                               "  Day/Month/Year\n\n" +
                                               "Date: " + str(strftime("%d/%m/%y")) + "\n" +
                                               "Time: " + str(strftime("%H:%M")))
            except Exception as error:
                print(str(error))
                display_access.display_message("Shut Down Failed\n" +
                                               "Remote Unit Offline\n\n" +
                                               "  Day/Month/Year\n\n" +
                                               "Date: " + str(strftime("%d/%m/%y")) + "\n" +
                                               "Time: " + str(strftime("%H:%M")))

        elif not key4state:
            try:
                display_access.display_message("Shutting Down\n" +
                                               "Local Unit\n\n" +
                                               "  Day/Month/Year\n\n" +
                                               "Date: " + str(strftime("%d/%m/%y")) + "\n" +
                                               "Time: " + str(strftime("%H:%M")))
                os.system("shutdown now -h")
            except Exception as error:
                print(str(error))
                display_access.display_message("Local Shut Down Failed?\n\n" +
                                               "  Day/Month/Year\n\n" +
                                               "Date: " + str(strftime("%d/%m/%y")) + "\n" +
                                               "Time: " + str(strftime("%H:%M")))

        sleep(1)


def get_initialized_display():
    waveshare_2_7_e_paper = __import__('supported_displays.waveshare_2_7_e_paper')
    if config_pi.installed_displays["WaveShare27"]:
        return waveshare_2_7_e_paper.CreateWaveShare27EPaper()
    return save_to_file.CreateSaveToFileDisplay()


def get_start_message():
    start_message = "Device Ready\n\nBe sure to\nGive 15 Seconds\nFor Remote\nDevice to boot\n\n" + \
                    "  Day/Month/Year\n\nDate: " + str(strftime("%d/%m/%y")) + "\nTime: " + str(strftime("%H:%M"))

    return start_message
