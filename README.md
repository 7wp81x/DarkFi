# DarkFi

## Disclaimer!!!
**This project is for testing and educational purposes. Use this on your own device or network. I don't take any responsibility for what you do with this program.**

## About this project
This is basically fake captive portal for NodeMCU (ESP8266 Module) with DNS spoofing. When you are connected to the AP It ask for social media credential in exchange of "**FREE INTERNET ACCESS**" it also allows you to host and display your own pages to captive portal without having root acess.
### How it works?
<p>
Simple. The ESP8266 creates a captive portal, then the captive portal redirects all clients to a local IP address which where the webpages is hosted **(192.168.0.100:8080)**.
Instead of displaying the webpages that inside ESP8266 which is ugly because you need to flash again to change the page. So why not redirect it to a local IP then host pages there.
</p>

# Features
- Change ESP8266 SSID
- Host own custom webpages
- DNS Hijacking

# Screenshots
<table>
  <tr>
    <th>Main menu</th>
    <th>Main server log</th> 
    <th>Main Captive portal page</th>
  </tr>
  <tr>
    <td><img src="https://raw.githubusercontent.com/Mrp1r4t3/DarkFi/main/screenshots/src1.jpg" title="menu"></td>
    <td><img src="https://raw.githubusercontent.com/Mrp1r4t3/DarkFi/main/screenshots/src2.jpg" title="log"></td>
    <td><img src="https://raw.githubusercontent.com/Mrp1r4t3/DarkFi/main/screenshots/src3.jpg" title="page"></td>
  </tr>
</table>


# Esp8266 Setup
### Flash using windows
1. Download ESP8266 [Flash Download Tools](https://www.espressif.com/en/support/download/other-tools).
2. Flash the `bin/DarkFi.bin` to your ESP8266.

### Flash using Android
1. Download [ESP8266 Loader](https://apkpure.com/esp8266-loader-blynk-uploader/com.bluino.esploader)
2. Connect to esp8266 using OTG cable
3. Upload the `bin/DarkFi.bin`

# Termux setup
```pkg install git python python-pip -y
git clone https://github.com/Mrp1r4t3/DarkFi
cd DarkFi/
sh install.sh
```
