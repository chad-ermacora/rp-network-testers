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


class CreateHardwareAccess:
    def __init__(self):
        self.key_states = [True, True, True, True]

    @staticmethod
    def get_key_states():
        return [1]

    @staticmethod
    def display_message(text_message):
        pass

    @staticmethod
    def get_start_message():
        return ""

    @staticmethod
    def get_mtr_message(cli_results):
        return ""

    @staticmethod
    def get_iperf_message(cli_results, cli_ok=True):
        return ""

    @staticmethod
    def get_sys_info_message():
        return ""

    @staticmethod
    def shutdown_local_unit_message():
        print("Shutting Down Local Unit")
        return ""

# TODO Add Upgrade, Dev Upgrade, reboot, shutdown, restart service??
