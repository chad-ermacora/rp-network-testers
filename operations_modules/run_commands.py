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
from operations_modules.config_primary import current_config
from operations_modules.app_generic_functions import get_subprocess_str_output, thread_function
from operations_modules import app_variables, save_to_file
from operations_modules.hardware_access import hardware_access


def run_command(command_num):
    if command_num == 0:
        _start_mtr()
    elif command_num == 1:
        _start_iperf()
    elif command_num == 2:
        pass
    elif command_num == 3:
        pass


def start_all_tests():
    _start_mtr()
    _start_iperf()


def _start_mtr():
    current_config.tests_running = True
    try:
        print("MTR Command Line: " + current_config.get_mtr_command_str() + "\n")
        thread_function(hardware_access.display_message("Starting MTR Test\n\nPlease Wait ..."))
        temp_lines = get_subprocess_str_output(current_config.get_mtr_command_str()).strip().split("\n")
        temp_lines = temp_lines[1:]
        new_str = ""
        for line in temp_lines:
            new_str += line + "\n"
        app_variables.raw_previous_mtr = new_str.strip()[:-2]
    except Exception as error:
        print("MTR Command Error: " + str(error))
    current_config.tests_running = False
    save_to_file.save_mtr_results_to_file()
    hardware_access.display_message(hardware_access.get_mtr_message(app_variables.raw_previous_mtr))


def _start_iperf():
    current_config.tests_running = True
    try:
        print("iPerf 3 Command Line: " + current_config.get_iperf_command_str() + "\n")
        thread_function(hardware_access.display_message("Starting iPerf3 Test\n\nPlease Wait ..."))
        app_variables.raw_previous_iperf = get_subprocess_str_output(current_config.get_iperf_command_str())[2:-2]
    except Exception as error:
        print("iPerf Command Error: " + str(error))
    current_config.tests_running = False
    save_to_file.save_iperf_results_to_file()
    hardware_access.display_message(hardware_access.get_iperf_message(app_variables.raw_previous_iperf))
