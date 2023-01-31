#include <Arduino.h>
#line 1 "d:\\SKRIPSI\\Github\\Skripsi\\Program\\WSN\\Node_Sensor\\Node_Sensor.ino"
#include <ESP8266HTTPClient.h>
#include <WiFiClient.h> 
#include <ESP8266WiFi.h>
#include <ArduinoJson.h>

const char *ssid= "yourssid";
const char *pass= "123456789abcd";
const char *ipAddressServer="192.168.101.100";
const int destPort=5000;
const char *identifier="AAAC";

// int interval=300000;
int interval=1000;

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
    delay(10);
               
       Serial.println("Connecting to ");
       Serial.println(ssid); 
 
       WiFi.begin(ssid, pass); 
       while (WiFi.status() != WL_CONNECTED) 
          {
            
            delay(500);
            Serial.print(".");
          }
      Serial.println("");
      Serial.println("WiFi connected on ip:"+WiFi.localIP().toString()); 
      udp.begin(4321); //source port
}

void loop() {
  // put your main code here, to run repeatedly:

  StaticJsonBuffer<300> JSONbuffer;
  JsonObject& JSONencoder = JSONbuffer.createObject();

  JSONencoder["idBS"]=Identifier;

  JsonArray& values = JSONencoder.createNestedArray("result");
  values['1']=30;
  values['2']=30;
  values['3']=40;
  values['4']=80;

  char JSONmessageBuffer[300];
  JSONencoder.prettyPrintTo(JSONmessageBuffer, sizeof(JSONmessageBuffer));

  Serial.println(JSONmessageBuffer);

  delay(interval);
}

