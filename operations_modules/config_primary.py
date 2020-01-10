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
import shutil
from operations_modules import file_locations
from operations_modules import app_variables
from operations_modules.app_generic_functions import get_file_content, write_file_to_disk, get_raspberry_pi_model
from operations_modules import network_ip
from operations_modules import network_wifi

dhcpcd_interface_template = """

# Custom Kootnet Network Tester Addition
interface {{ Interface }}
static ip_address={{ IPAddress }}{{ Subnet }}
static routers={{ Gateway }}
static domain_name_servers={{ DNS1 }} {{ DNS2 }}
"""


class CreateConfiguration:
    def __init__(self):
        self.app_version = "1.2.0"
        self.full_system_text = get_raspberry_pi_model()
        print("\nRunning on " + str(self.full_system_text))
        self.running_on_rpi = False
        if self.full_system_text[:12] == "Raspberry Pi":
            self.running_on_rpi = True

        self.tests_running = False
        self.is_iperf_server = 1
        self.iperf_port = "9000"
        self.mtr_run_count = "10"
        self.remote_tester_ip = "8.8.8.8"

        self.local_ethernet_dhcp = 1
        self.local_ethernet_adapter_name = "eth0"
        self.local_ethernet_ip = ""
        self.local_ethernet_subnet = ""
        self.local_ethernet_gateway = ""
        self.local_ethernet_dns1 = ""
        self.local_ethernet_dns2 = ""

        self.local_wireless_dhcp = 1
        self.local_wireless_adapter_name = "wlan0"
        self.local_wireless_ip = ""
        self.local_wireless_subnet = ""
        self.local_wireless_gateway = ""
        self.local_wireless_dns1 = ""
        self.local_wireless_dns2 = ""

        self.wifi_country_code = ""
        self.wifi_ssid = ""
        self.wifi_security_type = ""
        self.wifi_pass_key = ""

        self.installed_interactive_hw = {"WaveShare27": 0}
        self.using_dummy_access = False
        self.button_function_level = 0

        self.load_config_from_file()
        self.load_installed_hardware_from_file()
        self.load_dhcpcd_conf_from_file()
        self.load_wpa_supplicant_wifi()

    def load_wpa_supplicant_wifi(self):
        try:
            app_variables.wpa_supplicant_file_content = get_file_content(file_locations.wpa_supplicant_file)
            self.wifi_country_code = network_wifi.get_wifi_country_code()
            self.wifi_ssid = network_wifi.get_wifi_ssid()
            self.wifi_security_type = network_wifi.get_wifi_security_type()
            self.wifi_pass_key = network_wifi.get_wifi_psk()
        except Exception as error:
            print("Unable to get Wireless information from wpa_supplicant.conf: " + str(error))

    def load_dhcpcd_conf_from_file(self):
        try:
            app_variables.dhcpcd_config_file_content = get_file_content(file_locations.dhcpcd_config_file)
            self.local_ethernet_dhcp = network_ip.check_for_dhcp()
            self.local_ethernet_ip = network_ip.get_dhcpcd_ip()
            self.local_ethernet_subnet = network_ip.get_subnet()
            self.local_ethernet_gateway = network_ip.get_gateway()
            self.local_ethernet_dns1 = network_ip.get_dns(dns_server=0)
            self.local_ethernet_dns2 = network_ip.get_dns(dns_server=1)

            self.local_wireless_dhcp = network_ip.check_for_dhcp(wireless=True)
            self.local_wireless_ip = network_ip.get_dhcpcd_ip(wireless=True)
            self.local_wireless_subnet = network_ip.get_subnet(wireless=True)
            self.local_wireless_gateway = network_ip.get_gateway(wireless=True)
            self.local_wireless_dns1 = network_ip.get_dns(dns_server=0, wireless=True)
            self.local_wireless_dns2 = network_ip.get_dns(dns_server=1, wireless=True)
        except Exception as error:
            print("Unable to get IP information from dhcpcd.conf: " + str(error))

    def get_mtr_command_str(self):
        return "mtr -c " + self.mtr_run_count + " -r -n " + self.remote_tester_ip

    def get_iperf_command_str(self):
        return "iperf3 -c " + self.remote_tester_ip + " -O 1 -p " + self.iperf_port

    def write_wpa_supplicant_wifi_settings_to_file(self):
        wpa_supplicant_template = app_variables.wpa_supplicant_file_content_template
        if self.wifi_security_type == "":
            wifi_security_type = ""
            wifi_template = wpa_supplicant_template.replace("{{ WirelessPSK1 }}", self.wifi_pass_key)
        else:
            wifi_security_type = "key_mgmt=None"
            wifi_template = wpa_supplicant_template.replace("{{ WirelessPSK1 }}", "")

        wifi_template = wifi_template.replace("{{ WirelessCountryCode }}", self.wifi_country_code)
        wifi_template = wifi_template.replace("{{ WirelessSSID1 }}", self.wifi_ssid)
        wifi_template = wifi_template.replace("{{ WirelessKeyMgmt1 }}", wifi_security_type)
        write_file_to_disk(file_locations.wpa_supplicant_file, wifi_template)

    def write_dhcpcd_ip_settings_to_file(self):
        dhcpcd_template = app_variables.dhcpcd_config_file_content_template

        eth_replacement_variables = []
        wlan_replacement_variables = []

        if self.is_eth_ip_settings_ok():
            eth_replacement_variables.append("eth0")
            eth_replacement_variables.append(self.local_ethernet_ip)
            eth_replacement_variables.append(self.local_ethernet_subnet)
            eth_replacement_variables.append(self.local_ethernet_gateway)
            eth_replacement_variables.append(self.local_ethernet_dns1)
            eth_replacement_variables.append(self.local_ethernet_dns2)
        else:
            eth_replacement_variables = ["", "", "", "", "", ""]

        if self.is_wlan_ip_settings_ok():
            wlan_replacement_variables.append("wlan0")
            wlan_replacement_variables.append(self.local_wireless_ip)
            wlan_replacement_variables.append(self.local_wireless_subnet)
            wlan_replacement_variables.append(self.local_wireless_gateway)
            wlan_replacement_variables.append(self.local_wireless_dns1)
            wlan_replacement_variables.append(self.local_wireless_dns2)
        else:
            wlan_replacement_variables = ["", "", "", "", "", ""]

        eth_dhcpcd_text = self.get_dhcpcd_replacement_text(eth_replacement_variables)
        wlan_dhcpcd_text = self.get_dhcpcd_replacement_text(wlan_replacement_variables)
        new_dhcpcd = dhcpcd_template.replace("{{ StaticIPSettings }}", eth_dhcpcd_text + wlan_dhcpcd_text)
        write_file_to_disk(file_locations.dhcpcd_config_file, new_dhcpcd)
        shutil.chown(file_locations.dhcpcd_config_file, "root", "netdev")
        os.chmod(file_locations.dhcpcd_config_file, 0o664)

    @staticmethod
    def get_dhcpcd_replacement_text(replacement_variables):
        """
        Takes a list [] of variables and replaces the dhcpcd_template with them one by one.
        In order it takes [interface, ip, subnet, gateway, dns1, dns2]
        """
        if replacement_variables[0] == "" or replacement_variables[1] == "":
            return ""

        dhcpcd_replacement_identifiers = ["{{ Interface }}", "{{ IPAddress }}", "{{ Subnet }}",
                                          "{{ Gateway }}", "{{ DNS1 }}", "{{ DNS2 }}"]

        new_dhcpcd_interface_replacement = dhcpcd_interface_template
        for id_text, replacement_text in zip(dhcpcd_replacement_identifiers, replacement_variables):
            new_dhcpcd_interface_replacement = new_dhcpcd_interface_replacement.replace(id_text, str(replacement_text))
        return new_dhcpcd_interface_replacement

    def is_eth_ip_settings_ok(self):
        if not self.local_ethernet_dhcp:
            for req_var in [self.local_ethernet_ip, self.local_ethernet_subnet]:
                if req_var == "":
                    return False
            return True
        return False

    def is_wlan_ip_settings_ok(self):
        if not self.local_wireless_dhcp:
            for req_var in [self.local_wireless_ip, self.local_wireless_subnet]:
                if req_var == "":
                    return False
            return True
        return False

    def load_installed_hardware_from_file(self):
        """ Loads Installed Hardware configuration from local disk. """
        if os.path.isfile(file_locations.installed_hardware_file_location):
            log_msg = "Loading Installed Hardware Configuration from: "
            print(log_msg + file_locations.installed_hardware_file_location)
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
