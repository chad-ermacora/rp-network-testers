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
from operations_modules import file_locations
from operations_modules.app_generic_functions import get_file_content


# Flask HTTP Server Variables
flask_http_ip = ""
flask_http_port = 10066

# Cached results from the previous test run
previous_mtr_start_text = ""
previous_iperf_start_text = ""
previous_mtr_results = False
previous_iperf_results = False

# Monitored Thread placeholders. Replaced with class instances that have function and variables access
http_server = None
interactive_hw_server = None
iperf3_server = None

# Cached variables from disk
dhcpcd_config_file_content = ""
dhcpcd_config_file_content_template = get_file_content(file_locations.dhcpcd_config_file_template)
wpa_supplicant_file_content = ""
wpa_supplicant_file_content_template = get_file_content(file_locations.wpa_supplicant_file_template)

# Last state of Test checkboxes on the main HTML page
html_mtr_checked = "checked"
html_iperf_checked = "checked"
