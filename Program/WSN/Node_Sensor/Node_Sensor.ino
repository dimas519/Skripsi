
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
const char *pass= "<example password>";

const String ipAddressServer="http://192.168.101.11:5000";
const char *identifier="AAAA";
const char *token="0KTjKCgtda";

int interval=300000; //tidak pakai PROGMEM dan EEPROM karena keduanya hanya memiliki limit tulis 10.000 dan 100.000 saja


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

      Serial.println("Trying to getIntervalSensing");
      
      String takeConf="{\"idBS\":\"";
      takeConf+=identifier;
      takeConf+="\"}";
      Serial.print("arguments ");
      Serial.println(takeConf);

      String endpoint=ipAddressServer+"/interval";
      http.begin(client,endpoint);
      http.addHeader("Content-Type", "text/plain");
      http.POST(takeConf);
      String responseMSG= http.getString();
      processResponse(responseMSG);

      

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
  interval=interval*1000;
  Serial.print("new Interval :");
  Serial.println(interval);
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
  Serial.print("sending get: ");
  Serial.print(JsonString);

  String endpoint=ipAddressServer+"/sensing";
  http.begin(client,endpoint);
  http.addHeader("Content-Type", "text/plain");


  http.POST(JsonString);
  String responseMSG= http.getString();
  Serial.print(" response: ");
  Serial.println(responseMSG);

  return responseMSG;
}
