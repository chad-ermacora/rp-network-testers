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
import socket
from ipaddress import ip_address as _check_ip_address
from operations_modules import app_variables
from operations_modules.app_generic_functions import get_raspberry_pi_model

full_system_text = get_raspberry_pi_model()
running_on_rpi = False
if full_system_text[:12] == "Raspberry Pi":
    running_on_rpi = True


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


def get_ip_from_socket():
    """ Returns IPv4 Address as a String. """
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip_address = (s.getsockname()[0])
        s.close()
    except Exception as error:
        print("Get IP Failed: " + str(error))
        ip_address = "0.0.0.0"
    return ip_address


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


def check_html_network_settings(html_request, wireless_type=False):
    if wireless_type:
        local_ip = html_request.form.get("wifi_ip_address")
        local_subnet = html_request.form.get("wifi_ip_subnet")
        local_gateway = html_request.form.get("wifi_ip_gateway")
        local_dns1 = html_request.form.get("wifi_ip_dns1")
        local_dns2 = html_request.form.get("wifi_ip_dns2")
    else:
        local_ip = html_request.form.get("ethernet_ip_address")
        local_subnet = html_request.form.get("ethernet_ip_subnet")
        local_gateway = html_request.form.get("ethernet_ip_gateway")
        local_dns1 = html_request.form.get("ethernet_ip_dns1")
        local_dns2 = html_request.form.get("ethernet_ip_dns2")

    settings_status = True
    if not ip_address_validation_check(local_ip):
        settings_status = False
    if not _check_subnet(local_subnet):
        settings_status = False
    if local_gateway != "":
        if not ip_address_validation_check(local_gateway):
            settings_status = False
    if local_dns1 != "":
        if not ip_address_validation_check(local_dns1):
            settings_status = False
    if local_dns2 != "":
        if not ip_address_validation_check(local_dns2):
            settings_status = False
    return settings_status


def ip_address_validation_check(ip_address):
    try:
        if _check_ip_address(ip_address):
            return True
        return False
    except Exception as error:
        print(str(error))
        return False


def _check_subnet(subnet):
    subnet_ok = False
    count = 8
    while count <= 30:
        good_subnet = "/" + str(count)
        if subnet == good_subnet:
            subnet_ok = True
        count += 1
    return subnet_ok
