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

import RPi.GPIO as GPIO
from PIL import Image, ImageDraw, ImageFont

import epd2in7

mtr_cli_command = "mtr -c 10 -r -n 192.168.169.251"
iperf_cli_command = "iperf3 -c 192.168.169.251 -O 1 -p 9000"
start_message = "Device Ready\n\n" + \
                "Be sure to\n" + \
                "Give 15 Seconds\n" + \
                "For Remote\n" + \
                "Device to boot\n\n" + \
                "  Day/Month/Year\n\n" + \
                "Date: " + str(strftime("%d/%m/%y")) + "\n" + \
                "Time: " + str(strftime("%H:%M"))


def esp_message(display_message):
    display_image = Image.new("1", (epd2in7.EPD_WIDTH, epd2in7.EPD_HEIGHT), 255)  # 255: clear the frame
    draw = ImageDraw.Draw(display_image)
    font18 = ImageFont.truetype("/usr/share/fonts/truetype/freefont/FreeSans.ttf", 16)
    draw.text((2, 0), display_message, font=font18, fill=0)
    print(display_message)
    esp.display(esp.getbuffer(display_image))


def run_cli_command(command):
    return subprocess.check_output(command, shell=True)


key1 = 5
key2 = 6
key3 = 13
key4 = 19

GPIO.setmode(GPIO.BCM)
GPIO.setup(key1, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(key2, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(key3, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(key4, GPIO.IN, pull_up_down=GPIO.PUD_UP)
esp = epd2in7.EPD()
esp.init()

esp_message(start_message)
while True:
    key1state = GPIO.input(key1)
    key2state = GPIO.input(key2)
    key3state = GPIO.input(key3)
    key4state = GPIO.input(key4)

    if not key1state:
        esp_message("Starting MTR\n\n" +
                    "Please Wait ...")
        cli_results = run_cli_command(mtr_cli_command)
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
            esp_message(message)
        else:
            esp_message("MTR Failed\n" +
                        "Remote Unit Offline?\n" +
                        "  Or\n" +
                        "Bad Network\n\n" +
                        "  Day/Month/Year\n\n" +
                        "Date: " + str(strftime("%d/%m/%y")) + "\n" +
                        "Time: " + str(strftime("%H:%M")))

    elif not key2state:
        esp_message("Starting iPerf\n\n" +
                    "Please Wait ...")
        try:
            cli_results = run_cli_command(iperf_cli_command)
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
            esp_message(message)
        except Exception as error:
            print(str(error))
            esp_message("iPerf3 Failed\n" +
                        "Remote Unit Offline?\n" +
                        "  Or\n" +
                        "Bad Network\n\n" +
                        "  Day/Month/Year\n\n" +
                        "Date: " + str(strftime("%d/%m/%y")) + "\n" +
                        "Time: " + str(strftime("%H:%M")))

    elif not key3state:
        server_address = ("192.168.169.251", 10062)
        try:
            sockG = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sockG.connect(server_address)
            esp_message("Shutting Down\n" +
                        "Remote Unit\n\n" +
                        "  Day/Month/Year\n\n" +
                        "Date: " + str(strftime("%d/%m/%y")) + "\n" +
                        "Time: " + str(strftime("%H:%M")))
        except Exception as error:
            print(str(error))
            esp_message("Shut Down Failed\n" +
                        "Remote Unit Offline\n\n" +
                        "  Day/Month/Year\n\n" +
                        "Date: " + str(strftime("%d/%m/%y")) + "\n" +
                        "Time: " + str(strftime("%H:%M")))

    elif not key4state:
        try:
            esp_message("Shutting Down\n" +
                        "Local Unit\n\n" +
                        "  Day/Month/Year\n\n" +
                        "Date: " + str(strftime("%d/%m/%y")) + "\n" +
                        "Time: " + str(strftime("%H:%M")))
            os.system("shutdown now -h")
        except Exception as error:
            print(str(error))
            esp_message("Local Shut Down Failed?\n\n" +
                        "  Day/Month/Year\n\n" +
                        "Date: " + str(strftime("%d/%m/%y")) + "\n" +
                        "Time: " + str(strftime("%H:%M")))

    sleep(1)
