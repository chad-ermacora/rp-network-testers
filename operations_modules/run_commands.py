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
import time
from operations_modules.config_primary import current_config
from operations_modules import file_locations
from operations_modules import app_variables
from operations_modules.app_generic_functions import get_subprocess_str_output, thread_function, \
    write_file_to_disk, send_command
from operations_modules.hardware_access import hardware_access


def run_command(command_num):
    display_msg = ""
    if command_num == 0:
        if current_config.button_function_level == 0:
            thread_function(hardware_access.display_message, args="Running MTR Test\n\nPlease Wait ...")
            start_mtr()
            display_msg = hardware_access.get_mtr_message()
        elif current_config.button_function_level == 1:
            display_msg = hardware_access.get_sys_info_message()
            print(display_msg)
        elif current_config.button_function_level == 2:
            display_msg = "Shutting Down\nRemote Server\n\nPlease Wait 15 Seconds\nBefore Powering Down ..."
            port = app_variables.flask_http_port
            send_command("http://" + current_config.remote_tester_ip + ":" + str(port) + "/Shutdown")
    elif command_num == 1:
        if current_config.button_function_level == 0:
            thread_function(hardware_access.display_message, args="Running iPerf3 Test\n\nPlease Wait ...")
            start_iperf()
            display_msg = hardware_access.get_iperf_message()
        elif current_config.button_function_level == 1:
            thread_function(os.system, args="bash " + file_locations.http_upgrade_script)
            display_msg = hardware_access.get_upgrade_message()
        elif current_config.button_function_level == 2:
            display_msg = "Shutting Down\n\nPlease Wait 15 Seconds\nBefore Powering Down ..."
            thread_function(os.system, args="sleep 4 && shutdown now")
    elif command_num == 2:
        if current_config.button_function_level == 0:
            display_msg = "Nothing Yet"
        elif current_config.button_function_level == 1:
            thread_function(os.system, args="bash " + file_locations.http_upgrade_script + " dev")
            display_msg = hardware_access.get_upgrade_message(development_upgrade=True)
        elif current_config.button_function_level == 2:
            display_msg = "Nothing Yet"
    elif command_num == 3:
        if current_config.button_function_level == 0:
            current_config.button_function_level += 1
        elif current_config.button_function_level == 1:
            current_config.button_function_level += 1
        elif current_config.button_function_level == 2:
            current_config.button_function_level = 0
        display_msg = hardware_access.get_button_functions_message(current_config.button_function_level)
    thread_function(hardware_access.display_message, args=display_msg)


def _reset_buttons_in_sec(seconds):
    current_config.button_reset_running = True
    time.sleep(seconds)
    current_config.clear_button_counts()
    current_config.button_reset_running = False


def start_all_tests():
    start_mtr()
    start_iperf()


def start_mtr():
    current_config.tests_running = True
    app_variables.previous_mtr_start_text = "Ran at " + time.strftime("%d/%m/%y - %H:%M") + "\n(DD/MM/YY - HH:MM)\n\n"
    try:
        print("\nRunning MTR CLI: " + current_config.get_mtr_command_str() + "\n")
        temp_lines = get_subprocess_str_output(current_config.get_mtr_command_str()).strip().split("\n")
        temp_lines = temp_lines[1:]
        new_str = ""
        for line in temp_lines:
            new_str += line + "\n"
        app_variables.previous_mtr_results = new_str.strip()[:-2]
        print("MTR CLI Done\n")
    except Exception as error:
        print("MTR Command Error: " + str(error))
        temp_lines = []
    if len(temp_lines) < 3:
        app_variables.previous_mtr_results = "Error Connecting to Remote Test Server"
    current_config.tests_running = False
    save_mtr_results_to_file()


def start_iperf():
    current_config.tests_running = True
    app_variables.previous_iperf_start_text = "Ran at " + time.strftime("%d/%m/%y - %H:%M") + "\n(DD/MM/YY - HH:MM)\n\n"
    try:
        print("\nRunning iPerf 3 CLI: " + current_config.get_iperf_command_str())
        raw_iperf = get_subprocess_str_output(current_config.get_iperf_command_str())[2:-2]
        app_variables.previous_iperf_results = raw_iperf
        print("iPerf 3 CLI Done\n")
    except Exception as error:
        print("iPerf Command Error: " + str(error))
        app_variables.previous_iperf_results = "Error Connecting to Remote Test Server"
    current_config.tests_running = False
    save_iperf_results_to_file()


def save_mtr_results_to_file():
    text_time_sec = str(time.time()).split(".")[0]
    new_file_location = file_locations.location_save_report_folder + "/mtr-" + text_time_sec + ".txt"
    file_content = app_variables.previous_mtr_start_text + app_variables.previous_mtr_results
    write_file_to_disk(new_file_location, file_content)


def save_iperf_results_to_file():
    text_time_sec = str(time.time()).split(".")[0]
    new_file_location = file_locations.location_save_report_folder + "/iperf-" + text_time_sec + ".txt"
    file_content = app_variables.previous_iperf_start_text + app_variables.previous_iperf_results
    write_file_to_disk(new_file_location, file_content)
