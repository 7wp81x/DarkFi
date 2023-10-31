# DarkFi
DarkFi is an simple tool to host fake cative portal on android with the help of ESP8266 and Termux app without root access.
<p align="center">
  <img src="https://i0.wp.com/randomnerdtutorials.com/wp-content/uploads/2022/11/ESP8266-12E-NodeMCU-kit-development-board.jpg?w=620&quality=100&strip=all&ssl=1">
</p><br>

## Disclaimer
This project is for testing and educational purposes. I don't take any responsibility for what you do with this program.


## Features
- Change ESP8266 SSID
- Host own custom webpages
- DNS Hijacking

## Screenshots

## Esp8266 Setup
### Flash using windows
1. Download ESP8266 [Flash Download Tools](https://www.espressif.com/en/support/download/other-tools).
2. Flash the `DarkFi.bin` to your ESP8266.

### Flash using Android
1. Download [ESP8266 Loader](https://apkpure.com/esp8266-loader-blynk-uploader/com.bluino.esploader)
2. Connect to esp8266 using OTG cable
3. Upload the `DarkFi.bin`

## Termux setup
```pkg install git python python-pip -y
git clone https://github.com/Mrp1r4t3/DarkFi
cd DarkFi/
sh install.sh
```
