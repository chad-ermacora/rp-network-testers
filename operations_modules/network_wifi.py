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


def get_wifi_country_code():
    if running_on_rpi:
        wifi_config_lines = app_variables.wpa_supplicant_file_content.strip().split("\n")
        for line in wifi_config_lines:
            line_stripped = line.strip()
            if line_stripped[:8] == "country=":
                return line_stripped[8:]
    return ""


def get_wifi_ssid():
    if running_on_rpi:
        wifi_config_lines = app_variables.wpa_supplicant_file_content.strip().split("\n")
        for line in wifi_config_lines:
            line_stripped = line.strip()
            if line_stripped[:5] == "ssid=":
                return line_stripped[6:-1]
    return ""


def get_wifi_security_type():
    if running_on_rpi:
        wifi_config_lines = app_variables.wpa_supplicant_file_content.strip().split("\n")
        for line in wifi_config_lines:
            line_stripped = line.strip()
            if line_stripped[:13] == "key_mgmt=None":
                return "None"
    return ""


def get_wifi_psk():
    if running_on_rpi:
        wifi_config_lines = app_variables.wpa_supplicant_file_content.strip().split("\n")
        for line in wifi_config_lines:
            line_stripped = line.strip()
            if line_stripped[:4] == "psk=":
                return line_stripped[5:-1]
    return ""
