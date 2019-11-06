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
import time
from operations_modules.config_pi import current_config


class CreateSaveToFileDisplay:
    def __init__(self):
        pass

    @staticmethod
    def display_message(text_message):
        print(text_message)
        text_time_sec = str(time.time()).split(".")[0]
        new_file_location = current_config.script_folder_path + "/kootnet_ethernet_results-" + text_time_sec + ".txt"
        with open(new_file_location, "w") as open_file:
            open_file.write(text_message)

    @staticmethod
    def get_start_message():
        start_message = "Device Ready Be sure to Give 15 Seconds For Remote Device to boot.\n" + \
                        "Date - Day/Month/Year: " + str(time.strftime("%d/%m/%y")) + "\n" + \
                        "Time: " + str(time.strftime("%H:%M"))
        return start_message

    @staticmethod
    def get_mtr_message(cli_results):
        return cli_results

    @staticmethod
    def get_iperf_message(cli_results, cli_ok=True):
        return cli_results

    @staticmethod
    def shutdown_remote_unit_message(cli_ok):
        if cli_ok:
            message = "Shutting Down Remote Unit\n" + \
                      "Date - Day/Month/Year: " + str(time.strftime("%d/%m/%y")) + "\n" + \
                      "Time: " + str(time.strftime("%H:%M"))
        else:

            message = "ShutDown Failed on Remote Unit\n" + \
                      "Date - Day/Month/Year: " + str(time.strftime("%d/%m/%y")) + "\n" + \
                      "Time: " + str(time.strftime("%H:%M"))
        return message

    @staticmethod
    def shutdown_local_unit_message():
        message = "Shutting Down Local Unit\n" + \
                  "Date -  Day/Month/Year: " + str(time.strftime("%d/%m/%y")) + "\n" + \
                  "Time: " + str(time.strftime("%H:%M"))
        return message
