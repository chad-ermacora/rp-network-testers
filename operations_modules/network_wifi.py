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
from operations_modules import app_generic_functions
from operations_modules import file_locations


def get_wifi_country_code(wifi_config_lines):
    for line in wifi_config_lines:
        line_stripped = line.strip()
        if line_stripped[:8] == "country=":
            return line_stripped[8:]
    return ""


def get_wifi_ssid(wifi_config_lines):
    for line in wifi_config_lines:
        line_stripped = line.strip()
        if line_stripped[:5] == "ssid=":
            return line_stripped[6:-1]
    return ""


def get_wifi_security_type(wifi_config_lines):
    for line in wifi_config_lines:
        line_stripped = line.strip()
        if line_stripped[:9] == "key_mgmt=":
            return line_stripped[9:]
    return ""


def get_wifi_psk(wifi_config_lines):
    for line in wifi_config_lines:
        line_stripped = line.strip()
        if line_stripped[:4] == "psk=":
            return line_stripped[5:-1]


def get_wifi_config_from_file():
    """ Loads wpa_supplicant.conf from file and returns it. """
    return app_generic_functions.get_file_content(file_locations.wifi_config_file)


def write_wifi_config_to_file(config):
    """ Writes provided wpa_supplicant file to local disk. """
    app_generic_functions.write_file_to_disk(file_locations.wifi_config_file, config)
