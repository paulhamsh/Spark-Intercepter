import time
import socket
import threading
import serial
import struct
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
        while True:
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
                    print()
                    print()


# Get from Spark and send to serial            
class SenderThread(threading.Thread):
    def __init__(self, my_ser, my_sock):
        threading.Thread.__init__(self)
        self.SparkSocket = my_sock
        self.AppSerial = my_ser
        self.data = b''
        
    def run(self):
        s = self.SparkSocket.recv(1)
        while True:
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
                    print()
                else:
                   s = t
            else:
                s = self.SparkSocket.recv(1)


def main():

    ser=serial.Serial("COM7", BAUD, timeout=0)
    
    print ("Connecting to Spark - 08:EB:ED:4E:47:07")
    SERVER_PORT = 2
#    spark = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
    spark = socket.socket(socket.AF_BLUETOOTH, socket.SOCK_STREAM, socket.BTPROTO_RFCOMM)
    spark.connect(("08:EB:ED:4E:47:07", SERVER_PORT))
    print ("Connected successfully")

    sendThread = SenderThread(ser, spark)
    recvThread = ReceiverThread(ser, spark)
    sendThread.start()
    recvThread.start()
    sendThread.join()
    recvThread.join()
        
    while True:
        time.sleep(1)

    
if __name__ == "__main__":
        main()
