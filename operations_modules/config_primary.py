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
from operations_modules import file_locations
from operations_modules.app_generic_functions import get_file_content, write_file_to_disk, get_raspberry_pi_model


class CreateConfiguration:
    def __init__(self):
        self.app_version = "0.1.22"
        self.full_system_text = get_raspberry_pi_model()
        print("Running on " + str(self.full_system_text))
        self.running_on_rpi = False
        if self.full_system_text[:12] == "Raspberry Pi":
            self.running_on_rpi = True

        self.is_iperf_server = 0
        self.tests_running = False

        self.display_ip = "192.168.169.249"
        self.remote_tester_ip = "192.168.7.194"  # "192.168.169.251"
        self.iperf_port = "9000"
        self.mtr_run_count = "10"

        self.has_hardware_interactive = False
        self.has_hardware_display = False
        self.installed_interactive_hw = {"WaveShare27": 0}

        self.load_config_from_file()

    def get_mtr_command_str(self):
        return "mtr -c " + self.mtr_run_count + " -r -n " + self.remote_tester_ip

    def get_iperf_command_str(self):
        return "iperf3 -c " + self.remote_tester_ip + " -O 1 -p " + self.iperf_port

    def load_config_from_file(self):
        """ Writes provided configuration file to local disk. The provided configuration can be string or object. """
        if os.path.isfile(file_locations.config_file_location):
            try:
                config_file_lines = get_file_content(file_locations.config_file_location).split("\n")
                config_list = []
                for line in config_file_lines:
                    config_list.append(line.split("=")[0].strip())

                try:
                    self.is_iperf_server = int(config_list[1])
                except Exception as error:
                    print("Error loading iPerf 3 config setting: " + str(error))
                    self.is_iperf_server = 0

                self.display_ip = config_list[2]
                self.remote_tester_ip = config_list[3]
                self.iperf_port = config_list[4]
                self.mtr_run_count = config_list[5]

                try:
                    self.installed_interactive_hw["WaveShare27"] = int(config_list[6])
                except Exception as error:
                    print("Error loading WaveShare27 Installed config setting: " + str(error))
                    self.installed_interactive_hw["WaveShare27"] = 0
                for hardware in self.installed_interactive_hw:
                    if hardware:
                        self.has_hardware_interactive = True
            except Exception as error:
                print("Unable to load Configuration File: " + str(error))
        else:
            print("No Configuration file found, saving default")
            self.write_config_to_file()

    def write_config_to_file(self):
        """ Writes provided configuration file to local disk. The provided configuration can be string or object. """
        write_file_to_disk(file_locations.config_file_location, self._get_config_as_str())

    def _get_config_as_str(self):
        return_config = "Kootnet Ethernet Testers - Ver." + self.app_version + " - Enable = 1 & Disable = 0\n" + \
                        str(self.is_iperf_server) + " = Start as iPerf 3 Server\n" + \
                        str(self.display_ip) + " = Display/Interactive Unit IP\n" + \
                        str(self.remote_tester_ip) + " = Test Server IP\n" + \
                        str(self.iperf_port) + " = iPerf Server Port\n" + \
                        str(self.mtr_run_count) + " = Number of MTR Runs\n" + \
                        str(self.installed_interactive_hw["WaveShare27"]) + " = WaveShare 2.7 Inch E-Paper\n"
        return return_config


current_config = CreateConfiguration()
