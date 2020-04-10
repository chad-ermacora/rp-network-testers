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
import datetime
from io import BytesIO
from zipfile import ZipInfo, ZipFile, ZIP_DEFLATED
from socket import gethostname
from flask import request, Blueprint, render_template, send_file
from operations_modules.logger import primary_logger, get_sensor_log, get_number_of_log_entries, max_log_lines_return
from operations_modules import file_locations
from operations_modules import app_generic_functions
from operations_modules import app_variables
from operations_modules import run_commands
from operations_modules.config_primary import current_config
from operations_modules.network_wifi import check_html_wifi_settings
from operations_modules.network_ip import check_html_network_settings, ip_address_validation_check, \
    get_ip_from_socket, get_dhcpcd_ip

http_routes = Blueprint("http_routes", __name__)

invalid_os_msg1 = "OS Not Supported"
invalid_os_msg2 = "Network Configuration not supported on " + current_config.full_system_text


@http_routes.route("/jquery.min.js")
def jquery_min_js():
    return send_file(file_locations.j_query_js)


@http_routes.route("/mui.min.css")
def mui_min_css():
    return send_file(file_locations.mui_min_css)


@http_routes.route("/mui.min.js")
def mui_min_js():
    return send_file(file_locations.mui_min_js)


@http_routes.route("/mui-colors.min.css")
def mui_colors_min_css():
    return send_file(file_locations.mui_colors_min_css)


@http_routes.route("/favicon.ico")
def html_icon():
    return send_file(file_locations.html_icon)


@http_routes.route("/CheckOnlineStatus")
def check_online():
    return "Online"


@http_routes.route("/Version")
def get_app_version():
    return current_config.app_version


@http_routes.route("/")
@http_routes.route("/index.html")
def html_root():
    tests_running_msg = ""
    button_disabled = ""
    if current_config.tests_running:
        tests_running_msg = "Running Tests Please Wait ..."
        button_disabled = "disabled"

    ip = current_config.remote_tester_ip
    port = app_variables.flask_http_port
    remote_tester_online_status = app_generic_functions.check_tester_online_status(ip, port)
    remote_tester_colour = "#B71C1C"
    if remote_tester_online_status == "Online":
        remote_tester_colour = "darkgreen"

    return render_template("index.html",
                           TestsRunning=tests_running_msg,
                           MTRChecked=app_variables.html_mtr_checked,
                           iPerfChecked=app_variables.html_iperf_checked,
                           DisabledButton=button_disabled,
                           RemoteTesterStatus=remote_tester_online_status,
                           RemoteTesterStatusColor=remote_tester_colour,
                           Results_MTR=app_variables.web_mtr_results,
                           Results_iPerf=app_variables.web_iperf_results,
                           ConfigurationTabs=_get_configuration_tabs(),
                           NetworkingTabs=_get_networking_tabs(),
                           AboutSystemTabs=_get_about_system_tabs())


@http_routes.route("/PreviousResults", methods=["GET", "POST"])
def previous_results():
    if request.method == "POST":
        if request.form.get("button_function"):
            button_operation = request.form.get("button_function")
            if button_operation == "next":
                app_variables.previous_result_selected += 1
                if app_variables.previous_result_selected > app_variables.previous_results_total:
                    app_variables.previous_result_selected = 1
            elif button_operation == "back":
                app_variables.previous_result_selected -= 1
                if app_variables.previous_result_selected < 1:
                    app_variables.previous_result_selected = app_variables.previous_results_total
            elif button_operation == "custom_note_number":
                custom_current_note = request.form.get("current_results_num")
                if app_variables.previous_results_total > 0:
                    app_variables.previous_result_selected = int(custom_current_note)
    app_variables.previous_result_selected_cached = app_variables.get_selected_previous_result()
    current_file_name = "None"
    if len(app_variables.previous_results_file_locations) > 0:
        current_file_name = app_variables.previous_results_file_locations[app_variables.previous_result_selected - 1]
        current_file_name = current_file_name.split("/")[-1]
    return render_template("previous_results_tab.html",
                           CurrentResultSelection=app_variables.previous_result_selected,
                           LastResultNumber=str(app_variables.previous_results_total),
                           CurrentlyDisplayedResultName=str(current_file_name),
                           DisplayedResults=app_variables.previous_result_selected_cached)


@http_routes.route("/DownloadTestResultsZip")
def download_test_results_zip():
    try:
        if len(app_variables.previous_results_file_locations) > 0:
            date_time = datetime.date.today().strftime("D%dM%mY%Y")
            return_zip_file = BytesIO()
            zip_name = "TestResults_" + gethostname() + "_" + date_time + ".zip"
            file_meta_data_list = []
            names_of_files = []
            file_to_zip = []
            file_creation_dates = []
            for file_location in app_variables.previous_results_file_locations:
                file_to_zip.append(app_generic_functions.get_file_content(file_location))
                names_of_files.append(file_location.split("/")[-1])
                file_creation_dates.append(time.localtime(os.path.getmtime(file_location)))

            for name, modification_date in zip(names_of_files, file_creation_dates):
                name_data = ZipInfo(name)
                name_data.date_time = modification_date
                name_data.compress_type = ZIP_DEFLATED
                file_meta_data_list.append(name_data)
            with ZipFile(return_zip_file, "w") as zip_file:
                for file_meta_data, file_content in zip(file_meta_data_list, file_to_zip):
                    zip_file.writestr(file_meta_data, file_content)
            return_zip_file.seek(0)
            return send_file(return_zip_file, as_attachment=True, attachment_filename=zip_name)
    except Exception as error:
        primary_logger.error("Error zipping test results: " + str(error))
    return render_template("message_return.html", URL="/", TextMessage="No Results Found")


def _get_configuration_tabs():
    iperf_server_enabled = ""
    if current_config.is_iperf_server:
        iperf_server_enabled = "checked"
    wave_share_27_enabled = ""
    if current_config.installed_interactive_hw["WaveShare27"]:
        wave_share_27_enabled = "checked"

    run_scheduled_tests_on_boot = "unchecked"
    if current_config.schedule_run_on_boot:
        run_scheduled_tests_on_boot = "checked"
    scheduled_tests_every_minutes = "unchecked"
    if current_config.schedule_run_every_minutes_enabled:
        scheduled_tests_every_minutes = "checked"
    scheduled_tests_once = "unchecked"
    if current_config.schedule_run_1_enabled:
        scheduled_tests_once = "checked"

    return render_template("configuration_tabs.html",
                           IPHostname=str(gethostname()),
                           CheckediPerfServer=iperf_server_enabled,
                           ServerIP=current_config.remote_tester_ip,
                           iPerfPort=current_config.iperf_port,
                           iPerfRunOptions=current_config.iperf_run_options,
                           MTRCount=current_config.mtr_run_count,
                           CheckedWaveShare27EInk=wave_share_27_enabled,
                           EnableScheduleSystemBootChecked=run_scheduled_tests_on_boot,
                           EnableScheduleRunEveryChecked=scheduled_tests_every_minutes,
                           ScheduleRunMinutes=((current_config.schedule_run_every_minutes % 1440) % 60),
                           ScheduleRunHours=(current_config.schedule_run_every_minutes % 1440) // 60,
                           ScheduleRunDays=current_config.schedule_run_every_minutes // 1440,
                           EnableScheduleRunOnceChecked=scheduled_tests_once,
                           ScheduleRunOnceDateTime="")


@http_routes.route("/ScheduleTests", methods=["GET", "POST"])
def scheduled_tests():
    if request.method == "POST":
        current_config.schedule_run_on_boot = 0
        if request.form.get("enable_schedule_system_boot") is not None:
            current_config.schedule_run_on_boot = 1
        if request.form.get("enable_schedule_run_every") is not None:
            current_config.schedule_run_every_minutes_enabled = 1
            temp_minutes = 0
            if int(request.form.get("schedule_run_minutes")) > 0:
                temp_minutes += int(request.form.get("schedule_run_minutes"))
            if int(request.form.get("schedule_run_hours")) > 0:
                temp_minutes += int(request.form.get("schedule_run_hours")) * 60
            if int(request.form.get("schedule_run_days")) > 0:
                temp_minutes += int(request.form.get("schedule_run_days")) * 60 * 24
            if temp_minutes < 5:
                temp_minutes = 5
            current_config.schedule_run_every_minutes = temp_minutes
        else:
            current_config.schedule_run_every_minutes_enabled = 0
        current_config.write_config_to_file()
    return html_root()


def _get_networking_tabs():
    ethernet_dhcp = ""
    if current_config.local_ethernet_dhcp:
        ethernet_dhcp = "checked"
    wireless_dhcp = ""
    if current_config.local_wireless_dhcp:
        wireless_dhcp = "checked"

    wifi_type_wpa = ""
    wifi_type_none = ""
    if current_config.wifi_security_type == "":
        wifi_type_wpa = "checked"
    else:
        wifi_type_none = "checked"

    wifi_country_code_disable = "disabled"
    if current_config.running_on_rpi:
        wifi_country_code_disable = ""

    return render_template("network_tabs.html",
                           EthernetCheckedDHCP=ethernet_dhcp,
                           EthernetIPv4Address=get_dhcpcd_ip(),
                           EthernetIPv4Subnet=current_config.local_ethernet_subnet,
                           EthernetIPGateway=current_config.local_ethernet_gateway,
                           EthernetIPDNS1=current_config.local_ethernet_dns1,
                           EthernetIPDNS2=current_config.local_ethernet_dns2,
                           WirelessCheckedDHCP=wireless_dhcp,
                           WifiCountryCodeDisabled=wifi_country_code_disable,
                           WirelessIPv4Address=get_dhcpcd_ip(wireless=True),
                           WirelessIPv4Subnet=current_config.local_wireless_subnet,
                           WirelessIPGateway=current_config.local_wireless_gateway,
                           WirelessIPDNS1=current_config.local_wireless_dns1,
                           WirelessIPDNS2=current_config.local_wireless_dns2,
                           WirelessCountryCode=current_config.wifi_country_code,
                           CheckedWiFiSecurityWPA1=wifi_type_wpa,
                           CheckedWiFiSecurityNone1=wifi_type_none,
                           SSID1=current_config.wifi_ssid)


def _get_about_system_tabs():
    remote_ip_and_port = current_config.remote_tester_ip + ":" + str(app_variables.flask_http_port)
    remote_ip = current_config.remote_tester_ip
    remote_port = app_variables.flask_http_port
    remote_data_command = "http://" + remote_ip + ":" + str(remote_port) + "/Version"
    remote_version = str(app_generic_functions.get_remote_data(remote_data_command))[2:-1]

    if 3 > len(remote_version) or len(remote_version) > 14:
        remote_version = "NA"

    displayed_log_lines = get_number_of_log_entries()
    if displayed_log_lines > max_log_lines_return:
        displayed_log_lines = str(max_log_lines_return)

    return render_template("about_system_tabs.html",
                           KootnetVersion=current_config.app_version,
                           OSVersion=app_generic_functions.get_os_name_version(),
                           InternetIPAddress=get_ip_from_socket(),
                           FreeDiskSpace=app_generic_functions.get_disk_free_percent(),
                           RemoteVersion=remote_version,
                           RemoteIPandPort=remote_ip_and_port,
                           NumberOfLogLines=displayed_log_lines,
                           TotalLogLines=str(get_number_of_log_entries()),
                           LogEntries=get_sensor_log())


@http_routes.route("/UpdateProgram")
def update_program():
    os.system("systemctl start KootnetTesterUpgradeOnline.service")
    return render_template("message_return.html", URL="/",
                           TextMessage="Standard Upgrade in Progress",
                           TextMessage2="Please wait ...")


@http_routes.route("/UpdateProgramDev")
def update_program_development():
    os.system("systemctl start KootnetTesterUpgradeOnlineDev.service")
    return render_template("message_return.html", URL="/",
                           TextMessage="Development Upgrade in Progress",
                           TextMessage2="Please wait ...")


@http_routes.route("/ReStart")
def restart_program():
    app_generic_functions.thread_function(os.system, args="systemctl restart KootnetNetworkTestersServer")
    return render_template("message_return.html", URL="/", TextMessage="Re-Starting Program",
                           TextMessage2="You will automatically be redirected to home in 10 seconds")


@http_routes.route("/Reboot")
def reboot_system():
    app_generic_functions.thread_function(os.system, args="sleep 5 && reboot")
    return render_template("message_return.html", URL="/", TextMessage="Rebooting in 4 Seconds",
                           TextMessage2="It may take a few minutes for the system to reboot")


@http_routes.route("/Shutdown")
def shutdown_system():
    app_generic_functions.thread_function(os.system, args="shutdown now")
    return render_template("message_return.html", URL="/", TextMessage="Shutting Down Unit",
                           TextMessage2="Please wait 15 seconds before removing power")


@http_routes.route("/StartTests", methods=["POST"])
def start_tests():
    if request.form.get("run_mtr") is not None and request.form.get("run_iperf") is not None:
        app_variables.html_mtr_checked = "checked"
        app_variables.html_iperf_checked = "checked"
        app_generic_functions.thread_function(run_commands.start_all_tests)
    elif request.form.get("run_mtr") is not None:
        app_variables.html_mtr_checked = "checked"
        app_variables.html_iperf_checked = ""
        app_generic_functions.thread_function(run_commands.start_mtr)
    elif request.form.get("run_iperf") is not None:
        app_variables.html_iperf_checked = "checked"
        app_variables.html_mtr_checked = ""
        app_generic_functions.thread_function(run_commands.start_iperf)
    return html_root()


@http_routes.route("/EditConfiguration", methods=["POST"])
def edit_configuration():
    if request.form.get("ip_hostname") is not None:
        new_hostname = request.form.get("ip_hostname")
        if app_generic_functions.hostname_is_valid(new_hostname):
            os.system("hostnamectl set-hostname " + new_hostname)

    current_config.is_iperf_server = 0
    if request.form.get("checkbox_iperf_server") is not None:
        current_config.is_iperf_server = 1

    current_config.iperf_run_options = "-O 1"
    if request.form.get("iperf_run_options") is not None:
        current_config.iperf_run_options = request.form.get("iperf_run_options").strip()

    if ip_address_validation_check(request.form.get("remote_test_server_ip")):
        current_config.remote_tester_ip = str(request.form.get("remote_test_server_ip"))
    else:
        msg1 = "Bad Remote Test Server IP"
        msg2 = "Please check the remote test server IP and try again."
        return render_template("message_return.html", URL="/", TextMessage=msg1, TextMessage2=msg2)

    if request.form.get("iperf_port") is not None:
        current_config.iperf_port = str(request.form.get("iperf_port"))
    else:
        current_config.iperf_port = "9000"

    if request.form.get("mtr_run_count") is not None:
        current_config.mtr_run_count = str(request.form.get("mtr_run_count"))
    else:
        current_config.mtr_run_count = "10"
    current_config.write_config_to_file()
    return html_root()


@http_routes.route("/EditInstalledHardware", methods=["POST"])
def edit_installed_hardware():
    if request.form.get("checkbox_waveshare_2_7_e_ink") is not None:
        current_config.installed_interactive_hw["WaveShare27"] = 1
    else:
        current_config.installed_interactive_hw["WaveShare27"] = 0
    current_config.write_installed_hardware_to_file()
    return render_template("message_return.html", URL="/", TextMessage="Installed Hardware Saved",
                           TextMessage2="Please reboot the device for settings to take effect")


@http_routes.route("/EditEthernetIPv4", methods=["POST"])
def edit_eth_ipv4_network():
    if current_config.running_on_rpi:
        message1 = "Ethernet Settings Applied"
        message2 = "You must reboot for all settings to take effect."
        if request.form.get("ethernet_ip_dhcp") is not None:
            current_config.local_ethernet_dhcp = 1
            current_config.write_dhcpcd_ip_settings_to_file()
        else:
            if check_html_network_settings(request):
                current_config.local_ethernet_dhcp = 0
                set_html_config_ipv4(request)
                current_config.write_dhcpcd_ip_settings_to_file()
            else:
                message1 = "Invalid Network Settings"
                message2 = "One or more Network settings where incorrect."
                return render_template("message_return.html", URL="/", TextMessage=message1, TextMessage2=message2)
        return render_template("message_return.html", URL="/", TextMessage=message1, TextMessage2=message2)
    second_msg = "Ethernet " + invalid_os_msg2
    return render_template("message_return.html", URL="/", TextMessage=invalid_os_msg1, TextMessage2=second_msg)


@http_routes.route("/EditWifiIPv4", methods=["POST"])
def edit_wifi_ipv4_network():
    if current_config.running_on_rpi:
        message1 = "Wireless Settings Applied"
        message2 = "You must reboot for all settings to take effect."
        if request.form.get("wifi_ip_dhcp") is not None:
            current_config.local_wireless_dhcp = 1
            current_config.write_dhcpcd_ip_settings_to_file()
        else:
            if check_html_network_settings(request, wireless_type=True):
                current_config.local_wireless_dhcp = 0
                set_html_config_ipv4(request, wireless_type=True)
                current_config.write_dhcpcd_ip_settings_to_file()
            else:
                message1 = "Invalid Network Settings"
                message2 = "One or more Network settings where incorrect."
                return render_template("message_return.html", URL="/", TextMessage=message1, TextMessage2=message2)
        return render_template("message_return.html", URL="/", TextMessage=message1, TextMessage2=message2)
    second_msg = "Wireless " + invalid_os_msg2
    return render_template("message_return.html", URL="/", TextMessage=invalid_os_msg1, TextMessage2=second_msg)


@http_routes.route("/EditWifiConnection", methods=["POST"])
def edit_wifi_connection():
    if current_config.running_on_rpi:
        if check_html_wifi_settings(request):
            message1 = "Wireless Connection Settings Applied"
            message2 = "You must reboot for all settings to take effect."
            set_html_config_wifi_connection(request)
            current_config.write_wpa_supplicant_wifi_settings_to_file()
            return render_template("message_return.html", URL="/", TextMessage=message1, TextMessage2=message2)
        else:
            message1 = "Invalid Wireless Connection Settings"
            message2 = "One or more Wireless Connection settings where incorrect."
            return render_template("message_return.html", URL="/", TextMessage=message1, TextMessage2=message2)
    second_msg = "Wireless " + invalid_os_msg2
    return render_template("message_return.html", URL="/", TextMessage=invalid_os_msg1, TextMessage2=second_msg)


def set_html_config_wifi_connection(html_request):
    primary_logger.debug("Starting HTML Wireless Configuration Update")
    current_config.wifi_country_code = html_request.form.get("country_code")
    current_config.wifi_ssid = html_request.form.get("ssid1")
    current_config.wifi_security_type = html_request.form.get("wifi_security1")
    current_config.wifi_pass_key = html_request.form.get("wifi_key1")


def set_html_config_ipv4(html_request, wireless_type=False):
    log_msg = "Starting HTML IPv4 Configuration Update for Ethernet or Wireless."
    primary_logger.debug(log_msg + " Wireless = " + str(wireless_type))
    if wireless_type:
        current_config.local_wireless_ip = html_request.form.get("wifi_ip_address")
        current_config.local_wireless_subnet = html_request.form.get("wifi_ip_subnet")
        current_config.local_wireless_gateway = html_request.form.get("wifi_ip_gateway")
        current_config.local_wireless_dns1 = html_request.form.get("wifi_ip_dns1")
        current_config.local_wireless_dns2 = html_request.form.get("wifi_ip_dns2")
    else:
        current_config.local_ethernet_ip = html_request.form.get("ethernet_ip_address")
        current_config.local_ethernet_subnet = html_request.form.get("ethernet_ip_subnet")
        current_config.local_ethernet_gateway = html_request.form.get("ethernet_ip_gateway")
        current_config.local_ethernet_dns1 = html_request.form.get("ethernet_ip_dns1")
        current_config.local_ethernet_dns2 = html_request.form.get("ethernet_ip_dns2")
