# Spark-Intercepter

Uses an ESP32 board (running C++ program) and a PC (running python 3) to intercept traffic from the Spark app to the Amp and back.

This is a basic version that doesn't convert the data to meaningful commands - but that is a next step based on the communication protocol documentation and other programs in this github

# Setup

The ESP 32 board (in this case a M5Stack Core 2) runs the Spark    .ino program and is connected to the PC via the USB-C serial cable
The PC runs the python 3 program.

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
