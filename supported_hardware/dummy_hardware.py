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
from operations_modules.logger import primary_logger


class CreateHardwareAccess:
    def __init__(self):
        self.key_states = [True, True, True, True]

    @staticmethod
    def get_key_states():
        return [1]

    @staticmethod
    def display_message(text_message):
        print("Display message Accessed")
        pass

    @staticmethod
    def get_button_functions_message(function_level=0):
        print("Get button functions Pressed")
        return ""

    @staticmethod
    def get_mtr_message(cli_results):
        print("Get MTR message Pressed")
        return ""

    @staticmethod
    def get_iperf_message(cli_results, cli_ok=True):
        print("Get iPerf 3 message Pressed")
        return ""

    @staticmethod
    def get_sys_info_message():
        print("System Info Pressed")
        return ""

    @staticmethod
    def get_upgrade_message(development_upgrade=False):
        if development_upgrade:
            print("Development Upgrade Started")
        else:
            print("Upgrade Started")
        return ""

    @staticmethod
    def shutdown_local_unit_message():
        print("Shutting Down Local Unit")
        return ""
