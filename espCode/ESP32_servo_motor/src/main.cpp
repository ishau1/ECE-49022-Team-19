#include <Arduino.h>
#include <ESP32Servo.h>

Servo myservo_base;  // create servo object to control a servo
// 16 servo objects can be created on the ESP32
Servo myservo_elbow;
Servo myservo_arm1;

int pos = 0;    // variable to store the servo position
// Recommended PWM GPIO pins on the ESP32 include 2,4,12-19,21-23,25-27,32-33 
// Possible PWM GPIO pins on the ESP32-S3: 0(used by on-board button),1-21,35-45,47,48(used by on-board LED)

int servoPin_base = 13;
int servoPin_elbow = 15;
int servoPin_arm1 = 16;   
int servoPin_arm2 = 17;  // 17, 18, 3, 6, not working
int servoPin_gripper = 14;
//
int LED_Shine = 37;

void setup() {
	// Allow allocation of all timers
	ESP32PWM::allocateTimer(0);
	ESP32PWM::allocateTimer(1);
	ESP32PWM::allocateTimer(2);
	ESP32PWM::allocateTimer(3);
	myservo_base.setPeriodHertz(50);    // standard 50 hz servo
  myservo_elbow.setPeriodHertz(50); 
  myservo_arm1.setPeriodHertz(50); 
	
  // Attaches the servo on pin 18 to the servo object
  myservo_base.attach(servoPin_base, 500, 2500); 
	myservo_elbow.attach(servoPin_elbow, 500, 2500); 
  myservo_arm1.attach(servoPin_arm1, 500, 2500); 
	//myservo.attach(servoPin_arm2, 500, 2500); 
  //myservo.attach(servoPin_gripper, 500, 2500); 

  
  
  // using default min/max of 1000us and 2000us
	// different servos may require different min/max settings
	// for an accurate 0 to 180 sweep

 pinMode(LED_Shine, OUTPUT);
}

void loop(){
  //For the first component


  //set up initial position
  myservo_base.write(0);
  delay(100);
  myservo_elbow.write(0);
  delay(100);
  myservo_arm1.write(0);
  delay(100);
  
	for (pos = 0; pos <= 180; pos += 1) { // goes from 0 degrees to 180 degrees
		// in steps of 1 degree
		myservo_base.write(pos);    // tell servo to go to position in variable 'pos'
		delay(15);             // waits 15ms for the servo to reach the position
	}

  // for(pos = 90; pos >= 20; pos -= 1){
  //   myservo_elbow.write(pos);
  //   delay(50);
  // }
  // for(pos = 20; pos <= 90; pos += 1){
  //   myservo_elbow.write(pos);
  //   delay(50);
  // }

  // for(pos = 20; pos <= 90; pos += 1){
  //   myservo_arm1.write(pos);
  //   delay(50);
  // }
  /*
	for (pos = 180; pos >= 0; pos -= 1) { // goes from 180 degrees to 0 degrees
		myservo.write(pos);    // tell servo to go to position in variable 'pos'
		delay(15);             // waits 15ms for the servo to reach the position
	}
  */
  
  //finish moving
  digitalWrite(LED_Shine, HIGH);   // turn the LED on (HIGH is the voltage level)
  delay(1000);                       // wait for a second
  digitalWrite(LED_Shine, LOW);    // turn the LED off by making the voltage LOW
  delay(1000);                       // wait for a second
}


