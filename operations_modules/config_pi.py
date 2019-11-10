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
from platform import system
from operations_modules import file_locations
from operations_modules.app_generic_functions import get_file_content, write_file_to_disk


class CreateConfiguration:
    def __init__(self):
        self.app_version = "0.1.2"
        self.full_system_text = system()
        print("Running on " + str(self.full_system_text))
        print("PiCheck: " + str(self.full_system_text[:12]))

        self.tests_running = False

        self.display_ip = "192.168.169.249"
        self.remote_tester_ip = "192.168.7.194"
        # self.remote_tester_ip = "192.168.169.251"
        self.iperf_port = "9000"

        self.running_on_rpi = False
        if self.full_system_text[:12] == "Raspberry Pi":
            self.running_on_rpi = True

        self.installed_displays = {"WaveShare27": 0, "SaveToFile": 0}
        self.is_iperf_server = False

        # Disabled temporarily for testing.  ReEnable!
        # self.load_config_from_file()

    def _get_config_as_str(self):
        current_config_str = "Kootnet Ethernet Testers Configuration - Enable = 1 & Disable = 0\n" + \
                             str(self.display_ip) + " = Display Unit IP\n" + \
                             str(self.remote_tester_ip) + " = Test Server IP\n" + \
                             str(self.installed_displays["WaveShare27"]) + " = WaveShare 2.7 Inch E-Paper\n" + \
                             str(self.installed_displays["SaveToFile"]) + " = Save to File (Web View)\n" + \
                             str(self.iperf_port) + " = iPerf Port #"

        return current_config_str

    def load_config_from_file(self):
        """ Writes provided configuration file to local disk. The provided configuration can be string or object. """
        if os.path.isfile(file_locations.config_file_location):
            try:
                config_file_lines = get_file_content(file_locations.config_file_location).split("\n")
                config_list = []
                for line in config_file_lines:
                    config_list.append(line.split("=")[0].strip())

                self.display_ip = config_list[1]
                self.remote_tester_ip = config_list[2]
                self.iperf_port = config_list[5]
            except Exception as error:
                print("Unable to load Configuration File: " + str(error))
        else:
            print("No Configuration file found, saving default")
            self.write_config_to_file()

    def write_config_to_file(self):
        """ Writes provided configuration file to local disk. The provided configuration can be string or object. """
        write_file_to_disk(file_locations.config_file_location, self._get_config_as_str())


current_config = CreateConfiguration()
