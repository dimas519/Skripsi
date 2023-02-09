
#include <stdio.h>
#include <string.h>
#include <ESP8266HTTPClient.h>
#include <WiFiClient.h>
#include <ESP8266WiFi.h>
#include <ArduinoJson.h>

#include <DHT.h> //library sensor yang telah diimportkan
#define DHTPIN 10    //Pin apa yang digunakan
#define DHTTYPE DHT11   // DHT 11

#include <Adafruit_BMP085.h>
#define seaLevelPressure_hPa 1013.25


DHT dht(DHTPIN, DHTTYPE);
Adafruit_BMP085 bmp;

const char *ssid= "your ssid";
const char *pass= "123456789abcd";
const String ipAddressServer="http://103.150.196.40:5001";
const char *identifier="AAAC";
const char *token="nNOGdEmMjT";

int interval=300000;
// int interval=1000;

HTTPClient http;
WiFiClient client;

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
      dht.begin();
      bmp.begin();


      Serial.println("");
      Serial.println("WiFi connected on ip:"+WiFi.localIP().toString()); 
}

void loop() {
  // put your main code here, to run repeatedly:

  StaticJsonDocument<300> JSONbuffer;

  JSONbuffer["idBS"]=identifier;

  JsonObject result = JSONbuffer.createNestedObject("result");
  result["s"]=dht.readTemperature();
  result["t"]=bmp.readPressure();
  result["k"]=dht.readHumidity() ;
  std::string akselerasi="["+std::to_string(rand()%10)+","+std::to_string(rand()%10)+","+std::to_string(rand()%10)+"]";
  result["a"]=akselerasi;

  char JSONmessageBuffer[300];

  serializeJson(JSONbuffer, Serial);

  
  char jsonChar[300];
  serializeJson(JSONbuffer,jsonChar);
  
  Serial.println("sending get");
  String req=ipAddressServer+"/sensing";
  http.begin(client,req);
  http.addHeader("Content-Type", "text/plain");


  int httpResponseCode = http.POST(jsonChar);
  String payload = http.getString();
  Serial.println("code get:"+payload);






  delay(interval);
}
