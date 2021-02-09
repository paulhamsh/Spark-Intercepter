# now this uses the keyboard module
# python -m pip install keyboard

import keyboard
import time
import socket
import threading
import serial
import struct
from    SparkClass import *
#import bluetooth


BAUD = 1000000

# Get from Serial and send to Spark
class ReceiverThread(threading.Thread):
    def __init__(self, my_ser, my_sock):
        threading.Thread.__init__(self)
        self.SparkSocket = my_sock
        self.AppSerial = my_ser
        self.data = b''
        
    def run(self):
        global stop_now
        
        while not stop_now:
            self.data = self.data+self.AppSerial.read(400)
            if self.data:
                if self.data[0] != 1:
                    self.data= self.data[1:]
                elif self.data[-1] == 247: 
                    print (">> %s >>" % self.data.hex())
                    cmd = self.data[20:22]
                    if cmd.hex() == "0201":
                        num = self.data[23:25]
                        print("Skipping preset request: ",cmd.hex(), " ", num.hex())
                    else:
                        self.SparkSocket.send(self.data)
                    self.data=b''
                    
        print("App -> Spark thread stopped")


# Get from Spark and send to serial            
class SenderThread(threading.Thread):
    def __init__(self, my_ser, my_sock):
        threading.Thread.__init__(self)
        self.SparkSocket = my_sock
        self.AppSerial = my_ser
        self.data = b''
        
    def run(self):
        global stop_now
                
        s = self.SparkSocket.recv(1)
        while not stop_now:
            if s == b'\x01':
                t = self.SparkSocket.recv(1)
                if t == b'\xfe':
                    self.data = s + t
                    s = self.SparkSocket.recv(5)
                    self.data = self.data + s
                    leng = int(s[4])
                    s = self.SparkSocket.recv(leng - 7)
                    self.data += s
                    print ("<< %s <<" % self.data.hex())
                    self.AppSerial.write(self.data)
                else:
                   s = t
            else:
                s = self.SparkSocket.recv(1)
                
        print("Spark -> App thread stopped")
        
class IntercepterThread(threading.Thread):
    def __init__(self, my_ser, my_sock):
        threading.Thread.__init__(self)
        self.SparkSocket = my_sock
        self.AppSerial = my_ser
        self.data = b''
        self.sc = SparkMessage()
        
    def run(self):
        global stop_now
        
        while not stop_now:
            if keyboard.is_pressed('0'):
                pres = 0
            elif keyboard.is_pressed('1'):
                pres = 1
            elif keyboard.is_pressed('2'):
                pres = 2
            elif keyboard.is_pressed('3'):
                pres = 3
            else:
                pres = -1

            if keyboard.is_pressed('q'):
                stop_now = True
        
            if pres >=0:       
                byts = self.sc.change_hardware_preset(pres)
                byts2 = byts[0][0:4] + b'\x41\xff' + byts[0][6:20]+b'\x03'+byts[0][21:]

                print("Sending change to preset %d" % pres)
                print("}} %s }}" % byts[0].hex())
 
                self.SparkSocket.send(byts[0])

                print("{{ %s {{" % byts2.hex())
        
                self.AppSerial.write(byts2)
            # now just wait a bit    
            time.sleep(0.2)
                
        print("Inter thread stopped")

def main():
    global stop_now
    stop_now = False
    
    sc = SparkMessage()
    pres = 0
    
    ser=serial.Serial("COM7", BAUD, timeout=0)
    
    print ("Connecting to Spark - 08:EB:ED:4E:47:07")
    SERVER_PORT = 2
#    spark = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
    spark = socket.socket(socket.AF_BLUETOOTH, socket.SOCK_STREAM, socket.BTPROTO_RFCOMM)
    spark.connect(("08:EB:ED:4E:47:07", SERVER_PORT))
    print ("Connected successfully")

    sendThread = SenderThread(ser, spark)
    recvThread = ReceiverThread(ser, spark)
    interThread = IntercepterThread(ser, spark)
    
    sendThread.start()
    recvThread.start()
    interThread.start()
       
    sendThread.join()
    recvThread.join()
    interThread.join()

    print("Finished")
    ser.close()
    spark.close()

    
if __name__ == "__main__":
        main()
