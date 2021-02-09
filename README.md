# Spark-Intercepter

Uses an ESP32 board (running C++ program) and a PC (running python 3) to intercept traffic from the Spark app to the Amp and back.   

This is a basic version that doesn't convert the data to meaningful commands - but that is a next step based on the communication protocol documentation and other programs in this github.   

It allows you to control the amp from the app, and also press 0-3 on your PC keyboard to select a preset - proving app, amp and other control methods can co-exist.   

I use an esp32 and the PC because I haven't yet worked out how to make something connect to the amp via bluetooth but also look like the amp via bluetooth...   

# Setup

The ESP 32 board (in this case a M5Stack Core 2) runs the Spark_Server_Core_USB_1.ino program and is connected to the PC via the USB-C serial cable
The PC runs the python 3 program SparkSpoofer2.py.

Steps:

Turn the amp off   
Power on the ESP 32 board   
On the android tablet / phone, pair to Spark 40 Audio (which is the ESP 32 board)   
Turn off the ESP 32 board   
Turn on the amp   
Connect the PC to the Spark amp via bluetooth   
Connect the ESP 32 board to the PC   
Run the python   
On the app, try to connect   

Turn knobs, change effects, see data scroll by...   

# Note
Currently this works for everything apart from the app retrieving the preset information from the amp - this traffic is blocked by the python program. For some reason that traffic causes the app to crash. Perhaps there is a checksum in there that is not ok, or something timing sensitive - but allowing the app -> amp and amp -> app traffic for a preset retrieve does not currently work. This means the amp doesn't have details of the hardware presets to select them.
