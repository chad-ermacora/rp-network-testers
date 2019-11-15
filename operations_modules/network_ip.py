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
from operations_modules import file_locations
from operations_modules import app_generic_functions
from operations_modules.config_primary import current_config


def check_for_dhcp(dhcpcd_config_lines, wireless=False):
    dhcp_status = True
    for line in dhcpcd_config_lines:
        line_stripped = line.strip()
        if line_stripped[:18] == "static ip_address=":
            dhcp_status = False
    return dhcp_status


def get_dhcpcd_ip(dhcpcd_config_lines):
    for line in dhcpcd_config_lines:
        line_stripped = line.strip()
        if line_stripped[:18] == "static ip_address=":
            ip_address = line_stripped[18:].split("/")[0]
            return ip_address
    return ""


def get_gateway(dhcpcd_config_lines):
    for line in dhcpcd_config_lines:
        line_stripped = line.strip()
        if line_stripped[:15] == "static routers=":
            return line_stripped[15:]
    return ""


def get_subnet(dhcpcd_config_lines):
    for line in dhcpcd_config_lines:
        line_stripped = line.strip()
        if line_stripped[:18] == "static ip_address=":
            subnet_mask = "/" + line_stripped[18:].split("/")[1]
            return subnet_mask
    return ""


def get_dns(dhcpcd_config_lines, dns_server=0):
    for line in dhcpcd_config_lines:
        line_stripped = line.strip()
        if line_stripped[:27] == "static domain_name_servers=":
            dns_list = line_stripped[27:].split(" ")
            if len(dns_list) > 1 or dns_server == 0:
                return dns_list[dns_server]
    return ""


def get_dhcpcd_config_from_file():
    """ Loads dhcpcd.conf from file and returns it. """
    if current_config.running_on_rpi:
        return app_generic_functions.get_file_content(file_locations.dhcpcd_config_file)
    return ""


def write_ipv4_config_to_file(dhcpcd_config):
    """ Writes provided dhcpcd.conf file to local disk. """
    if current_config.running_on_rpi:
        app_generic_functions.write_file_to_disk(file_locations.dhcpcd_config_file, dhcpcd_config)
    else:
        print("Warning, IPv4 Network settings not saved: Current OS Not Supported")
