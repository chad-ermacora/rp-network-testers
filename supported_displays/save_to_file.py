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
import time

save_to_file_location = "/home/pi/kootnet_ethernet_results-"


class CreateSaveToFileDisplay:
    def __init__(self):
        pass

    @staticmethod
    def display_message(text_message):
        print(text_message)
        text_time_sec = str(time.time()).split(".")[0]
        new_file_location = save_to_file_location + text_time_sec + ".txt"
        with open(new_file_location, "w") as open_file:
            open_file.write(text_message)
