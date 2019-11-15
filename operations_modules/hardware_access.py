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


def _get_initialized_display():
    driver_import = None
    if current_config.running_on_rpi:
        if current_config.installed_interactive_hw["WaveShare27"]:
            driver_import = __import__('supported_hardware.waveshare_2_7_e_paper', fromlist=["CreateHardwareAccess"])
    if driver_import is None:
        driver_import = __import__('operations_modules.save_to_file', fromlist=["CreateHardwareAccess"])
    return driver_import.CreateHardwareAccess()


hardware_access = _get_initialized_display()
