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

    self.distanceValue1.setText(str(round(distance1)) + " cm") # Set labels back in Qt GUI
    self.distanceValue2.setText(str(round(distance2)) + " cm")

def beepSPKR(self, freq, duration):
    while True:
        self.logTb.append("SPKR")
        stm32.write("SPKR\r\n".encode())
        response = stm32.readline()
        self.logTb.append(str(response))
        if response.decode() == "OK\r\n":
            stm32.write(str(freq).encode())
            stm32.write("\r\n".encode())
            response = stm32.readline()
            self.logTb.append(str(response))
            if response.decode() == "OK\r\n":
                stm32.write(str(duration).encode())
                stm32.write("\r\n".encode())
                response = stm32.readline()
                self.logTb.append(str(response))
                if response.decode() == "OK\r\n":
                    break

def setLED(self, ledID, rValue, gValue, bValue):
    if ledID == "all": # If setting all LEDs
        while True: # Loop until all data sent
            self.logTb.append("LEDA")
            stm32.write("LEDA\r\n".encode()) # Send command
            response = stm32.readline() # Read response
            self.logTb.append(str(response)) # Print response
            if response.decode() == "OK\r\n": # If response recieved
                stm32.write(str(rValue).encode()) # Send first set of data
                stm32.write("\r\n".encode()) # Send newline
                response = stm32.readline() # Get second response
                self.logTb.append(str(response)) # Print second response
                if response.decode() == "OK\r\n": # If response recieved
                    stm32.write(str(gValue).encode()) # Send second set of data
                    stm32.write("\r\n".encode()) # Send newline
                    response = stm32.readline() # Get third response
                    self.logTb.append(str(response)) # Print third response
                    if response.decode() == "OK\r\n": # If response recieved
                        stm32.write(str(bValue).encode()) # Send third set of data
                        stm32.write("\r\n".encode()) # Send newline
                        response = stm32.readline() # Get fourth response
                        self.logTb.append(str(response)) # Print third response
                        if response.decode() == "OK\r\n": # If response recieved
                            break # Sent successfully, break from loop.

    else: # If only setting one
        while True:
            self.logTb.append("LEDS")
            stm32.write("LEDS\r\n".encode())
            response = stm32.readline()
            self.logTb.append(str(response))
            if response.decode() == "OK\r\n":
                stm32.write(ledID.encode())
                stm32.write("\r\n".encode())
                response = stm32.readline()
                self.logTb.append(str(response))
                if response.decode() == "OK\r\n":
                    stm32.write(str(rValue).encode())
                    stm32.write("\r\n".encode())
                    response = stm32.readline()
                    self.logTb.append(str(response))
                    if response.decode() == "OK\r\n":
                        stm32.write(str(gValue).encode())
                        stm32.write("\r\n".encode())
                        response = stm32.readline()
                        self.logTb.append(str(response))
                        if response.decode() == "OK\r\n":
                            stm32.write(str(bValue).encode())
                            stm32.write("\r\n".encode())
                            response = stm32.readline()
                            self.logTb.append(str(response))
                            if response.decode() == "OK\r\n":
                                break

def setMotor(self, motorID, direction, speed): # Set one motor
    while True:
        self.logTb.append("SETM")
        stm32.write("SETM\r\n".encode())
        response = stm32.readline()
        self.logTb.append(str(response))
        if response.decode() == "OK\r\n":
            stm32.write(str(motorID).encode())
            stm32.write("\r\n".encode())
            response = stm32.readline()
            self.logTb.append(str(response))
            if response.decode() == "OK\r\n":
                stm32.write(str(direction).encode())
                stm32.write("\r\n".encode())
                response = stm32.readline()
                self.logTb.append(str(response))
                if response.decode() == "OK\r\n":
                    stm32.write(str(speed).encode())
                    stm32.write("\r\n".encode())
                    response = stm32.readline()
                    self.logTb.append(str(response))
                    if response.decode() == "OK\r\n":
                        break

def stopMotor(self, motorID): # Stop one motor
    while True:
        self.logTb.append("STPM")
        stm32.write("STPM\r\n".encode())
        response = stm32.readline()
        self.logTb.append(str(response))
        if response.decode() == "OK\r\n":
            stm32.write(str(motorID).encode())
            stm32.write("\r\n".encode())
            response = stm32.readline()
            self.logTb.append(str(response))
            if response.decode() == "OK\r\n":
                break

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

    def initSTM(self): # Send INIT command
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

    def resetSTM(self): # Send Software Reset instruction
        stm32.write("RSTS\r\n".encode())
        self.logTb.append("Resetting now...")
        time.sleep(1.5)
        stm32.reset_input_buffer()
        setSTM32Text(self, False)
        self.logTb.append("Reset Complete")

    def clearLog(self): # Clear the log
        self.logTb.clear()
    
    def printVer(self): # Print STM version info
        stm32.write("VERS\r\n".encode())
        response = stm32.readline()
        response2 = stm32.readline()
        response3 = stm32.readline()

        self.logTb.append(str(response))
        self.logTb.append(str(response2))
        self.logTb.append(str(response3))

    def motorSet(self): # Set one motor
        motorID, okPressed = QtWidgets.QInputDialog.getInt(self, "Motor ID", "Motor ID?", 1, 1, 4, 1)
        direction, okPressed = QtWidgets.QInputDialog.getInt(self, "Direction", "1 is FWD, 2 is BWD:", 1, 1, 2, 1)
        speed, okPressed = QtWidgets.QInputDialog.getInt(self, "Speed", "Speed?", 255, 1, 255, 25)
        if okPressed:
            setMotor(self, motorID, direction, speed)

    def stopMotorBtn(self): # Stop one motor
        motorID, okPressed = QtWidgets.QInputDialog.getInt(self, "Motor ID", "Motor ID?", 1, 1, 4, 1)
        if okPressed:
            stopMotor(self, motorID)

    def allMotor(self): # Set all motors
        direction, okPressed = QtWidgets.QInputDialog.getInt(self, "Direction", "1 is FWD, 2 is BWD:", 1, 1, 2, 1)
        speed, okPressed = QtWidgets.QInputDialog.getInt(self, "Speed", "Speed?", 255, 1, 255, 25)
        if okPressed:
            for i in range(4):
                setMotor(self, i+1, direction, speed)

    def stopAllMotorBtn(self): # Stop all motors
        for i in range(4):
            stopMotor(self, i+1)

    def setLED(self): # Set one LED
        ledID, okPressed = QtWidgets.QInputDialog.getInt(self, "LED ID", "LED ID?", 1, 1, 36, 1)
        rValue, okPressed = QtWidgets.QInputDialog.getInt(self, "Red", "Red?", 255, 0, 255, 25)
        gValue, okPressed = QtWidgets.QInputDialog.getInt(self, "Green", "Green?", 255, 0, 255, 25)
        bValue, okPressed = QtWidgets.QInputDialog.getInt(self, "Blue", "Blue?", 255, 0, 255, 25)
        if okPressed:
            setLED(self, str(ledID-1), rValue, gValue, bValue)

    def allLED(self): # Set all LEDs
        rValue, okPressed = QtWidgets.QInputDialog.getInt(self, "Red", "Red?", 255, 0, 255, 25)
        gValue, okPressed = QtWidgets.QInputDialog.getInt(self, "Green", "Green?", 255, 0, 255, 25)
        bValue, okPressed = QtWidgets.QInputDialog.getInt(self, "Blue", "Blue?", 255, 0, 255, 25)
        if okPressed:
            setLED(self, "all", rValue, gValue, bValue)

    def closeApp(self):
        sys.exit()

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        uic.loadUi('mainwindow.ui', self)

        global stm32
        stm32 = serial.Serial('/dev/ttyAMA0', 115200, parity=serial.PARITY_EVEN) # Open serial comms with the STM32
        self.initSTM()
        
        gpioInit(self)

        self.ultrasonicTimer = QtCore.QTimer()
        self.ultrasonicTimer.timeout.connect(lambda: ultrasonicPoll(self, 22, 12, 23, 1))

        self.enableUltrasonicPoll.clicked.connect(self.toggleUltrasonicTimer)
        self.doAThing.clicked.connect(self.buttonFunction)
        self.clearBtn.clicked.connect(self.clearLog)
        self.resetBtn.clicked.connect(self.resetSTM)
        self.versBtn.clicked.connect(self.printVer)
        self.motorBtn.clicked.connect(self.motorSet)
        self.stopMtrBtn.clicked.connect(self.stopMotorBtn)
        self.allMotorBtn.clicked.connect(self.allMotor)
        self.stopAllMtrBtn.clicked.connect(self.stopAllMotorBtn)
        self.reInit.clicked.connect(self.initSTM)
        self.setLEDBtn.clicked.connect(self.setLED)
        self.allLEDBtn.clicked.connect(self.allLED)
        self.actionQuit.triggered.connect(self.closeApp)

def main():
    app = QtWidgets.QApplication(sys.argv)
    main = MainWindow()
    main.show()
    sys.exit(app.exec_())

if __name__ == '__main__':         
    main()