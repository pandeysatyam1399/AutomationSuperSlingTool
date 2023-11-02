################################################################

# File: itachIP2IR.py
# Author: Satyam Pandey
# Date: 2023-11-02
# Description: This is a Python script for Itach IP2IR APIs that
#              Does all the get and send of itach commands to STB.

################################################################
import socket
import automationConfig as ssc

class itach:
    remote_type = None
    itach_port = None
    itach_IP = None
    itachCode = None
    itachCodes = None
    dattDB = None
    keyMap = None

    def __init__(self):
        # Key Press config
        self.keyMap = ssc.key_config()
        # IR codes
        self.itachCodes = self.read_ir_codes('ir_codes_itach.txt')
        # Database
        self.dattDB = self.read_super_sling_db('SuperSlingDB.txt')

    def read_ir_codes(self, filename):
        itachCodes = {}
        with open(filename, 'r') as file:
            for line in file:
                parts = line.strip().split('|')
                if len(parts) == 3:
                    remote_type, itachCode, _ = parts
                    itachCodes[remote_type] = itachCode
        
        return itachCodes

    def read_super_sling_db(self, filename):
        dattDB = {}
        with open(filename, 'r') as file:
            for line in file:
                if not line.startswith('#'):
                    parts = line.strip().split('|')
                    if len(parts) == 5:
                        stb_id, itach_ip, itach_port, stb_type, stb_info = parts
                        dattDB[stb_id] = {
                            'iTach_IP': itach_ip,
                            'iTach_port': itach_port,
                            'stb_type': stb_type,
                            'STB_INFO': stb_info
                        }
        
        return dattDB

    def getData(self, stb_no):
        data = self.dattDB.get(stb_no)
        if data:
            # print(data)
            self.remote_type = data['stb_type']
            self.itach_port = data['iTach_port']
            self.itach_IP = data['iTach_IP']

    def sendData(self, onPress):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        if self.itachCode is None:
            self.getItachCodes("Charter Motorola:" + str(onPress))
        else:
            pass
        dataToSend = "sendir,1:" + str(self.itach_port) + ",111,38109,1,1," + self.itachCode + "\r"
        s.connect((self.itach_IP, 4998))
        s.sendall(dataToSend.encode())

        self.itachCode = None

        response = s.recv(1024).decode()
        if len(response) == 0:
            print("Error while sending itach code to", self.itach_IP)

        s.close()

    def getItachCodes(self, remote_data):
        self.itachCode = self.itachCodes.get(remote_data)

    def OnKeyPress(self, key):
        try:
            # print(self.keyMap.get(key.lower()))
            self.sendData(self.keyMap.get(key.lower()))
        except:
            print("Not correct Key Press", key)
            pass
