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
from operations_modules.file_locations import script_folder_path
from operations_modules import app_variables
from operations_modules.app_generic_functions import write_file_to_disk


class CreateHardwareAccess:
    def __init__(self):
        self.key_states = [True, True, True, True]

    @staticmethod
    def get_key_states():
        return [1]

    @staticmethod
    def display_message(text_message):
        print(text_message)

    @staticmethod
    def get_start_message():
        start_message = "Device Ready Be sure to Give 15 Seconds For Remote Device to boot.\n" + \
                        "Date - Day/Month/Year: " + str(time.strftime("%d/%m/%y")) + "\n" + \
                        "Time: " + str(time.strftime("%H:%M") + "\n")
        return start_message

    @staticmethod
    def get_mtr_message(cli_results):
        pass

    @staticmethod
    def get_iperf_message(cli_results, cli_ok=True):
        pass

    @staticmethod
    def shutdown_remote_unit_message(cli_ok):
        if cli_ok:
            message = "Shutting Down Remote Unit"
        else:
            message = "ShutDown Failed on Remote Unit"
        return message

    @staticmethod
    def shutdown_local_unit_message():
        return "Shutting Down Local Unit"


def save_mtr_results_to_file():
    print(app_variables.raw_previous_mtr)
    text_time_sec = str(time.time()).split(".")[0]
    new_file_location = script_folder_path + "/test_results/kootnet_ethernet_results-mtr-" + text_time_sec + ".txt"
    write_file_to_disk(new_file_location, app_variables.raw_previous_mtr)


def save_iperf_results_to_file():
    print(app_variables.raw_previous_iperf)
    text_time_sec = str(time.time()).split(".")[0]
    new_file_location = script_folder_path + "/test_results/kootnet_ethernet_results-iperf-" + text_time_sec + ".txt"
    write_file_to_disk(new_file_location, app_variables.raw_previous_iperf)
