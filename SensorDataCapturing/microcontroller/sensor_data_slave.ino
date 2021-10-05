#include <SoftwareSerial.h>
#include "DHT.h"
#include <string.h>

#define DHTPIN 8
#define DHTTYPE DHT11

DHT dht(DHTPIN, DHTTYPE);
SoftwareSerial Blue(2, 3);

#define SensorPin A1
String BASENAME = "test-id-1";

const int dry = 768;
const int wet = 431;

void setup() {
  Serial.begin(9600);
  dht.begin();
  Blue.begin(9600);
}
String get_soil_moisture(){
  float sensorValue = 0;
  for (int i = 0; i < 100; i++)
  {
    sensorValue = sensorValue + analogRead(SensorPin);
    delay(1);
  }
  sensorValue = sensorValue / 100.0;
  float percentageHumidity = map(sensorValue, wet, dry, 100, 0);
  
  return (String)percentageHumidity ;
}
String read_data() {
  String hum = (String)dht.readHumidity();
  Serial.println("Humidity:");
  Serial.println(String(hum));
  String temp = (String)dht.readTemperature();
  String soil = get_soil_moisture();

  String sensorData = String("[")+String("{\"bn\":\"")+String(BASENAME)
                +String("\",\"n\":\"temp\",\"u\":\"C\",\"v\":")+String(temp)+String("},")
                +String("{\"n\":\"humidity\",\"u\":\"P\",\"v\":")+String(hum)+String("},")
                +String("{\"n\":\"soil\",\"u\":\"P\",\"v\":")+String(soil)+String("}]");
  return sensorData;
} 


void loop() {
  delay(100);
  char data ='y';
  while (Blue.available()>0) {
     data = Blue.read();
  }
    delay(200);
    Serial.println("Received");
    Serial.println(data);
    if (data == 'x') {
      Serial.println("recieved x");
      String stringData = read_data();
      for(int i = 0; i<stringData.length(); i++){
        Serial.println("next byte");
        Blue.write(stringData[i]);
      }
      Blue.write("\n");
      
    
  }
  delay(300);
}
