
// #include <stdio.h>
// #include <string.h>
#include <ESP8266HTTPClient.h>
#include <WiFiClient.h>
#include <ESP8266WiFi.h>
#include <ArduinoJson.h>

#include <DHT.h> //libary sensor dht 11(sensor suhu dan kelembapan)
#define DHTPIN 14  
#define DHTTYPE DHT11

#include <Adafruit_BMP085.h>  //libary sensor tekanan
#define seaLevelPressure_hPa 1013.25


DHT dht(DHTPIN, DHTTYPE);
Adafruit_BMP085 bmp;

const char *ssid= "your ssid";
const char *pass= "123456789abcd";
const String ipAddressServer="http://192.168.101.101:5000/sensing";
const char *identifier="AAAC";
const char *token="nNOGdEmMjT";

int interval=100;
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

  String responseMSG=doSensingAndSend();
  processResponse(responseMSG);

  delay(interval);
}


void processResponse(String responseMSG){
  String action=getAction(responseMSG);
  if(action.equalsIgnoreCase("result")){
    int i=2;
  }else if(action.equalsIgnoreCase("setInterval")){
    setInterval(responseMSG);
  }
}


void setInterval(String responseMSG){
  String intervalStr=responseMSG.substring(15,responseMSG.length()-1); //15 untuk membuang action dan length -2 untuk membuang }
  interval=intervalStr.toInt();
}



String getAction(String responseMSG){
  int posisi=0;
  bool valid=false; //untuk mengecek apakah formatnya valid

  for (int i=0; i<responseMSG.length();i++){  
    if(responseMSG.charAt(i)==':'){
      valid=true;
      break;
    }
  posisi++;
  }

  if(valid){
    return responseMSG.substring(2,posisi-1); //mulai dari 2 untuk membuang {" dan posisi -1 untuk membuang "
  }
  return "0";
}


String doSensingAndSend(){
  StaticJsonDocument<300> JSONbuffer;

  JSONbuffer["idBS"]=identifier;

  JsonObject result = JSONbuffer.createNestedObject("result");
  result["s"]=dht.readTemperature();
  result["t"]=bmp.readPressure();
  result["k"]=dht.readHumidity() ;
  std::string akselerasi="["+std::to_string(rand()%10)+","+std::to_string(rand()%10)+","+std::to_string(rand()%10)+"]";
  result["a"]=akselerasi;


  char JsonString[300];
  serializeJson(JSONbuffer,JsonString);
  


  Serial.println("sending get");
  http.begin(client,ipAddressServer);
  http.addHeader("Content-Type", "text/plain");


  http.POST(JsonString);
  String response= http.getString();
  
  return response;
}
