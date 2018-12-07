"""
    KootNet Network Testers is a programs to test a Network Connection
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
from time import sleep, strftime

import RPi.GPIO as GPIO

import epsimplelib

mtr_cli_command = "mtr -c 10 -r -n 192.168.169.251 > /home/pi/MTR_Results.txt"
iperf_cli_command = "iperf3 -c 192.168.169.251 -O 1 -p 9000 > /home/pi/iperf_Results.txt"
start_message = "Device Ready\n\n" + \
                "Be sure to\n" + \
                "Give 15 Seconds\n" + \
                "For Remote\n" + \
                "Device to boot\n" + \
                "Time: " + str(strftime("%H:%M"))


def esp_message(display_message):
    esp.add_text((1, 1), display_message)
    esp.update_screen()
    print(display_message)


def run_cli_command(command):
    os.system(command)


def get_text_file_content(file_location):
    local_file = open(file_location, "r")
    return local_file.read()


key1 = 5
key2 = 6
key3 = 13
key4 = 19

GPIO.setmode(GPIO.BCM)
GPIO.setup(key1, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(key2, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(key3, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(key4, GPIO.IN, pull_up_down=GPIO.PUD_UP)
esp = epsimplelib.EPScreen("portrait")  # eps = e-Ink Paper Screen

esp_message(start_message)

while True:
    key1state = GPIO.input(key1)
    key2state = GPIO.input(key2)
    key3state = GPIO.input(key3)
    key4state = GPIO.input(key4)

    if not key1state:
        print("Key1 Pressed")
        esp_message("Starting MTR\nPlease Wait ...")
        try:
            run_cli_command(mtr_cli_command)
            cli_results = get_text_file_content("/home/pi/MTR_Results.txt")
            message = "MTR Results\n" + \
                      "Sent: " + str(cli_results)[-34:-30] + "\n" + \
                      "Loss: " + str(cli_results)[-43:-35] + "\n" + \
                      "Avg: " + str(cli_results)[-23:-18] + "ms" + "\n" + \
                      "Worst: " + str(cli_results)[-10:-6] + "ms" + "\n" + \
                      "Best: " + str(cli_results)[-17:-12] + "ms" + "\n" + \
                      "Last: " + str(cli_results)[-29:-24] + "ms" + "\n" + \
                      "StDev: " + str(cli_results)[-5:-1] + "ms" + "\n\n" + \
                      " Day/Month/Year" + "\n\n" + \
                      "Date: " + str(strftime("%d/%m/%y")) + "\n" + \
                      "Time: " + str(strftime("%H:%M"))
            esp_message(message)
        except ConnectionError:
            esp_message("MTR Failed\nUnit Offline?\nTime: " + str(strftime("%H:%M")))
        else:
            esp_message("Unknown Error")

    elif not key2state:
        print("Key2 Pressed")
        esp_message("Starting iPerf\nPlease Wait ...")
        try:
            cli_results = get_text_file_content("/home/pi/iperf_Results.txt")
            message = "iPerf3 Results\n" + \
                      "Max device\n" + \
                      "Bandwidth\n" + \
                      " 220Mbps-230Mbps\n\n" + \
                      "Transferred:\n" + \
                      str(cli_results)[-68:-55] + "\n" + \
                      "Bandwidth:\n" + \
                      str(cli_results)[-55:-40] + "\n" + \
                      "Over " + str(cli_results)[-79:-68] + "\n\n" + \
                      " Day/Month/Year" + "\n" + \
                      "Date: " + str(strftime("%d/%m/%y")) + "\n" + \
                      "Time: " + str(strftime("%H:%M"))
            esp_message(message)
        except ConnectionError:
            esp_message("iPerf3 Failed\nUnit Offline?\nTime: " + str(strftime("%H:%M")))
        else:
            esp_message("Unknown Error")

    elif not key3state:
        print("Key3 Pressed")
        server_address = ('192.168.169.251', 10062)
        try:
            sockG = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sockG.connect(server_address)
            esp_message("Shutting Down\nRemote Unit\nTime: " + str(strftime("%H:%M")))
        except Exception as error:
            esp_message("Shut Down Failed\nRemote N/A\nOffline : " + str(strftime("%H:%M")))
            print(str(error))

    elif not key4state:
        print("Key4 Pressed")
        try:
            esp_message("Shutting Down\nLocal Unit\nTime: " + str(strftime("%H:%M")))
            os.system("shutdown now -h")
        except Exception as error:
            esp_message("Shut Down Failed?\nTime: " + str(strftime("%H:%M")))
            print(str(error))

    sleep(1)
