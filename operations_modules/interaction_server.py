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
from time import sleep
from operations_modules.config_primary import current_config
from operations_modules import run_commands
from operations_modules.hardware_access import hardware_access


class CreateInteractiveServer:
    def __init__(self):
        if current_config.using_dummy_access:
            print("No Interactive Hardware Detected.  Using Web Access Only.\n")
            while True:
                sleep(300)
        print("Starting Interactive Server\n")
        while True:
            if current_config.tests_running:
                sleep(1)
            count = 0
            for key_state in hardware_access.get_key_states():
                if not key_state:
                    run_commands.run_command(count)
                    break
                count += 1
            sleep(1)
