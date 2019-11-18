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
import sys

script_folder_path = os.path.dirname(sys.argv[0])
enable_fake_hw_clock_script = script_folder_path + "/scripts/enable_fake_hw_clock.sh"
config_file_location = script_folder_path + "/config.txt"
installed_hardware_file_location = script_folder_path + "/installed_hardware.txt"
http_upgrade_script = script_folder_path + "/scripts/kootnet_testers_installer_http.sh"

dhcpcd_config_file = "/etc/dhcpcd.conf"
dhcpcd_config_file_template = script_folder_path + "/operations_modules/extras/dhcpcd_template.conf"

wifi_config_file = "/etc/wpa_supplicant/wpa_supplicant.conf"
wifi_config_file_template = script_folder_path + "/operations_modules/extras/wpa_supplicant_template.conf"

location_save_report_folder = "/home/pi"
location_truetype_font = "/usr/share/fonts/truetype/freefont/FreeSans.ttf"

# Flask HTTP files
menu_js = script_folder_path + "/operations_modules/extras/menu.js"
menu_css_style = script_folder_path + "/operations_modules/extras/style.css"
j_query_js = script_folder_path + "/operations_modules/extras/jquery-3.4.1.min.js"
mui_min_css = script_folder_path + "/operations_modules/extras/mui.min-ver-0.9.43.css"
mui_min_js = script_folder_path + "/operations_modules/extras/mui.min-ver-0.9.43.js"
mui_colors_min_css = script_folder_path + "/operations_modules/extras/mui-colors.min-ver-0.9.43.css"
