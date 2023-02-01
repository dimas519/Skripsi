# 1 "d:\\SKRIPSI\\Github\\Skripsi\\Program\\WSN\\Node_Sensor\\Node_Sensor.ino"

# 3 "d:\\SKRIPSI\\Github\\Skripsi\\Program\\WSN\\Node_Sensor\\Node_Sensor.ino" 2
# 4 "d:\\SKRIPSI\\Github\\Skripsi\\Program\\WSN\\Node_Sensor\\Node_Sensor.ino" 2
# 5 "d:\\SKRIPSI\\Github\\Skripsi\\Program\\WSN\\Node_Sensor\\Node_Sensor.ino" 2
# 6 "d:\\SKRIPSI\\Github\\Skripsi\\Program\\WSN\\Node_Sensor\\Node_Sensor.ino" 2
# 7 "d:\\SKRIPSI\\Github\\Skripsi\\Program\\WSN\\Node_Sensor\\Node_Sensor.ino" 2
# 8 "d:\\SKRIPSI\\Github\\Skripsi\\Program\\WSN\\Node_Sensor\\Node_Sensor.ino" 2

const char *ssid= "your ssid";
const char *pass= "123456789abcd";
const String ipAddressServer="http://192.168.101.100";
const int destPort=5000;
const char *identifier="AAAC";

int interval=60000;
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
      Serial.println("");
      Serial.println("WiFi connected on ip:"+WiFi.localIP().toString());
}

void loop() {
  // put your main code here, to run repeatedly:

  StaticJsonDocument<300> JSONbuffer;

  JSONbuffer["idBS"]=identifier;

  JsonObject result = JSONbuffer.createNestedObject("result");
  result["s"]=(rand() % 15)+20;
  result["t"]=(rand()%100 ) +900;
  result["k"]=(rand() %100) ;
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
