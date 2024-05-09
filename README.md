# Surveillance System

## Hardware and Software Requirements
Hardware Requirements: 1 Raspberry Pi 4 Board, 2 Raspberry Pi Cameras Module v2, 1 Arducam Multi Camera Adapter Module V2.2, 1 USB Flash Drive, Keyboard and Mouse, SD Card, 3 LEDs, 1 buzzer, 1 button, cables, and wires.

Software Requirements: Raspberry Pi Imager, OpenCV, Picamera2, and Flask.

## Instructions
Follow the below instructions to ensure that the system runs correctly.

The setup of the Raspberry Pi board will require working operating system to be installed in the microSD card to plug in the board. The Raspberry Pi OS for setup of the Raspberry Pi board can be facilitated by the Raspberry Pi Imager, a tool that simplifies the OS installation process on the microSD card. This software supports various OS options, but you can primarily use Raspberry Pi OS for its lightweight nature and robust support.

Insert the SD card into the Micro SD Card slot in the Raspberry Pi board, then perform the setup for the system as shown in the following picture:
![System Setup](https://github.com/anhtu-pham/Surveillance-System/blob/main/assets/system_setup.jpg)

Use the HDMI cable to connect to the monitor, connect the mouse and keyboard to the Raspberry Pi board, power up the Raspberry Pi board, then turn on the monitor.

All images and videos that the system would store will be in corresponding directories in the /media/ecse488-7/group7 directory for the USB Flash Drive. With the monitor's user interface, create this directory, then inside this directory, create /images and /videos directories to store images and videos respectively.

On the monitor's user interface, open up 2 terminals, the first terminal to run the system's central functionalities and the second terminal to run the website for manual settings of the system.

On the first terminal, change directory into src, then execute the following command to run the system's central functionalities:
```
sudo python3 driver.py
```
In the state with the highest level of security, the system would activate alarm with the LEDs and the buzzer. In this state, reset the system and turn off the alarm by firm reset press on the button.

Turn on the Wi-Fi connection, then on the second terminal, change directory into src, then execute the following command to run the website:
```
python3 app.py
```
Open the browser and use the link displayed in the message on the second terminal to open the website.
