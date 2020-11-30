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

if os.uname()[1] == 'cryptoid':
    import RPi.GPIO as GPIO
    from hcsr04sensor import sensor
    import serial

def ultrasonicPoll(self, trig, echo, trig2, echo2):
    sensor1 = sensor.Measurement(trig, echo) # Init both sensors
    sensor2 = sensor.Measurement(trig2, echo2)
    distance1 = sensor1.raw_distance() # Get raw distance readings
    distance2 = sensor2.raw_distance()

    '''distance1 = random.randint(0, 999) # Fake values while we're not on actual HW
    distance2 = random.randint(0, 999)'''

    self.distanceValue1.setText(str(round(distance1)) + " cm") # Set labels back in Qt GUI
    self.distanceValue2.setText(str(round(distance2)) + " cm")

def setSTM32Text(self, state):
    if state == True:
        self.stm32Connected.setText("STM32 Connected") # Set text + colour
        self.stm32Connected.setStyleSheet("color:#33cc33")
    elif state == False:
        self.stm32Connected.setText("STM32 Disconnected")
        self.stm32Connected.setStyleSheet("color:#ff0000")

def beepBuzzer(self, noteList):
    notes = {
        "A": 440,
        "B": 494,
        "C": 523,
        "D": 587,
        "E": 659,
        "F": 698,
        "G": 784
    }
    for x in noteList:
        freq = notes[x]
        print(freq)
        buzzerPWM.ChangeFrequency(freq)
        buzzerPWM.ChangeDutyCycle(20)
    buzzerPWM.ChangeDutyCycle(0)
    
def gpioInit(self):

    GPIO.setmode(GPIO.BCM) # Set mode to BCM numbering
    GPIO.setup(18, GPIO.OUT)

    global buzzerPWM
    buzzerPWM = GPIO.PWM(18, 1000)

class MainWindow(QtWidgets.QMainWindow):

    def buttonFunction(self):
        global textState
        try: 
            textState
        except NameError: 
            textState = "Default"

        if textState == "Default":
            self.mwLabel.setText("World Hello!")
            textState = "Changed"
        elif textState == "Changed":
            self.mwLabel.setText("Hello World!")
            textState = "Default"
    
    def toggleUltrasonicTimer(self):
        if self.ultrasonicTimer.isActive() == False:
            self.ultrasonicTimer.start(500)
        else:
            self.ultrasonicTimer.stop()

    def closeApp(self):
        sys.exit()

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        uic.loadUi('mainwindow.ui', self)

        stm32 = serial.Serial('/dev/ttyAMA0', 115200, parity=serial.PARITY_EVEN) # Open serial comms with the STM32
        print("Trying to initialize the STM32")
        while True: # Check for response
            stm32.write("INIT\r\n".encode()) # Init the STM32
            response = stm32.readline()
            print(response)
            if response.decode() == "OK\r\n":
                print("STM32 is working")
                setSTM32Text(self, True)
                break
        
        gpioInit(self)
        beepBuzzer(self, ["A", "D", "E"])

        self.ultrasonicTimer = QtCore.QTimer()
        self.ultrasonicTimer.timeout.connect(lambda: ultrasonicPoll(self, 22, 12, 23, 1))

        self.enableUltrasonicPoll.clicked.connect(self.toggleUltrasonicTimer)
        self.doAThing.clicked.connect(self.buttonFunction)
        self.actionQuit.triggered.connect(self.closeApp)

def main():
    app = QtWidgets.QApplication(sys.argv)
    main = MainWindow()
    main.show()
    sys.exit(app.exec_())

if __name__ == '__main__':         
    main()