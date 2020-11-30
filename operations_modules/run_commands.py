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
from operations_modules.logger import primary_logger
from operations_modules.config_primary import current_config
from operations_modules import file_locations
from operations_modules import app_variables
from operations_modules.app_generic_functions import get_subprocess_str_output, thread_function, \
    write_file_to_disk, send_command
from operations_modules.hardware_access import hardware_access


def run_command(command_num):
    if hardware_access.display_in_use:
        primary_logger.debug("Display In Use, skipping Command.  Try again in a few seconds.")
    else:
        display_msg = ""
        if command_num == 0:
            if current_config.button_function_level == 0:
                thread_function(hardware_access.display_message, args="Running MTR Test\n\nPlease Wait ...")
                start_mtr()
                display_msg = hardware_access.get_mtr_message()
            elif current_config.button_function_level == 1:
                display_msg = hardware_access.get_sys_info_message()
                primary_logger.debug(display_msg)
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
                os.system("systemctl start KootnetTesterUpgradeOnline.service")
                display_msg = hardware_access.get_upgrade_message()
            elif current_config.button_function_level == 2:
                display_msg = "Shutting Down\n\nPlease Wait 15 Seconds\nBefore Powering Down ..."
                thread_function(os.system, args="sleep 4 && shutdown now")
        elif command_num == 2:
            if current_config.button_function_level == 0:
                display_msg = "Nothing Yet"
            elif current_config.button_function_level == 1:
                os.system("systemctl start KootnetTesterUpgradeOnlineDev.service")
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
    if not current_config.mtr_running:
        current_config.mtr_running = True
        mtr_text_results = "Ran at " + time.strftime("%d/%m/%y - %H:%M") + "\n(DD/MM/YY - HH:MM)\n\n" + \
                           current_config.get_mtr_command_str() + "\n\n"
        try:
            primary_logger.info("Starting MTR Test: " + current_config.get_mtr_command_str())
            temp_lines = get_subprocess_str_output(current_config.get_mtr_command_str()).strip().split("\n")
            temp_lines = temp_lines[1:]
            new_str = ""
            for line in temp_lines:
                new_str += line + "\n"
            mtr_text_results += new_str.strip()[:-2]
            app_variables.raw_mtr_results = new_str.strip()[:-2]
            primary_logger.info("MTR Test Complete")
        except Exception as error:
            primary_logger.error("MTR Command Error: " + str(error))
            mtr_text_results += "Error Connecting to Remote Test Server"
            app_variables.raw_mtr_results = "Error Connecting to Remote Test Server"
        app_variables.web_mtr_results = mtr_text_results
        current_config.mtr_running = False
        save_mtr_results_to_file()


def start_iperf():
    if not current_config.iperf_running:
        current_config.iperf_running = True
        iperf_text_results = "Ran at " + time.strftime("%d/%m/%y - %H:%M") + "\n(DD/MM/YY - HH:MM)\n\n" + \
                             current_config.get_iperf_command_str() + "\n\n"
        try:
            primary_logger.info("Starting iPerf 3 Test: " + current_config.get_iperf_command_str())
            temp_results_text = get_subprocess_str_output(current_config.get_iperf_command_str())[2:-2]
            iperf_text_results += temp_results_text
            app_variables.raw_iperf_results = temp_results_text
            primary_logger.info("iPerf 3 Test Complete")
        except Exception as error:
            primary_logger.error("iPerf Command Error: " + str(error))
            iperf_text_results += "Error Connecting to Remote Test Server"
            app_variables.raw_iperf_results = "Error Connecting to Remote Test Server"
        current_config.iperf_running = False
        app_variables.web_iperf_results = iperf_text_results
        save_iperf_results_to_file()


def save_mtr_results_to_file():
    primary_logger.info("Saving MTR test results to file")
    try:
        text_time_sec = str(time.time()).split(".")[0]
        new_file_location = file_locations.location_save_report_folder + "/mtr-" + text_time_sec + ".txt"
        write_file_to_disk(new_file_location, app_variables.web_mtr_results)
        app_variables.previous_mtr_results_file_locations = app_variables.get_previous_results_file_names()
        app_variables.previous_mtr_results_total = len(app_variables.previous_mtr_results_file_locations)
    except Exception as error:
        primary_logger.error("Error saving MTR test results to file: " + str(error))


def save_iperf_results_to_file():
    primary_logger.info("Saving iPerf 3 test results to file")
    try:
        text_time_sec = str(time.time()).split(".")[0]
        new_file_location = file_locations.location_save_report_folder + "/iperf-" + text_time_sec + ".txt"
        write_file_to_disk(new_file_location, app_variables.web_iperf_results)
        app_variables.previous_iperf_results_file_locations = app_variables.get_previous_results_file_names(test_type="iperf")
        app_variables.previous_iperf_results_total = len(app_variables.previous_iperf_results_file_locations)
    except Exception as error:
        primary_logger.error("Error saving iPerf 3 test results to file: " + str(error))
