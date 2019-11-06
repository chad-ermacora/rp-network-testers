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
import subprocess
from time import sleep
from operations_modules.config_pi import current_config
from operations_modules import app_generic_functions
from operations_modules.http_server import flask_http_port
from supported_displays import save_to_file

mtr_cli_command = "mtr -c 10 -r -n " + current_config.remote_tester_ip
iperf_cli_command = "iperf3 -c " + current_config.remote_tester_ip + " -O 1 -p " + current_config.iperf_port


class CreateDisplayServer:
    def __init__(self):
        self.display_access = self.get_initialized_display()
        self.display_access.display_message(self.display_access.get_start_message())

        while True:
            count = 0
            for key_state in self.display_access.key_states:
                if not key_state:
                    self.run_command(count)
                count += 1
            sleep(1)

    @staticmethod
    def get_initialized_display():
        if current_config.installed_displays["WaveShare27"]:
            waveshare_2_7_e_paper = __import__('supported_displays.waveshare_2_7_e_paper')
            return waveshare_2_7_e_paper.CreateWaveShare27EPaper()
        return save_to_file.CreateSaveToFileDisplay()

    def run_command(self, key_pressed):
        if key_pressed == 0:
            self.display_access.display_message("Starting MTR\n\nPlease Wait ...")
            cli_results = str(subprocess.check_output(mtr_cli_command, shell=True))
            self.display_access.display_message(self.display_access.get_mtr_message(cli_results))
        elif key_pressed == 1:
            self.display_access.display_message("Starting iPerf\n\nPlease Wait ...")
            try:
                cli_results = str(subprocess.check_output(iperf_cli_command, shell=True))
                cli_command_ok = True
            except Exception as error:
                cli_results = ""
                cli_command_ok = False
                print(str(error))
            self.display_access.display_message(self.display_access.get_iperf_message(cli_results, cli_ok=cli_command_ok))
        elif key_pressed == 2:
            url = "https://" + current_config.remote_tester_ip + ":" + str(flask_http_port) + "/Shutdown"
            send_ok = app_generic_functions.send_command(url)
            self.display_access.display_message(self.display_access.shutdown_remote_unit_message(send_ok))
        elif key_pressed == 3:
            self.display_access.display_message(self.display_access.shutdown_local_unit_message())
            os.system("shutdown now -h")
