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
from operations_modules.app_generic_functions import get_file_content


def get_previous_results_file_names():
    """ Returns a list of file locations of all previous results """
    for (root_path, directory_names, file_names) in os.walk(file_locations.location_save_report_folder):
        temp_file_locations = []
        for file_name in sorted(file_names):
            temp_file_locations.append(os.path.join(root_path, file_name))
        return temp_file_locations


def get_selected_previous_result():
    if len(previous_results_file_locations) > 0:
        return get_file_content(previous_results_file_locations[previous_result_selected - 1])
    return "No Previous Results Found"


# Flask HTTP Server Variables
flask_http_ip = ""
flask_http_port = 10066

# Cached results from last test run
web_mtr_results = ""
web_iperf_results = ""
raw_mtr_results = ""
raw_iperf_results = ""

# Previous Results variables
previous_result_selected = 1
previous_results_file_locations = get_previous_results_file_names()
previous_result_selected_cached = get_selected_previous_result()
previous_results_total = len(previous_results_file_locations)


# Monitored Thread placeholders. Replaced with class instances that have function and variables access
http_server = None
interactive_hw_server = None
iperf3_server = None
scheduled_test_run_server = None

# Cached variables from disk
dhcpcd_config_file_content = ""
dhcpcd_config_file_content_template = get_file_content(file_locations.dhcpcd_config_file_template)
wpa_supplicant_file_content = ""
wpa_supplicant_file_content_template = get_file_content(file_locations.wpa_supplicant_file_template)

# Last state of Test checkboxes on the main HTML page
html_mtr_checked = "checked"
html_iperf_checked = "checked"
