from gpiozero import LEDBoard, MotionSensor, LED, Button
from subprocess import check_call
import sys
import os
import smbus
import time
from signal import pause
import requests
from threading import Thread
import logging
from datetime import datetime

pressed_right=''

def reboot():
    try:
        red.on()
        green.off()
        time.sleep(2)
        print("rebooting pi...")
        time.sleep(2)
        os.system("sudo reboot")
    except Exception as e :
        print('Exception occured while trying to reboot-->',e)
        logging.exception("Exception while trying to reboot: -->",e)
        pass
def reboot_monitor():
    try:
        red.on()
        time.sleep(2)
        print("rebooting monitor...")
        r = requests.get('http://10.100.102.30:6000/reboot')
        print("now sleep 20 seconds")
        time.sleep(18)
        print("now rebooting this device")
        time.sleep(2)
        reboot()
    except Exception as e:      
        print ('Unable to reboot monitor!',e)
        logging.exception("Exception while trying to reboot monitor: -->",e)
        pass
def openVLC():
    script = '/home/pi/Downloads/buildm3u'
    global pressed_right
    try:
        print ('VLC is now running!')
        check_call(["cvlc", script])
    except Exception as e:	
        print ('Unable to open VLC!',e)
        logging.exception("Exception while trying to open vlc: -->",e)
        pass
    
def checkVLC():
    try:
        while True:
            processname = 'buildm3u'
            tmp = os.popen("ps -aux").read()
            proaccount = tmp.count(processname)
            if proaccount == 0:
                red.on()
            else:
                red.off()
            time.sleep(10)
    except Exception as e :
        print('error while trying to check if vlc is running')
        print ('Error is: ',e)
        logging.exception("Exception while trying to check if vlc is running: -->",e)
        pass
        
    
def checkDarkice():

    try:
        while True:
            #check if darkice is running
            response = requests.get('http://10.100.102.30:9000/auth.xsl')
            if "password" not in response.text:
                print("darkice is down")
                green.off()
                dt=datetime.now()
                dtTemp = dt.strftime('%d-%b-%Y - %H-%M-%S')
                file_name = "reboot_baby_pi.txt"
                new_string = "rebooting %s" % dtTemp
                opened_file = open(file_name, 'a')
                opened_file.write("%r\n" %new_string)
                opened_file.close()
                r = requests.get('http://10.100.102.30:6000/reboot')
            else:
                print("darkice is up")
                green.on()
            time.sleep(10)
    except Exception as e :
        print('error while trying to check if darkice is running')
        print ('Error is: ',e)
        logging.exception("Exception while trying to check if darkice is running: -->",e)
        pass

    
if __name__ == '__main__':

  try:
    logging.basicConfig(level=logging.DEBUG, filename='launcher_errors.log')
    button = Button(24)
    button_exit=Button(16)
    #leds = LEDBoard(6, active_high=True)
    green = LED(27)
    red = LED(6)
    button.when_pressed = reboot_monitor
    button_exit.when_pressed = reboot
    t1 = Thread(target = checkDarkice)
    t1.setDaemon(True)
    t1.start()
    t2 = Thread(target = checkVLC)
    t2.setDaemon(True)
    t2.start()
    pause()

  except Exception as e :
    print('error on main')
    print ('Error is: ',e)
    logging.exception("Exception occured on main! this is a custom error message")
    pass
  finally:
    green.off()
    red.off()
        
