#!/bin/python3
'''
                                           __                __        __ 
                                          /  |              /  |      /  |
  _______   ______   __    __   ______   _%% |_     ______  %%/   ____%% |
 /       | /      \ /  |  /  | /      \ / %%   |   /      \ /  | /    %% |
/%%%%%%%/ /%%%%%%  |%% |  %% |/%%%%%%  |%%%%%%/   /%%%%%%  |%% |/%%%%%%% |
%% |      %% |  %%/ %% |  %% |%% |  %% |  %% | __ %% |  %% |%% |%% |  %% |
%% \_____ %% |      %% \__%% |%% |__%% |  %% |/  |%% \__%% |%% |%% \__%% |
%%       |%% |      %%    %% |%%    %%/   %%  %%/ %%    %%/ %% |%%    %% |
 %%%%%%%/ %%/        %%%%%%% |%%%%%%%/     %%%%/   %%%%%%/  %%/  %%%%%%%/ 
                    /  \__%% |%% |                                        
                    %%    %%/ %% |                                        
                     %%%%%%/  %%/ 
                     
Main Python Code                                        
'''    

from PyQt5 import QtWidgets, QtCore, uic
import sys
import random
import os
import time
from cryptoidHAL import *

if os.uname()[1] == 'cryptoid':
    import RPi.GPIO as GPIO
    from hcsr04sensor import sensor
    import serial

def ultrasonicPoll(self, trig, echo, trig2, echo2):
    sensor1 = sensor.Measurement(trig, echo) # Init both sensors
    sensor2 = sensor.Measurement(trig2, echo2)
    distance1 = sensor1.raw_distance() # Get raw distance readings
    distance2 = sensor2.raw_distance()

    self.distanceValue1.setText(str(round(distance1)) + " cm") # Set labels back in Qt GUI
    self.distanceValue2.setText(str(round(distance2)) + " cm")

def setSTM32Text(self, state):
    if state == True:
        self.stm32Connected.setText("STM32 Connected") # Set text + colour
        self.stm32Connected.setStyleSheet("color:#33cc33")
    elif state == False:
        self.stm32Connected.setText("STM32 Disconnected")
        self.stm32Connected.setStyleSheet("color:#ff0000")
    
def gpioInit(self):
    GPIO.setmode(GPIO.BCM) # Set mode to BCM numbering

class MainWindow(QtWidgets.QMainWindow):

    def buttonFunction(self):
        setLED(self, "all", 0, 0, 255)

        beepSPKR(self, 523, 200)
        time.sleep(0.2)
        beepSPKR(self, 523, 200)
        time.sleep(0.2)
        beepSPKR(self, 523, 200)
        time.sleep(0.2)
        beepSPKR(self, 523, 200)
        time.sleep(0.6)
        beepSPKR(self, 415, 200)
        time.sleep(0.6)
        beepSPKR(self, 466, 200)
        time.sleep(0.5)
        beepSPKR(self, 523, 200)
        time.sleep(0.3)
        beepSPKR(self, 466,200)
        time.sleep(0.2)
        beepSPKR(self, 523, 200)

    def toggleUltrasonicTimer(self):
        if self.ultrasonicTimer.isActive() == False:
            self.ultrasonicTimer.start(500)
        else:
            self.ultrasonicTimer.stop()

    def clearLog(self): # Clear the log
        self.logTb.clear()

    def closeApp(self):
        sys.exit()

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        uic.loadUi('mainwindow.ui', self)

        global stm32
        stm32 = serial.Serial('/dev/ttyAMA0', 115200, parity=serial.PARITY_EVEN) # Open serial comms with the STM32
        self.logTb.append("Trying to initialize the STM32")
        while True: # Check for response
            stm32.write("INIT\r\n".encode()) # Init the STM32
            self.logTb.append("INIT")
            response = stm32.readline()
            self.logTb.append(str(response))
            if response.decode() == "OK\r\n":
                self.logTb.append("STM32 is working")
                setSTM32Text(self, True)
                break
        
        gpioInit(self)

        self.ultrasonicTimer = QtCore.QTimer()
        self.ultrasonicTimer.timeout.connect(lambda: ultrasonicPoll(self, 22, 12, 23, 1))

        self.enableUltrasonicPoll.clicked.connect(self.toggleUltrasonicTimer)
        self.doAThing.clicked.connect(self.buttonFunction)
        self.clearBtn.clicked.connect(self.clearLog)
        self.resetBtn.clicked.connect(resetSTM)
        self.versBtn.clicked.connect(printVer)
        self.actionQuit.triggered.connect(self.closeApp)

def main():
    app = QtWidgets.QApplication(sys.argv)
    main = MainWindow()
    main.show()
    sys.exit(app.exec_())

if __name__ == '__main__':         
    main()