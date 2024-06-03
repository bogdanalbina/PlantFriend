//temp sensor init and pin
#include "Bonezegei_DHT11.h"
Bonezegei_DHT11 dht(3);

//soil sensor pin init
int soilSensorPin = A0;
int soilSensorValue = 0;

//switch
int switchValue = 0;

//piezo pin init - I don't use this sensor
//int piezoPin = 4;

//sound sensor init
int soundSensor = A5;
int soundLevel = 0;

//instead of delay use millis
unsigned long previousMillis = 0UL;
unsigned long previousMillisFast = 0UL;
unsigned long standardInterval = 2000UL;
unsigned long fastInterval = 100UL;

int sw = 0;

//define pins and variables for ultrasonic sensor
const int trigPin = 9;  
const int echoPin = 10; 
float duration, distance;

//setting a min and max for Noise Sensor and Ultrasonic sensor
int maxSound = 0;
float minUltra = 1000;


void setup() {
  // put your setup code here, to run once:
  //ultrasonic setup
  pinMode(trigPin, OUTPUT);  
	//pinMode(echoPin, INPUT);

  //temp setup
  dht.begin();

  //Serial setup
  Serial.begin(115200);
}

void loop() {
  //temp sensor works on 2s so minimum delay must be 2000
  //piezo works continous so with 2000 is hard to detect normal movement, only for strong vibrations works
  //delay(2000);

  unsigned long currentMillis = millis();
  
  
  
  
  if(currentMillis - previousMillisFast > fastInterval) {
	  // The Arduino executes this code once every fastInterval ms
    
 	  //sound level
    soundLevel = analogRead(soundSensor);
    if (soundLevel > maxSound) {
      maxSound = soundLevel;
    }

    //ultrasonic code
    digitalWrite(trigPin, LOW);  
	  delayMicroseconds(2);  
	  digitalWrite(trigPin, HIGH);  
	  delayMicroseconds(10);  
	  digitalWrite(trigPin, LOW);

    duration = pulseIn(echoPin, HIGH);

    distance = (duration*.0343)/2;
    if (distance < minUltra) {
      minUltra = distance;
    }

 	  // Don't forget to update the previousMillis value
 	  previousMillisFast = currentMillis;
  }

  
  if (currentMillis - previousMillis > standardInterval)
  {
    switchValue = analogRead(A7);
    //delay(1);
    //switch
    if (switchValue < 500) {
      sw = 0;
    } else {sw = 1;}

    //Serial.println(sw);
    //float time = micros()/1e6; // time is currentMillis
    float temp = 0;
    
    soilSensorValue = analogRead(soilSensorPin);
    //map values from 255 to 0 (reverse so dry is low, and high is humid)
    soilSensorValue = map(soilSensorValue,0,1024,255,0);
    
    if(dht.getData()){
      temp = dht.getTemperature();
    }
    else {
      //temp error 666
      temp = 666;
      }
      
    if (!sw) {
      Serial.println(sw);
    }
    else {
    Serial.print(sw);
    Serial.print(", ");
    Serial.print(currentMillis);
    Serial.print(", ");
    Serial.print(temp,2);
    Serial.print(", " );
    //no vibroSensor needed
    //Serial.print(vibroSensorState);
    //Serial.print(", ")
    Serial.print(soilSensorValue);
    Serial.print(", ");
    Serial.print(minUltra);
    Serial.print(", ");
    Serial.println(maxSound);}
    
    
    maxSound = 0;
    minUltra = 1000;

   	previousMillis = currentMillis;
  }

  //vibration sensor state HIGH and LOW - not in use
  //int vibroSensorState = digitalRead(piezoPin);
  
}
