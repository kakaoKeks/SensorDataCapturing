import bluetooth
import sys
import time
import json
import save_data
import traceback
import atexit
from MySocket import MySocket


BD_ADDR  = 'test-id-1'
SERVER_ADDR = "127.0.0.1"
PORT = 7777

class Blue:
    
    def close_cli_sock(self):
        print("Disconnecting from cli socket")
        self.cli_sock.disconnect()

    
    def __init__(self):
        self.sock = None
        self.save_sd = save_data.Save()
        self.cli_sock = MySocket()
        self.cli_sock.connect(SERVER_ADDR, PORT)    

    def connect(self):
        try:
            nearby_devices = bluetooth.discover_devices(lookup_names=True)
            print(nearby_devices)
            for dev in nearby_devices:
                if dev[0] == BD_ADDR:
                    print("Host found")

                    port = 1
                    self.sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
                    self.sock.connect((BD_ADDR, port))

                    self.sock.settimeout(20.0)
                
                    return True
            
        except bluetooth.btcommon.BluetoothError:
            print("Couldn't connect to slave module")
            pass
        print("Host not found")    
        return False
    
    def send(self):
        self.sock.send('x')
        print('Daten versendet')
        time.sleep(2)


    def receive(self):
        try:
            rec_string = ""
            while True:
                received = self.sock.recv(1024)

                rec_string += received.decode("utf-8")
                if rec_string[-1:].__eq__("\n"):
                    break
            
            print("Received:", rec_string)
            self.sock.close()
            return json.loads(rec_string)

        except OSError:
            print("Error while receiving data")
            pass
        except bluetooth.btcommon.BluetoothError:
            print("A BluetoothError occurred while receiving data")
            pass
        except json.decoder.JSONDecodeError:
            print("Error while parsing")
            pass
        
        self.sock.close()
        return []
        
    def loop(self):
        while True:
            connected = False
            while connected != True:
                connected = self.connect()
            
            if connected:
                self.send()
                jsonData = self.receive()
                if jsonData != []:
                    self.save_sd.insert_sensor_data(jsonData)
                    s = "y\n"
                    b = bytearray()
                    b.extend(s.encode())
                    self.cli_sock.mysend(b)
            if self.sock != None:
                self.sock.close
            time.sleep(20)
        
blue = Blue()
atexit.register(blue.close_cli_sock)
blue.loop()
