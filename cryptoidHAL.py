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
                     
HAL Module                                     
'''

import serial

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

def printVer(self): # Print STM version info
    stm32.write("VERS\r\n".encode())
    response = stm32.readline()
    response2 = stm32.readline()
    response3 = stm32.readline()

    self.logTb.append(str(response))
    self.logTb.append(str(response2))
    self.logTb.append(str(response3))

def resetSTM(self): # Send Software Reset instruction
    stm32.write("RSTS\r\n".encode())
    self.logTb.append("Resetting now...")
    time.sleep(1.5)
    stm32.reset_input_buffer()
    self.logTb.append("Reset Complete")

def halINIT(self):
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
    
def setSTM32Text(self, state):
    if state == True:
        self.stm32Connected.setText("STM32 Connected") # Set text + colour
        self.stm32Connected.setStyleSheet("color:#33cc33")
    elif state == False:
        self.stm32Connected.setText("STM32 Disconnected")
        self.stm32Connected.setStyleSheet("color:#ff0000")