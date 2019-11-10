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
from flask import Blueprint, render_template, send_file
from operations_modules import file_locations
from operations_modules import app_generic_functions
from operations_modules import app_variables
from operations_modules.config_pi import current_config

mtr_cli_command = "mtr -c 10 -r -n " + current_config.remote_tester_ip
iperf_cli_command = "iperf3 -c " + current_config.remote_tester_ip + " -O 1 -p " + current_config.iperf_port

http_routes = Blueprint("http_routes", __name__)


@http_routes.route("/")
@http_routes.route("/index.html")
def html_root():
    results_mtr = ""
    results_iperf = ""
    if app_variables.raw_previous_iperf and app_variables.raw_previous_mtr:
        results_mtr = app_variables.raw_previous_mtr
        results_iperf = app_variables.raw_previous_iperf

    tests_running_msg = ""
    button_disabled = ""
    if current_config.tests_running:
        tests_running_msg = "Running Tests Please Wait ..."
        button_disabled = "disabled"
    return render_template("index.html",
                           TestsRunning=tests_running_msg,
                           DisabledButton=button_disabled,
                           OSVersion=app_generic_functions.get_os_name_version(),
                           KootnetVersion=current_config.app_version,
                           Results_MTR=results_mtr,
                           Results_iPerf=results_iperf)


@http_routes.route("/mui.min.css")
def mui_min_css():
    return send_file(file_locations.mui_min_css)


@http_routes.route("/mui.min.js")
def mui_min_js():
    return send_file(file_locations.mui_min_js)


@http_routes.route("/mui-colors.min.css")
def mui_colors_min_css():
    return send_file(file_locations.mui_colors_min_css)


@http_routes.route("/StartTests", methods=["POST"])
def start_tests():
    if current_config.is_iperf_server:
        app_generic_functions.send_command("https://" + current_config.display_ip + "/StartTests")
        return render_template("message_return.html",
                               URL="https://" + current_config.display_ip,
                               TextMessage="Re-Directing to Display Server")
    else:
        app_generic_functions.thread_function(_run_tests)
    return html_root()


def _run_tests():
    current_config.tests_running = True
    try:
        print(mtr_cli_command)
        app_variables.raw_previous_mtr = app_generic_functions.get_subprocess_str_output(mtr_cli_command)[2:-2]
    except Exception as error:
        print(str(error))
    try:
        print(iperf_cli_command)
        app_variables.raw_previous_iperf = app_generic_functions.get_subprocess_str_output(iperf_cli_command)[2:-2]
    except Exception as error:
        print(str(error))
    current_config.tests_running = False
