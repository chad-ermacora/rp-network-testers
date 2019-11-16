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
        self.app_version = "0.1.54"
        self.full_system_text = get_raspberry_pi_model()
        print("\nRunning on " + str(self.full_system_text))
        self.running_on_rpi = False
        if self.full_system_text[:12] == "Raspberry Pi":
            self.running_on_rpi = True

        self.tests_running = False
        self.is_iperf_server = 0
        self.iperf_port = "9000"
        self.mtr_run_count = "10"
        self.remote_tester_ip = "192.168.7.194"  # "192.168.169.251"

        self.local_ethernet_dhcp = True
        self.local_ethernet_adapter_name = "eth0"
        self.local_ethernet_ip = ""
        self.local_ethernet_subnet = ""
        self.local_ethernet_gateway = ""
        self.local_ethernet_dns1 = ""
        self.local_ethernet_dns2 = ""

        self.local_wireless_dhcp = True
        self.local_wireless_adapter_name = "wlan0"
        self.local_wireless_ip = ""
        self.local_wireless_subnet = ""
        self.local_wireless_gateway = ""
        self.local_wireless_dns1 = ""
        self.local_wireless_dns2 = ""

        # Holds how many times the corresponding button has been pressed for additional actions
        self.button_1 = 0
        self.button_2 = 0
        self.button_3 = 0
        self.button_4 = 0

        self.installed_interactive_hw = {"WaveShare27": 0}
        self.using_dummy_access = False

        self.load_config_from_file()
        self.load_installed_hardware_from_file()

    def clear_button_counts(self, exception_button=100):
        if exception_button != 0:
            self.button_1 = 0
        if exception_button != 1:
            self.button_2 = 0
        if exception_button != 2:
            self.button_3 = 0
        if exception_button != 3:
            self.button_4 = 0

    def get_mtr_command_str(self):
        return "mtr -c " + self.mtr_run_count + " -r -n " + self.remote_tester_ip

    def get_iperf_command_str(self):
        return "iperf3 -c " + self.remote_tester_ip + " -O 1 -p " + self.iperf_port

    def load_installed_hardware_from_file(self):
        """ Loads Installed Hardware configuration from local disk. """
        if os.path.isfile(file_locations.installed_hardware_file_location):
            log_msg = "Loading Installed Hardware Configuration from: "
            print(log_msg + file_locations.installed_hardware_file_location + "\n")
            try:
                config_file_lines = get_file_content(file_locations.installed_hardware_file_location).split("\n")
                config_list = []
                for line in config_file_lines:
                    config_list.append(line.split("=")[0].strip())

                try:
                    self.installed_interactive_hw["WaveShare27"] = int(config_list[1])
                except Exception as error:
                    print("Error loading Installed Hardware config: " + str(error))
                    self.write_installed_hardware_to_file()
            except Exception as error:
                print("Unable to load Installed Hardware configuration File: " + str(error))
        else:
            print("No Installed Hardware Configuration file found, saving default")
            self.write_installed_hardware_to_file()

    def write_installed_hardware_to_file(self):
        """ Writes Installed Hardware config to local disk. """
        write_file_to_disk(file_locations.installed_hardware_file_location, self._get_installed_hardware_as_str())

    def _get_installed_hardware_as_str(self):
        return_config = "Kootnet Ethernet Testers - Ver." + self.app_version + " - Enable = 1 & Disable = 0\n" + \
                        str(self.installed_interactive_hw["WaveShare27"]) + " = WaveShare 2.7 Inch E-Paper\n"
        return return_config

    def load_config_from_file(self):
        """ Loads Primary configuration from local disk and set's accordingly. """
        if os.path.isfile(file_locations.config_file_location):
            print("Loading Primary Configuration from: " + file_locations.config_file_location)
            try:
                config_file_lines = get_file_content(file_locations.config_file_location).split("\n")
                config_list = []
                for line in config_file_lines:
                    config_list.append(line.split("=")[0].strip())

                try:
                    self.is_iperf_server = int(config_list[1])
                    self.remote_tester_ip = config_list[2]
                    self.iperf_port = config_list[3]
                    self.mtr_run_count = config_list[4]
                except Exception as error:
                    print("Error loading config settings.  Writing new Configuration: " + str(error))
                    self.write_config_to_file()
            except Exception as error:
                print("Unable to load Configuration File: " + str(error))
        else:
            print("No Configuration file found, saving default")
            self.write_config_to_file()

    def write_config_to_file(self):
        """ Writes configuration to local disk. """
        write_file_to_disk(file_locations.config_file_location, self._get_config_as_str())

    def _get_config_as_str(self):
        return_config = "Kootnet Ethernet Testers - Ver." + self.app_version + " - Enable = 1 & Disable = 0\n" + \
                        str(self.is_iperf_server) + " = Start iPerf 3 Server on Boot\n" + \
                        str(self.remote_tester_ip) + " = Remote Test Server IP\n" + \
                        str(self.iperf_port) + " = Local & Remote iPerf Server Port\n" + \
                        str(self.mtr_run_count) + " = Number of MTR Runs\n"
        return return_config


current_config = CreateConfiguration()
