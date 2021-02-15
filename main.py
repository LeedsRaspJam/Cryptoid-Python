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

from PyQt5 import QtWidgets, QtCore, QtGui, uic
import sys
import random
import os
from datetime import datetime
from pygments import highlight
from pygments.lexers import *
from pygments.formatter import Formatter
import re
import psutil
import time

if os.uname()[1] == 'cryptoid':
    import RPi.GPIO as GPIO
    import lib_ultrasonicsensor as sensor
    import serial
    import picamera
    import picamera.array
    import lib_gamepad as Gamepad

global motorBuffer, ledBuffer
motorBuffer = {
    1: [0, 0],
    2: [0, 0],
    3: [0, 0],
    4: [0, 0]
}

ledBuffer = {
    0: [0, 0, 0],
    1: [0, 0, 0],
    2: [0, 0, 0],
    3: [0, 0, 0],
    4: [0, 0, 0],
    5: [0, 0, 0],
    6: [0, 0, 0],
    7: [0, 0, 0],
    8: [0, 0, 0],
    9: [0, 0, 0],
    10: [0, 0, 0],
    11: [0, 0, 0],
    12: [0, 0, 0],
    13: [0, 0, 0],
    14: [0, 0, 0],
    15: [0, 0, 0],
    16: [0, 0, 0],
    17: [0, 0, 0],
    18: [0, 0, 0],
    19: [0, 0, 0],
    20: [0, 0, 0],
    21: [0, 0, 0],
    22: [0, 0, 0],
    23: [0, 0, 0],
    24: [0, 0, 0],
    25: [0, 0, 0],
    26: [0, 0, 0],
    27: [0, 0, 0],
    28: [0, 0, 0],
    29: [0, 0, 0],
    30: [0, 0, 0],
    31: [0, 0, 0],
    32: [0, 0, 0],
    33: [0, 0, 0],
    34: [0, 0, 0],
    35: [0, 0, 0]
}

def ultrasonicPoll(self):
    distance1 = sensor1.raw_distance(sample_size=2, sample_wait=0.03) # Get raw distance readings
    distance2 = sensor2.raw_distance(sample_size=2, sample_wait=0.03)

    self.distanceValue1.setText(str(round(distance1)) + " cm") # Set labels back in Qt GUI
    self.distanceValue2.setText(str(round(distance2)) + " cm")

    if distance1 < 35 or distance2 < 35:
        if ledBuffer[0] == [0, 255, 0]:
            for i in range(4):
                stopMotor(self, i+1)
            setLED(self, "all", 254, 0, 0)
            MainWindow.stopGP(self)
    elif ledBuffer[0] == [254, 0, 0]:
        setLED(self, "all", 0, 255, 0)

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
        for key in ledBuffer:
            ledBuffer[key] = [rValue, gValue, bValue]
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
        ledBuffer[int(ledID)] = [rValue, gValue, bValue]
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
    motorBuffer[motorID] = [direction, speed]
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
    motorBuffer[motorID] = [0, 0]
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

def setExtPins(self, type1, type2, type3, type4, type5, type6): # Set STM external pins
    while True:
        self.logTb.append("EXTS")
        stm32.write("EXTS\r\n".encode())
        response = stm32.readline()
        self.logTb.append(str(response))
        if response.decode() == "OK\r\n":
            stm32.write(type1.encode())
            stm32.write("\r\n".encode())
            response = stm32.readline()
            self.logTb.append(str(response))
            if response.decode() == "OK\r\n":
                stm32.write(type2.encode())
                stm32.write("\r\n".encode())
                response = stm32.readline()
                self.logTb.append(str(response))
                if response.decode() == "OK\r\n":
                    stm32.write(type3.encode())
                    stm32.write("\r\n".encode())
                    response = stm32.readline()
                    self.logTb.append(str(response))
                    if response.decode() == "OK\r\n":
                        stm32.write(type4.encode())
                        stm32.write("\r\n".encode())
                        response = stm32.readline()
                        self.logTb.append(str(response))
                        if response.decode() == "OK\r\n":
                            stm32.write(type5.encode())
                            stm32.write("\r\n".encode())
                            response = stm32.readline()
                            self.logTb.append(str(response))
                            if response.decode() == "OK\r\n":
                                stm32.write(type6.encode())
                                stm32.write("\r\n".encode())
                                response = stm32.readline()
                                self.logTb.append(str(response))
                                if response.decode() == "OK\r\n":
                                    break

def setServo180(self, id, angle): # Set 180 degree servo
    while True:
        self.logTb.append("SRVO")
        stm32.write("SRVO\r\n".encode())
        response = stm32.readline()
        self.logTb.append(str(response))
        if response.decode() == "OK\r\n":
            stm32.write(str(id).encode())
            stm32.write("\r\n".encode())
            response = stm32.readline()
            self.logTb.append(str(response))
            if response.decode() == "OK\r\n":
                stm32.write(str(angle).encode())
                stm32.write("\r\n".encode())
                response = stm32.readline()
                self.logTb.append(str(response))
                if response.decode() == "OK\r\n":
                    break

def setServo360(self, id, initialAngle, delayTime, stopAngle): # Set 360 degree servo
    while True: # Set to initial angle
        self.logTb.append("SRVO")
        stm32.write("SRVO\r\n".encode())
        response = stm32.readline()
        self.logTb.append(str(response))
        if response.decode() == "OK\r\n":
            stm32.write(str(id).encode())
            stm32.write("\r\n".encode())
            response = stm32.readline()
            self.logTb.append(str(response))
            if response.decode() == "OK\r\n":
                stm32.write(str(initialAngle).encode())
                stm32.write("\r\n".encode())
                response = stm32.readline()
                self.logTb.append(str(response))
                if response.decode() == "OK\r\n":
                    break

    time.sleep(delayTime) # Wait for the specified time

    while True: # Set to stop angle
        self.logTb.append("SRVO")
        stm32.write("SRVO\r\n".encode())
        response = stm32.readline()
        self.logTb.append(str(response))
        if response.decode() == "OK\r\n":
            stm32.write(str(id).encode())
            stm32.write("\r\n".encode())
            response = stm32.readline()
            self.logTb.append(str(response))
            if response.decode() == "OK\r\n":
                stm32.write(str(stopAngle).encode())
                stm32.write("\r\n".encode())
                response = stm32.readline()
                self.logTb.append(str(response))
                if response.decode() == "OK\r\n":
                    break

def setSTM32Text(self, state):
    if state == True:
        for key in ledBuffer:
            ledBuffer[key] = [0, 255, 0]
        self.stm32Connected.setText("STM32 Connected") # Set text + colour
        self.stm32Connected.setStyleSheet("color:#33cc33")
        self.cpuFreqTextB.setText("CPU Freq (HCP): 72 MHz")
    elif state == False:
        for key in ledBuffer:
            ledBuffer[key] = [255, 0, 0]
        self.stm32Connected.setText("STM32 Disconnected")
        self.stm32Connected.setStyleSheet("color:#ff0000")
        self.cpuFreqTextB.setText("CPU Freq (HCP): 0 MHz")

def hex2QColor(c): # Convert to QColor (for highlighting)
    r=int(c[0:2],16)
    g=int(c[2:4],16)
    b=int(c[4:6],16)
    return QtGui.QColor(r,g,b)

def gpioInit(self):
    GPIO.setmode(GPIO.BCM) # Set mode to BCM numbering

    global sensor1, sensor2
    sensor1 = sensor.Measurement(22, 12) # Init both sensors
    sensor2 = sensor.Measurement(23, 1)

# Highlighting class - Copyright (C) 2008 Christophe Kibleur <kib2@free.fr>

class QFormatter(Formatter):
    
    def __init__(self):
        Formatter.__init__(self)
        self.data=[]
        
        # Create a dictionary of text styles, indexed
        # by pygments token names, containing QTextCharFormat
        # instances according to pygments' description
        # of each style
        
        self.styles={}
        for token, style in self.style:
            qtf=QtGui.QTextCharFormat()

            if style['color']:
                qtf.setForeground(hex2QColor(style['color'])) 
            if style['bgcolor']:
                qtf.setBackground(hex2QColor(style['bgcolor'])) 
            if style['bold']:
                qtf.setFontWeight(QtGui.QFont.Bold)
            if style['italic']:
                qtf.setFontItalic(True)
            if style['underline']:
                qtf.setFontUnderline(True)
            self.styles[str(token)]=qtf
    
    def format(self, tokensource, outfile):
        global styles
        # We ignore outfile, keep output in a buffer
        self.data=[]
        
        # Just store a list of styles, one for each character
        # in the input. Obviously a smarter thing with
        # offsets and lengths is a good idea!
        
        for ttype, value in tokensource:
            l=len(value)
            t=str(ttype)                
            self.data.extend([self.styles[t],]*l)

class Highlighter(QtGui.QSyntaxHighlighter):

    def __init__(self, parent, mode):
        QtGui.QSyntaxHighlighter.__init__(self, parent)
        self.tstamp=time.time()
        
        # Keep the formatter and lexer, initializing them 
        # may be costly.
        self.formatter=QFormatter()
        self.lexer=get_lexer_by_name(mode)
        
    def highlightBlock(self, text):
        """Takes a block, applies format to the document. 
        according to what's in it.
        """
        
        # I need to know where in the document we are,
        # because our formatting info is global to
        # the document
        cb = self.currentBlock()
        p = cb.position()

        # The \n is not really needed, but sometimes  
        # you are in an empty last block, so your position is
        # **after** the end of the document.
        text=str(self.document().toPlainText())+'\n'
        
        # Yes, re-highlight the whole document.
        # There **must** be some optimizacion possibilities
        # but it seems fast enough.
        highlight(text,self.lexer,self.formatter)
        
        # Just apply the formatting to this block.
        # For titles, it may be necessary to backtrack
        # and format a couple of blocks **earlier**.
        for i in range(len(str(text))):
            try:
                self.setFormat(i,1,self.formatter.data[p+i])
            except IndexError:
                pass
        
        # I may need to do something about this being called
        # too quickly.
        self.tstamp=time.time() 

class cameraThread(QtCore.QThread):
    def __init__(self, pixmap):
        QtCore.QThread.__init__(self)
        global camera, cameraPixmapB, rawCapture
        camera = picamera.PiCamera()
        camera.resolution = (960, 720)
        camera.framerate = 60
        cameraPixmapB = pixmap
        rawCapture = picamera.array.PiRGBArray(camera, size=(960, 720))

    def run(self):
        for frame in camera.capture_continuous(rawCapture, format="rgb", use_video_port=True):
                frame.truncate()
                frame.seek(0)
                image = frame.array
                qImg = QtGui.QImage(image, 960, 720, QtGui.QImage.Format_RGB888)
                cameraPixmapB.setPixmap(QtGui.QPixmap.fromImage(qImg))
                self.usleep(200)

class monitorThread(QtCore.QThread):
    setOneBarSignal = QtCore.pyqtSignal([int])
    setTwoBarSignal = QtCore.pyqtSignal([int])
    setThreeBarSignal = QtCore.pyqtSignal([int])
    setFourBarSignal = QtCore.pyqtSignal([int])

    setCpuFreqTextSignal = QtCore.pyqtSignal([str])
    setRamTextSignal = QtCore.pyqtSignal([str])
    setRamTextSysSignal = QtCore.pyqtSignal([str])
    resetSysMonTextSignal = QtCore.pyqtSignal()

    def __init__(self):
        QtCore.QThread.__init__(self)
        global killMonitorThread
        killMonitorThread = False

    def run(self):
        while True:
            cpuInfo = psutil.cpu_percent(interval = 1, percpu=True)
            self.setOneBarSignal.emit(int(cpuInfo[0]))
            self.setTwoBarSignal.emit(int(cpuInfo[1]))
            self.setThreeBarSignal.emit(int(cpuInfo[2]))
            self.setFourBarSignal.emit(int(cpuInfo[3]))

            self.setCpuFreqTextSignal.emit("CPU Freq: " + str(int(psutil.cpu_freq().current)) + " MHz")
            self.setRamTextSysSignal.emit("RAM Usage (Sys): " + str(int(psutil.virtual_memory().used/1024/1024)) + " MB")
            self.setRamTextSignal.emit("RAM Usage: " + str(int(process.memory_info()[0]/1024/1024)) + " MB")

            if killMonitorThread == True:
                self.resetSysMonTextSignal.emit()
                break

            self.usleep(2000)

class controllerThread(QtCore.QThread):
    setDirectionLabelSignal = QtCore.pyqtSignal([str])
    setLControllerBarSignal = QtCore.pyqtSignal([int])
    setRControllerBarSignal = QtCore.pyqtSignal([int])
    beginUSPollingSignal = QtCore.pyqtSignal()

    def __init__(self):
        QtCore.QThread.__init__(self)
        global killControllerThread
        killControllerThread = False

    def run(self):
        while True:
            self.controllerPoll()
            if killControllerThread == True:
                self.beginUSPollingSignal.emit()
                break

            self.usleep(125)

    def setMotorSilent(self, motorID, direction, speed): # Set one motor with no logging
        motorBuffer[motorID] = [direction, speed]
        while True:
            stm32.write("SETM\r\n".encode())
            response = stm32.readline()
            if response.decode() == "OK\r\n":
                stm32.write(str(motorID).encode())
                stm32.write("\r\n".encode())
                response = stm32.readline()
                if response.decode() == "OK\r\n":
                    stm32.write(str(direction).encode())
                    stm32.write("\r\n".encode())
                    response = stm32.readline()
                    if response.decode() == "OK\r\n":
                        stm32.write(str(speed).encode())
                        stm32.write("\r\n".encode())
                        response = stm32.readline()
                        if response.decode() == "OK\r\n":
                            break

    def controllerPoll(self):
        try:
            right_y = gamepad.axis("RIGHT-Y")
            left_x = gamepad.axis("LEFT-X")

            if right_y > 0:
                isBackward = True
                isStopped = False
            elif right_y < 0:
                isBackward = False
                isStopped = False
            elif right_y == 0:
                isStopped = True

            y_corrected = abs(right_y) * 155

            if left_x < 0:
                l_value = abs(left_x) * y_corrected
                r_value = 0
            elif left_x > 0:
                l_value = 0
                r_value = abs(left_x) * y_corrected
            elif left_x == 0:
                l_value = y_corrected
                r_value = y_corrected

            if l_value != 0 and y_corrected != 0:
                l_value = l_value + 100
            if r_value != 0 and y_corrected != 0:
                r_value = r_value + 100

            if isStopped == True:
                self.setLControllerBarSignal.emit(100)
                self.setRControllerBarSignal.emit(100)
            else:
                self.setLControllerBarSignal.emit(l_value)
                self.setRControllerBarSignal.emit(r_value)

            if left_x > 0:
                self.setLControllerBarSignal.emit(100)
            elif left_x < 0:
                self.setRControllerBarSignal.emit(100)

            if isStopped == True:
                self.setDirectionLabelSignal.emit("Stopped")
                self.setMotorSilent(1, 2, l_value)
                self.setMotorSilent(3, 2, l_value)
                self.setMotorSilent(2, 2, r_value)
                self.setMotorSilent(4, 2, r_value)
            elif isBackward == False:
                self.setDirectionLabelSignal.emit("Forward")
                self.setMotorSilent(1, 1, l_value)
                self.setMotorSilent(3, 1, l_value)
                self.setMotorSilent(2, 1, r_value)
                self.setMotorSilent(4, 1, r_value)
            elif isBackward == True:
                self.setDirectionLabelSignal.emit("Backward")
                self.setMotorSilent(1, 2, l_value)
                self.setMotorSilent(3, 2, l_value)
                self.setMotorSilent(2, 2, r_value)
                self.setMotorSilent(4, 2, r_value)
        except():
            errorMsg = QtWidgets.QErrorMessage()
            errorMsg.showMessage("You need to connect a controller before polling can begin.")
            global killControllerThread
            killControllerThread = True

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
            if self.controllerQThread.isRunning() == True:
                print("Controller thread is running, killing it")
                global killControllerThread
                killControllerThread = True
            else:
                self.ultrasonicTimer.start(50)
                setLED(self, "all", 0, 255, 0)
        else:
            self.ultrasonicTimer.stop()

    def beginUSPolling(self): # Begin US Polling (used when terminating controller thread)
        self.ultrasonicTimer.start(50)
        self.setLED("all", 0, 255, 0)

    def initSTM(self): # Send INIT command
        global currentColour
        self.logTb.append("Trying to initialize the STM32")
        while True: # Check for response
            stm32.write("INIT\r\n".encode()) # Init the STM32
            self.logTb.append("INIT")
            response = stm32.readline()
            self.logTb.append(str(response))
            if response.decode() == "OK\r\n":
                self.logTb.append("STM32 is working")
                setSTM32Text(self, True)
                currentColour = "green"
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

    def startGP(self): # Start controller polling
        global gamepad
        gamepad = Gamepad.PS4()
        gamepad.startBackgroundUpdates()
        global killControllerThread
        killControllerThread = False
        self.controllerQThread.start()

    def stopGP(self): # Stop controller polling
        global killControllerThread
        killControllerThread = True

    def setLED(self): # Set one LED
        ledID, okPressed = QtWidgets.QInputDialog.getInt(self, "LED ID", "LED ID?", 1, 1, 36, 1)
        ledColor = QtWidgets.QColorDialog.getColor(options = QtWidgets.QColorDialog.DontUseNativeDialog)
        if okPressed:
            setLED(self, str(ledID-1), ledColor.red(), ledColor.green(), ledColor.blue())

    def allLED(self): # Set all LEDs
        ledColor = QtWidgets.QColorDialog.getColor(options = QtWidgets.QColorDialog.DontUseNativeDialog)
        setLED(self, "all", ledColor.red(), ledColor.green(), ledColor.blue())

    def allLEDOff(self): # Turn off all LEDs
        setLED(self, "all", 0, 0, 0)

    def showCamera(self): # Show camera feed
        self.cameraQThread.start()
    
    def startRec(self): # Start recording
        camera.start_recording("/home/pi/recordings/" + str(datetime.now()) + ".h264")
        self.recText.setText("Recording...") # Set text + colour
        self.recText.setStyleSheet("color:#ff0000")

    def stopRec(self): # Stop recording
        try:
            camera.stop_recording()
        except:
            errorMsg = QtWidgets.QErrorMessage(self)
            errorMsg.showMessage("Not currently recording.")

        self.recText.setText("Not Recording") # Set text + colour
        self.recText.setStyleSheet("color:#000000")

    def runTask(self): # Run loaded task
        try:
            taskFile = open(currentTaskLocation, "r") # Open task file as object
            taskContents = taskFile.readlines() # Read lines from file into an array
            for line in taskContents: # For every line in that array
                try:
                    exec(line) # Run it through the interpreter
                except Exception as errorMsg:
                    self.logTb.append("Error in task: halting execution!")
                    self.logTb.append(str(errorMsg))
                    break
            taskFile.close() # Close the file
        except(NameError, FileNotFoundError):
            pass # Do nothing, no file loaded

    def loadTask(self): # Load task into RAM
        global currentTaskLocation
        currentTaskLocation = QtWidgets.QFileDialog.getOpenFileName(self, "Open Task", "tasks", "Cryptoid Task File (*.crtask)") # Get task location with file dialog
        if currentTaskLocation[1] == 'Cryptoid Task File (*.crtask)' and currentTaskLocation[0][-7:] != '.crtask': # If the file is meant to be a .crtask and the extension was not added by Qt
            currentTaskLocation = currentTaskLocation[0] + '.crtask' # Add the extension and remove the second tuple object
        else:
            currentTaskLocation = currentTaskLocation[0] # Just remove the second tuple object

        try:
            taskFile = open(currentTaskLocation, "r") # Open task file as object
            self.taskTextEdit.setPlainText(taskFile.read()) # Dump file to QTextEdit
            taskFile.close() # Close the file
        except(FileNotFoundError):
            pass # Do nothing, user cancelled the operation

    def newTask(self): # Create new task
        global currentTaskLocation
        currentTaskLocation = QtWidgets.QFileDialog.getSaveFileName(self, "Create New Task", "tasks", "Cryptoid Task File (*.crtask)") # Get task location with file dialog
        if currentTaskLocation[1] == 'Cryptoid Task File (*.crtask)' and currentTaskLocation[0][-7:] != '.crtask': # If the file is meant to be a .crtask and the extension was not added by Qt
            currentTaskLocation = currentTaskLocation[0] + '.crtask' # Add the extension and remove the second tuple object
        else:
            currentTaskLocation = currentTaskLocation[0] # Just remove the second tuple object

        if os.path.exists(currentTaskLocation): # If overwriting a file
            os.remove(currentTaskLocation) # Delete the current version

        try:
            taskFile = open(currentTaskLocation, "w") # Open task file as object
            taskFile.write("self.logTb.append(\"Example Text\")") # Write in example text
            taskFile.close() # Close the file

            taskFile = open(currentTaskLocation, "r") # Open task file as object
            self.taskTextEdit.setPlainText(taskFile.read()) # Dump file to QTextEdit
            taskFile.close() # Close the file
        except(FileNotFoundError):
            pass # Do nothing, user cancelled the operation

    def deleteTask(self): # Delete task on SD
        global currentTaskLocation
        delTaskLocation = QtWidgets.QFileDialog.getOpenFileName(self, "Open Task", "tasks", "Cryptoid Task File (*.crtask)") # Get task location with file dialog
        if delTaskLocation[1] == 'Cryptoid Task File (*.crtask)' and delTaskLocation[0][-7:] != '.crtask': # If the file is meant to be a .crtask and the extension was not added by Qt
            delTaskLocation = delTaskLocation[0] + '.crtask' # Add the extension and remove the second tuple object
        else:
            delTaskLocation = delTaskLocation[0] # Just remove the second tuple object
        
        try:
            os.remove(delTaskLocation) # Delete the file
            if delTaskLocation == currentTaskLocation: # If deleting the current file
                self.taskTextEdit.clear() # Clear the QTextEdit
                currentTaskLocation = "" # Clear currentTaskLocation
        except(FileNotFoundError):
            pass # Do nothing, user cancelled the operation

    def onTextUpdate(self): # Save file upon edit
        try:
            taskFile = open(currentTaskLocation, "w") # Open task file as object
            taskFile.write(self.taskTextEdit.toPlainText()) # Dump QTextEdit to file
            taskFile.close() # Close the file
        except(FileNotFoundError, NameError): # On FnFe
            errorMsg = QtWidgets.QErrorMessage(self)
            errorMsg.showMessage("You must open a file before attempting to edit it.")
            self.taskTextEdit.textChanged.disconnect()
            self.taskTextEdit.clear()
            self.taskTextEdit.textChanged.connect(self.onTextUpdate)
        except: # On all other errors
            errorMsg = QtWidgets.QErrorMessage(self)
            errorMsg.showMessage("Error while saving file, something has gone horribly wrong.")
    
    def toggleSystemMonitor(self): # Enable/disable system monitor
        global killMonitorThread
        if self.monitorQThread.isRunning() == False:
            killMonitorThread = False
            self.monitorQThread.start()
        elif self.monitorQThread.isRunning() == True:
            killMonitorThread = True

    def resetSysMonText(self):
        self.oneBar.setValue(100)
        self.twoBar.setValue(100)
        self.threeBar.setValue(100)
        self.fourBar.setValue(100)
        self.cpuFreqText.setText("CPU Freq: ???? MHz")
        self.ramTextSys.setText("RAM Usage (Sys): ??? MB")
        self.ramText.setText("RAM Usage: ??? MB")

    def setDirectionLabel(self, direction):
        if direction == "Stopped":
            self.directionLabel.setText("Stopped")
            self.directionLabel.setStyleSheet("color:#000000")
        elif direction == "Forward":
            self.directionLabel.setText("Forward") # Set text + colour
            self.directionLabel.setStyleSheet("color:#33cc33")
        elif direction == "Backward":
            self.directionLabel.setText("Backward") # Set text + colour
            self.directionLabel.setStyleSheet("color:#ff0000")

    def setLControllerBar(self, lVal):
        self.LBar.setValue(lVal)

    def setRControllerBar(self, rVal):
        self.RBar.setValue(rVal)

    def setOneBar(self, oVal):
        self.oneBar.setValue(oVal)

    def setTwoBar(self, tVal):
        self.twoBar.setValue(tVal)
    
    def setThreeBar(self, tVal):
        self.threeBar.setValue(tVal)

    def setFourBar(self, fVal):
        self.fourBar.setValue(fVal)

    def setCpuFreqText(self, text):
        self.cpuFreqText.setText(text)
    
    def setRamText(self, text):
        self.ramText.setText(text)

    def setRamTextSys(self, text):
        self.ramTextSys.setText(text)
    
    def closeApp(self):
        sys.exit()

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        uic.loadUi('qt_mainwindow.ui', self)
        
        global taskTextEdit, hl
        hl=Highlighter(self.taskTextEdit.document(), "python")

        appPid = os.getpid()
        global process
        process = psutil.Process(appPid)

        verFile = open("version.txt", "rt")
        self.setWindowTitle("Cryptoid Control Utility (Build ID: " + verFile.read()[:-1] + ")")
        verFile.close()

        global stm32
        stm32 = serial.Serial('/dev/ttyAMA0', 115200, parity=serial.PARITY_EVEN) # Open serial comms with the STM32
        self.initSTM()

        gpioInit(self)

        self.ultrasonicTimer = QtCore.QTimer()
        self.ultrasonicTimer.timeout.connect(lambda: ultrasonicPoll(self))

        self.monitorQThread = monitorThread()
        self.cameraQThread = cameraThread(self.cameraPixmap)
        self.controllerQThread = controllerThread()

        self.enableUltrasonicPoll.clicked.connect(self.toggleUltrasonicTimer)
        self.enableSysMon.clicked.connect(self.toggleSystemMonitor)
        self.doAThing.clicked.connect(self.buttonFunction)
        self.clearBtn.clicked.connect(self.clearLog)
        self.resetBtn.clicked.connect(self.resetSTM)
        self.versBtn.clicked.connect(self.printVer)
        self.motorBtn.clicked.connect(self.motorSet)
        self.stopMtrBtn.clicked.connect(self.stopMotorBtn)
        self.allMotorBtn.clicked.connect(self.allMotor)
        self.stopAllMtrBtn.clicked.connect(self.stopAllMotorBtn)
        self.startGPBtn.clicked.connect(self.startGP)
        self.stopGPBtn.clicked.connect(self.stopGP)
        self.reInit.clicked.connect(self.initSTM)
        self.setLEDBtn.clicked.connect(self.setLED)
        self.allLEDBtn.clicked.connect(self.allLED)
        self.allLEDOffBtn.clicked.connect(self.allLEDOff)
        self.showCameraBtn.clicked.connect(self.showCamera)
        self.startRecBtn.clicked.connect(self.startRec)
        self.stopRecBtn.clicked.connect(self.stopRec)
        self.runTaskBtn.clicked.connect(self.runTask)
        self.loadTaskBtn.clicked.connect(self.loadTask)
        self.newTaskBtn.clicked.connect(self.newTask)
        self.deleteTaskBtn.clicked.connect(self.deleteTask)
        self.taskTextEdit.textChanged.connect(self.onTextUpdate)
        self.actionQuit.triggered.connect(self.closeApp)

        self.controllerQThread.setDirectionLabelSignal.connect(self.setDirectionLabel)
        self.controllerQThread.setLControllerBarSignal.connect(self.setLControllerBar)
        self.controllerQThread.setRControllerBarSignal.connect(self.setRControllerBar)
        self.controllerQThread.beginUSPollingSignal.connect(self.beginUSPolling)

        self.monitorQThread.setOneBarSignal.connect(self.setOneBar)
        self.monitorQThread.setTwoBarSignal.connect(self.setTwoBar)
        self.monitorQThread.setThreeBarSignal.connect(self.setThreeBar)
        self.monitorQThread.setFourBarSignal.connect(self.setFourBar)
        self.monitorQThread.setCpuFreqTextSignal.connect(self.setCpuFreqText)
        self.monitorQThread.setRamTextSignal.connect(self.setRamText)
        self.monitorQThread.setRamTextSysSignal.connect(self.setRamTextSys)
        self.monitorQThread.resetSysMonTextSignal.connect(self.resetSysMonText)

def main():
    app = QtWidgets.QApplication(sys.argv)
    main = MainWindow()
    main.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()