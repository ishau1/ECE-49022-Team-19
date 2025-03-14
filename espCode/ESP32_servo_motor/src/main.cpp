#include <Arduino.h>
#include <ESP32Servo.h>

//Function Declaration
void SetInitialPos();
void move_arm(int type);
void grab_Pos();
void write_pos(int, int, int, int, int); // This is the Simple one
void write_Pos(int, int, int, int, int, int, int, int, int, int); // The Complex one for movements
void write_Pos_Back(int, int, int, int, int, int, int, int, int, int); // The Complex one for movements back

// create servo object to control a servo
// 16 servo objects can be created on the ESP32
Servo myservo_base;  
Servo myservo_elbow;
Servo myservo_arm;
Servo myservo_wrist;
Servo myservo_gripper;

int pos = 0;              // variable to store the servo position
                          
int servoPin_base = 13;
int servoPin_elbow = 15;
int servoPin_arm = 16;   
int servoPin_wrist = 17;  // 17, 18, 3, 6, not working
int servoPin_gripper = 14;

int LED_Shine = 18;

void setup() {
  
	// Allow allocation of all timers
	ESP32PWM::allocateTimer(0);
	ESP32PWM::allocateTimer(1);
	ESP32PWM::allocateTimer(2);
	ESP32PWM::allocateTimer(3);
	myservo_base.setPeriodHertz(50);    // standard 50 hz servo
  myservo_elbow.setPeriodHertz(50); 
  myservo_arm.setPeriodHertz(50); 
  myservo_wrist.setPeriodHertz(50); 
  myservo_gripper.setPeriodHertz(50);

	
  // Attaches the servo on pin 18 to the servo object
  // using default min/max of 1000us and 2000us
	// different servos may require different min/max settings
	// for an accurate 0 to 180 sweep
  myservo_base.attach(servoPin_base, 500, 2500); 
	myservo_elbow.attach(servoPin_elbow, 500, 2500); 
  myservo_arm.attach(servoPin_arm, 500, 2500); 
	myservo_wrist.attach(servoPin_wrist, 400, 2600);        //-< change the range of wrist
  myservo_gripper.attach(servoPin_gripper, 500, 2500); 

  
  Serial.begin(115200);  // Start serial communication at 115200 baud rate
  // while (!Serial);       // Wait for serial to initialize (optional, useful for debugging)
  delay(1000);
  Serial.println("ESP32 Serial Communication Started");

  
  //Set Initial Position
  SetInitialPos();
  delay(1000);

/*  
  //Check Base
  for (pos = 5; pos <= 5; pos += 1) { // goes from 5 degrees to 100 degrees
		// in steps of 1 degree
		myservo_base.write(pos);    
		delay(15);             // waits 15ms for the servo to reach the position
	}  
  delay(1000);

  //Check Elbow: - lean forward, + lean backward 
  for (pos = 90; pos >= 15; pos -= 1) { // goes from 90 degrees to 60 degrees
		myservo_elbow.write(pos);    // tell servo to go to position in variable 'pos'
		delay(15);             // waits 15ms for the servo to reach the position
	}  
  delay(1000);

  //Check Arm: + lean forward, - lean backward
  for (pos = 100; pos <= 140; pos += 1) { // goes from 100 degrees to 120 degrees
		// in steps of 1 degree
		myservo_arm.write(pos);    // tell servo to go to position in variable 'pos'
		delay(15);             // waits 15ms for the servo to reach the position
	}  
  delay(1000);

  // Check Wrist: + counterclock, -clock
  for (pos = 80; pos <= 80; pos += 1) { 
		// in steps of 1 degree
		myservo_wrist.write(pos);    
		delay(15);             // waits 15ms for the servo to reach the position
	}  
*/
  
  // Type 1
  //        Base   Elbow   Arm   Wrist  Gripper
  write_Pos(5,5, 70,15, 100,140, 80,80, 0,0);  // initialized position -> grasp position
  
  write_Pos(5,58, 15,65, 140,110, 80,200, 0,0);  // grasp position -> bin position 1
  
  write_Pos_Back(58,5, 65,15, 110,140, 200,80, 0,0);  // bin position 1 -> grasp position
  
  // Type 2
  //        Base   Elbow   Arm   Wrist  Gripper  
  write_Pos(5,70, 15,65, 140,110, 80,200, 0,0);  // grasp position -> bin position 2

  write_Pos_Back(70,5, 65,15, 110,140, 200,80, 0,0);  // bin position 2 -> grasp position

  // Type 3
  //        Base   Elbow   Arm   Wrist  Gripper  
  write_Pos(5,85, 15,65, 140,110, 80,200, 0,0);  // grasp position -> bin position 3

  write_Pos_Back(85,5, 65,15, 110,140, 200,80, 0,0);  // bin position 3 -> grasp position

  
  // Type 4
  //        Base   Elbow   Arm   Wrist  Gripper  
  write_Pos(5,100, 15,65, 140,110, 80,200, 0,0);  // grasp position -> bin position 3

  write_Pos_Back(100,5, 65,15, 110,140, 200,80, 0,0);  // bin position 3 -> grasp position

  // Type 5
  //        Base   Elbow   Arm   Wrist  Gripper  
  write_Pos(5,115, 15,45, 140,110, 80,200, 0,0);  // grasp position -> bin position 3

  write_Pos_Back(115,5, 45,15, 100,140, 200,80, 0,0);  // bin position 3 -> grasp position

  // Type 6
  //        Base   Elbow   Arm   Wrist  Gripper  
  write_Pos(5,130, 15,45, 140,110, 80,200, 0,0);  // grasp position -> bin position 3

  write_Pos_Back(130,5, 45,15, 110,140, 200,80, 0,0);  // bin position 3 -> grasp position

 // Set LED Pin output
 pinMode(LED_Shine, OUTPUT);
}

void loop(){
  //begin moving
  digitalWrite(LED_Shine, HIGH);   // turn the LED on (HIGH is the voltage level)
  delay(1000);                       // wait for a second
  digitalWrite(LED_Shine, LOW);    // turn the LED off by making the voltage LOW
  delay(1000);                       // wait for a second


  int type = 1;
  //grab_Pos();
  // move_arm(type);

  delay(3000);

}


void move_arm(int type) {
  grab_Pos();    // Set to the grap position

  delay(3000);
  switch(type){
     case 1:
      write_Pos(5,45, 15,50, 140,140, 90,0, 0,0);
      break;
  //   myservo_elbow.write(80);  
  //   delay(100);
  //   myservo_arm.write(120);   
  //   delay(100);
  //   myservo_base.write(45);    
  //   delay(100);
  //   myservo_wrist.write(50);  
  //   delay(1000);
  }
  // grab_Pos();    // Set to the grap position

}

void write_Pos(int base_pos_1, int base_pos_2,int elbow_pos_1,int elbow_pos_2,
               int arm_pos_1, int arm_pos_2, int wrist_pos_1, int wrist_pos_2,
               int gripper_pos_1, int gripper_pos_2) {
 
  //Check Elbow: - lean forward, + lean backward 
  if(elbow_pos_1 >= elbow_pos_2) {
    for (pos = elbow_pos_1; pos >= elbow_pos_2; pos -= 1) { // goes from 90 degrees to 60 degrees
      Serial.print("Elbow: In the first branch!, angle: ");
      Serial.println(pos);
      myservo_elbow.write(pos);    
      delay(30);             
    } 
  } else {
    for (pos = elbow_pos_1; pos <= elbow_pos_2; pos += 1) { // goes from 90 degrees to 60 degrees
      Serial.print("Elbow: In the 2nd branch!");
      myservo_elbow.write(pos);    
      delay(30);             
    } 
  }
  delay(100);

  //Check Arm: + lean forward, - lean backward

  if(arm_pos_1 <= arm_pos_2) {
    for (pos = arm_pos_1; pos <= arm_pos_2; pos += 1) { // goes from 100 degrees to 120 degrees
      // in steps of 1 degree
      Serial.print("Arm: In the first branch!, angle: ");
      Serial.println(pos);
      myservo_arm.write(pos);    // tell servo to go to position in variable 'pos'
      delay(15);             
    }  
  }else {
    for (pos = arm_pos_1; pos >= arm_pos_2; pos -= 1) { // goes from 100 degrees to 120 degrees
      // in steps of 1 degree
      Serial.print("Arm: In the 2nd branch!, angle: ");
      Serial.println(pos);
      myservo_arm.write(pos);    // tell servo to go to position in variable 'pos'
      delay(15);             
    }  
  }

  delay(100);

  //Check Base: + counterclock, - lean clockwise
  // Base same as initial position, goes from 5 degrees to 5 degrees

  if(base_pos_1 <= base_pos_2){
    for (pos = base_pos_1; pos <= base_pos_2; pos += 1) { // goes from 90 degrees to 60 degrees
      Serial.print("Base: In the first branch!, angle: ");
      Serial.println(pos);
      myservo_base.write(pos);    
      delay(15);
    }
  }else {
    for (pos = base_pos_1; pos >= base_pos_2; pos -= 1) { // goes from 90 degrees to 60 degrees
      Serial.print("Base: In the 2nd branch!, angle: ");
      Serial.println(pos);
      myservo_base.write(pos);    
      delay(15);
  }
}
delay(100);


// Check Wrist: + counterclock, -clock
if(wrist_pos_1 <= wrist_pos_2) {
  for (pos = wrist_pos_1; pos <= wrist_pos_2; pos += 1) { 
    // in steps of 1 degree
    myservo_wrist.write(pos);    
    delay(15);             
  } 
}else {
  for (pos = wrist_pos_1; pos >= wrist_pos_2; pos -= 1) { 
    // in steps of 1 degree
    myservo_wrist.write(pos);    
    delay(15);             
  } 
}
delay(100);
}

void write_Pos_Back(int base_pos_1, int base_pos_2,int elbow_pos_1,int elbow_pos_2,
  int arm_pos_1, int arm_pos_2, int wrist_pos_1, int wrist_pos_2,
  int gripper_pos_1, int gripper_pos_2) {


// Check Wrist: + counterclock, -clock
if(wrist_pos_1 <= wrist_pos_2) {
  for (pos = wrist_pos_1; pos <= wrist_pos_2; pos += 1) { 
  // in steps of 1 degree
  myservo_wrist.write(pos);    
  delay(15);             
} 
}else {
  for (pos = wrist_pos_1; pos >= wrist_pos_2; pos -= 1) { 
  // in steps of 1 degree
  myservo_wrist.write(pos);    
  delay(15);             
  } 
}

delay(100);

//Check Base: + counterclock, - lean clockwise
// Base same as initial position, goes from 5 degrees to 5 degrees

if(base_pos_1 <= base_pos_2){
  for (pos = base_pos_1; pos <= base_pos_2; pos += 1) { // goes from 90 degrees to 60 degrees
  Serial.print("Base: In the first branch!, angle: ");
  Serial.println(pos);
  myservo_base.write(pos);    
  delay(15);
}
}else {
  for (pos = base_pos_1; pos >= base_pos_2; pos -= 1) { // goes from 90 degrees to 60 degrees
  Serial.print("Base: In the 2nd branch!, angle: ");
  Serial.println(pos);
  myservo_base.write(pos);    
  delay(15);
}
}

delay(100);

//Check Elbow: - lean forward, + lean backward 
if(elbow_pos_1 >= elbow_pos_2) {
  for (pos = elbow_pos_1; pos >= elbow_pos_2; pos -= 1) { // goes from 90 degrees to 60 degrees
  Serial.print("Elbow: In the first branch!, angle: ");
  Serial.println(pos);
  myservo_elbow.write(pos);    
  delay(30);             
} 
} else {
  for (pos = elbow_pos_1; pos <= elbow_pos_2; pos += 1) { // goes from 90 degrees to 60 degrees
  Serial.print("Elbow: In the 2nd branch!");
  myservo_elbow.write(pos);    
  delay(30);             
} 
}

delay(100);

//Check Arm: + lean forward, - lean backward

if(arm_pos_1 <= arm_pos_2) {
  for (pos = arm_pos_1; pos <= arm_pos_2; pos += 1) { // goes from 100 degrees to 120 degrees
  // in steps of 1 degree
  Serial.print("Arm: In the first branch!, angle: ");
  Serial.println(pos);
  myservo_arm.write(pos);    // tell servo to go to position in variable 'pos'
  delay(15);             
}  
}else {
  for (pos = arm_pos_1; pos >= arm_pos_2; pos -= 1) { // goes from 100 degrees to 120 degrees
  // in steps of 1 degree
  Serial.print("Arm: In the 2nd branch!, angle: ");
  Serial.println(pos);
  myservo_arm.write(pos);    // tell servo to go to position in variable 'pos'
  delay(15);             
}  
}

delay(100);

}

void grab_Pos(){
  write_Pos(5,5, 90,15, 100,140, 80,80, 0,0);
}

void SetInitialPos(){  
  // Set Initial Position
  delay(15);
  myservo_base.write(5);    //Initial Pos of Base is 5 degree
  delay(50);
  myservo_elbow.write(70);  //Initial Pos of Elbow is 90 degree
  delay(50);
  myservo_arm.write(100);   //Initial Pos of Arm is 100 degree
  delay(50);
  myservo_wrist.write(80);  //Initial Pos of Wrist is 80 degree
  delay(50);
  myservo_gripper.write(0);
  delay(50);
}

// Move the Robotic Arm to the component grabbing position
void grabPos() {
  //Check Base
  // Base same as initial position, goes from 5 degrees to 5 degrees
  myservo_elbow.write(5); 

  //Check Elbow: - lean forward, + lean backward 
  for (pos = 90; pos >= 30; pos -= 1) { // goes from 90 degrees to 60 degrees
		myservo_elbow.write(pos);    
		delay(50);             
	}  
  delay(1000);
  
  //Check Arm: + lean forward, - lean backward
  for (pos = 100; pos <= 120; pos += 1) { // goes from 100 degrees to 120 degrees
		// in steps of 1 degree
		myservo_arm.write(pos);    // tell servo to go to position in variable 'pos'
		delay(500);             
	}  
  delay(1000);

  // Check Wrist: + counterclock, -clock
  for (pos = 80; pos <= 120; pos += 1) { 
		// in steps of 1 degree
		myservo_wrist.write(pos);    
		delay(500);             
	} 
}

void write_pos(int base_pos, int elbow_pos, int arm_pos, int wrist_pos, int gripper_pos) {
  myservo_base.write(base_pos);    
  delay(100);
  myservo_elbow.write(elbow_pos);  
  delay(100);
  myservo_arm.write(arm_pos);   
  delay(100);
  myservo_wrist.write(wrist_pos);  
  delay(100);
  myservo_gripper.write(gripper_pos);
  delay(100);
}
