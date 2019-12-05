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
from socket import gethostname
from flask import request, Blueprint, render_template, send_file
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

    iperf_server_enabled = ""
    if current_config.is_iperf_server:
        iperf_server_enabled = "checked"
    wave_share_27_enabled = ""
    if current_config.installed_interactive_hw["WaveShare27"]:
        wave_share_27_enabled = "checked"

    ethernet_dhcp = ""
    if current_config.local_ethernet_dhcp:
        ethernet_dhcp = "checked"
    wireless_dhcp = ""
    if current_config.local_wireless_dhcp:
        wireless_dhcp = "checked"

    mtr_results = ""
    if app_variables.previous_mtr_results:
        mtr_results = app_variables.previous_mtr_start_text + str(app_variables.previous_mtr_results)
    iperf_results = ""
    if app_variables.previous_iperf_results:
        iperf_results = app_variables.previous_iperf_start_text + str(app_variables.previous_iperf_results)

    wifi_type_wpa = ""
    wifi_type_none = ""
    if current_config.wifi_security_type == "":
        wifi_type_wpa = "checked"
    else:
        wifi_type_none = "checked"

    wifi_country_code_disable = "disabled"
    if current_config.running_on_rpi:
        wifi_country_code_disable = ""

    ip = current_config.remote_tester_ip
    port = app_variables.flask_http_port
    remote_tester_online_status = app_generic_functions.check_tester_online_status(ip, port)
    remote_tester_colour = "#B71C1C"
    if remote_tester_online_status == "Online":
        remote_tester_colour = "darkgreen"

    remote_ip = current_config.remote_tester_ip
    remote_port = app_variables.flask_http_port
    remote_version = str(app_generic_functions.get_remote_data("http://" + remote_ip + ":" + str(remote_port) +
                                                               "/Version"))[2:-1]
    if 3 > len(remote_version) or len(remote_version) > 14:
        remote_version = "NA"
    return render_template("index.html",
                           RemoteIPandPort=current_config.remote_tester_ip + ":" + str(app_variables.flask_http_port),
                           RemoteVersion=remote_version,
                           TestsRunning=tests_running_msg,
                           MTRChecked=app_variables.html_mtr_checked,
                           iPerfChecked=app_variables.html_iperf_checked,
                           IPHostname=str(gethostname()),
                           DisabledButton=button_disabled,
                           OSVersion=app_generic_functions.get_os_name_version(),
                           InternetIPAddress=get_ip_from_socket(),
                           KootnetVersion=current_config.app_version,
                           FreeDiskSpace=app_generic_functions.get_disk_free_percent(),
                           RemoteTesterStatus=remote_tester_online_status,
                           RemoteTesterStatusColor=remote_tester_colour,
                           Results_MTR=mtr_results,
                           Results_iPerf=iperf_results,
                           CheckediPerfServer=iperf_server_enabled,
                           InteractiveIP=current_config.local_ethernet_ip,
                           ServerIP=current_config.remote_tester_ip,
                           iPerfPort=current_config.iperf_port,
                           MTRCount=current_config.mtr_run_count,
                           CheckedWaveShare27EInk=wave_share_27_enabled,
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


@http_routes.route("/UpdateProgram")
def update_program():
    app_generic_functions.thread_function(os.system, args="bash " + file_locations.http_upgrade_script)
    return render_template("message_return.html", URL="/",
                           TextMessage="Standard Upgrade in Progress",
                           TextMessage2="Please wait ...")


@http_routes.route("/UpdateProgramDev")
def update_program_development():
    app_generic_functions.thread_function(os.system, args="bash " + file_locations.http_upgrade_script + " dev")
    return render_template("message_return.html", URL="/",
                           TextMessage="Development Upgrade in Progress",
                           TextMessage2="Please wait ...")


@http_routes.route("/ReStart")
def restart_program():
    app_generic_functions.thread_function(os.system, args="systemctl restart KootnetEthServer")
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

    if request.form.get("checkbox_iperf_server") is not None:
        current_config.is_iperf_server = 1
    else:
        current_config.is_iperf_server = 0

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
    print("Starting HTML Wireless Configuration Update")
    current_config.wifi_country_code = html_request.form.get("country_code")
    current_config.wifi_ssid = html_request.form.get("ssid1")
    current_config.wifi_security_type = html_request.form.get("wifi_security1")
    current_config.wifi_pass_key = html_request.form.get("wifi_key1")


def set_html_config_ipv4(html_request, wireless_type=False):
    print("Starting HTML IPv4 Configuration Update for Ethernet or Wireless.  Wireless = " + str(wireless_type))
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
