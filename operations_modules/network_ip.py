"""
    KootNet Sensors is a collection of programs and scripts to deploy,
    interact with, and collect readings from various Sensors.
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
from operations_modules import app_variables
from operations_modules.app_generic_functions import get_raspberry_pi_model

full_system_text = get_raspberry_pi_model()
running_on_rpi = False
if full_system_text[:12] == "Raspberry Pi":
    running_on_rpi = True


def get_number_of_interface_entries_dhcpcd():
    dhcpcd_content_lines = app_variables.dhcpcd_config_file_content.split("\n")
    interface_count = 0
    for line in dhcpcd_content_lines:
        if line.strip()[:9] == "interface":
            interface_count += 1
    return interface_count


def check_for_dhcp(wireless=False):
    if running_on_rpi:
        dhcpcd_content_lines = app_variables.dhcpcd_config_file_content.split("\n")
        for line in dhcpcd_content_lines:
            line_stripped = line.strip()
            if line_stripped[:9] == "interface":
                if wireless:
                    if line_stripped[9:].strip() == "wlan0":
                        return 0
                else:
                    if line_stripped[9:].strip() == "eth0":
                        return 0
    return 1


def get_dhcpcd_ip(wireless=False):
    if running_on_rpi:
        dhcpcd_content_lines = app_variables.dhcpcd_config_file_content.split("\n")
        current_interface = ""
        for line in dhcpcd_content_lines:
            line_stripped = line.strip()
            if line_stripped[:9] == "interface":
                current_interface = line_stripped[9:].strip()
            elif line_stripped[:18] == "static ip_address=":
                ip_without_subnet = line_stripped[18:].strip().split("/")[0]
                if wireless:
                    if current_interface == "wlan0":
                        return ip_without_subnet
                else:
                    if current_interface == "eth0":
                        return ip_without_subnet
    return ""


def get_subnet(wireless=False):
    if running_on_rpi:
        dhcpcd_content_lines = app_variables.dhcpcd_config_file_content.split("\n")
        current_interface = ""
        for line in dhcpcd_content_lines:
            line_stripped = line.strip()
            if line_stripped[:9] == "interface":
                current_interface = line_stripped[9:].strip()
            elif line_stripped[:18] == "static ip_address=":
                if wireless:
                    if current_interface == "wlan0":
                        return "/" + line_stripped[18:].split("/")[1].strip()
                else:
                    if current_interface == "eth0":
                        return "/" + line_stripped[18:].split("/")[1].strip()
    return ""


def get_gateway(wireless=False):
    if running_on_rpi:
        dhcpcd_content_lines = app_variables.dhcpcd_config_file_content.split("\n")
        current_interface = ""
        for line in dhcpcd_content_lines:
            line_stripped = line.strip()
            if line_stripped[:9] == "interface":
                current_interface = line_stripped[9:].strip()
            elif line_stripped[:15] == "static routers=":
                if wireless:
                    if current_interface == "wlan0":
                        return line_stripped[15:].strip()
                else:
                    if current_interface == "eth0":
                        return line_stripped[15:].strip()
    return ""


def get_dns(dns_server=0, wireless=False):
    if running_on_rpi:
        dhcpcd_content_lines = app_variables.dhcpcd_config_file_content.split("\n")
        current_interface = ""
        for line in dhcpcd_content_lines:
            line_stripped = line.strip()
            if line_stripped[:9] == "interface":
                current_interface = line_stripped[9:].strip()
            elif line_stripped[:27] == "static domain_name_servers=":
                dns_list = line_stripped[27:].split(" ")
                if wireless:
                    if current_interface == "wlan0":
                        if len(dns_list) > 1 or dns_server == 0:
                            return dns_list[dns_server]
                else:
                    if current_interface == "eth0":
                        if len(dns_list) > 1 or dns_server == 0:
                            return dns_list[dns_server]
    return ""
