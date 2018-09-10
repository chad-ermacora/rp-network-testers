'''
    KootNet Network Testers is a programs to test a Network Connection
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
'''

import epsimplelib, os, socket
import RPi.GPIO as GPIO
from time import sleep, strftime

GPIO.setmode(GPIO.BCM)
key1 = 5
key2 = 6
key3 = 13
key4 = 19

GPIO.setup(key1, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(key2, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(key3, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(key4, GPIO.IN, pull_up_down=GPIO.PUD_UP)

esp = epsimplelib.EPScreen('portrait') # eps = e-Ink Paper Screen
esp2 = epsimplelib.EPScreen('portrait') # eps = e-Ink Paper Screen

def esp_message(message1):
    esp.add_text((1,1), message1)
    esp.update_screen()
    
def esp_message2(message2):
    esp2.add_text((1,1), message2)
    esp2.update_screen()
    
esp_message("Device Ready\n\nBe sure to\nGive 15 Seconds\nFor Remote\nDevice to boot\nTime: " + str(strftime("%H:%M")))

while True:
    key1state = GPIO.input(key1)
    key2state = GPIO.input(key2)
    key3state = GPIO.input(key3)
    key4state = GPIO.input(key4)
    
    if key1state == False:
        esp = epsimplelib.EPScreen('portrait') # eps = e-Ink Paper Screen
        esp2 = epsimplelib.EPScreen('portrait') # eps = e-Ink Paper Screen
        print("Key1 Pressed")
        esp_message("Starting MTR\nPlease Wait ...")
        
        try:
            
            os.system("mtr -c 10 -r -n 192.168.169.251 > /home/pi/MTR_Results.txt")
            localfile = open("/home/pi/MTR_Results.txt", "r")
            mess = localfile.read()
            message = "MTR Results\nSent: " + str(mess)[-34:-30] + "\nLoss: " + str(mess)[-43:-35] + \
                      "\nAvg: " + str(mess)[-23:-18] + "ms" + "\nWorst: " + str(mess)[-10:-6] + \
                      "ms" + "\nBest: " + str(mess)[-17:-12] + "ms" + "\nLast: " + str(mess)[-29:-24] + \
                      "ms" + "\nStDev: " + str(mess)[-5:-1] + "ms" + "\n\n Day/Month/Year" + "\n\nDate: " + \
                      str(strftime("%d/%m/%y")) + "\nTime: " + str(strftime("%H:%M"))
            
            print(message)
            esp_message2(message)
        except:
            esp_message2("MTR Failed\nUnit Offline?\nTime: " + str(strftime("%H:%M")))
            
    elif key2state == False:
        esp = epsimplelib.EPScreen('portrait') # eps = e-Ink Paper Screen
        esp2 = epsimplelib.EPScreen('portrait') # eps = e-Ink Paper Screen
        print('Key2 Pressed')
        esp_message("Starting iPerf\nPlease Wait ...")
        
        try:
            
            os.system("iperf3 -c 192.168.169.251 -O 1 -p 9000 > /home/pi/iperf_Results.txt")
            localfile = open("/home/pi/iperf_Results.txt", "r")
            mess = localfile.read()
            message = "iPerf3 Results\nMax device\nBandwidth\n 220Mbps-230Mbps\n\nTransfered:\n" + \
                      str(mess)[-68:-55] + "\nBandwidth:\n" + str(mess)[-55:-40] + "\nOver " + \
                      str(mess)[-79:-68] + "\n\n Day/Month/Year" + "\nDate: " + str(strftime("%d/%m/%y")) + \
                      "\nTime: " + str(strftime("%H:%M"))
            
            print(message)
            esp_message2(message)
        except:
            esp_message2("iPerf3 Failed\nUnit Offline?\nTime: " + str(strftime("%H:%M")))
        
    elif key3state == False:
        esp = epsimplelib.EPScreen('portrait') # eps = e-Ink Paper Screen
        server_address = ('192.168.169.251', 10062)
        print('Key3 Pressed')
        try:
            sockG = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sockG.connect(server_address)
            esp_message("Shutting Down\nRemote Unit\nTime: " + str(strftime("%H:%M")))
        except:
            esp_message("Shut Down Failed\nRemote N/A\nOffline : " + str(strftime("%H:%M")))

    elif key4state == False:
        esp = epsimplelib.EPScreen('portrait') # eps = e-Ink Paper Screen
        print('Key4 Pressed')
        try:
            esp_message("Shutting Down\nLocal Unit\nTime: " + str(strftime("%H:%M")))
            os.system("shutdown now -h")
        except:
            esp_message("Shut Down Failed?\nTime: " + str(strftime("%H:%M")))
        
    sleep(1)