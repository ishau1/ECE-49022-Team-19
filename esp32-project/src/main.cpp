#include <Arduino.h>
#include <ESP32Servo.h> // <---- Added Code

// Define LED pins
#define LED_1 4  // Available GPIO Pins
#define LED_2 5  //
#define LED_3 16 //
#define LED_4 18 //
#define LED_5 3  //

// PWM configuration
#define PWM_CHANNEL_1 0
#define PWM_CHANNEL_2 1
#define PWM_CHANNEL_3 2
#define PWM_CHANNEL_4 3
#define PWM_CHANNEL_5 4

#define PWM_FREQ 5000
#define PWM_RESOLUTION 12 // 8-bit resolution (0-255) ----< change on 4/24

// <---- Added Code
//Fuction Declaration
void SetInitialPos();
void move_arm(int type);
void write_Pos(int, int, int, int, int, int, int, int, int, int); // The Complex one for movements
void write_Pos_Back(int, int, int, int, int, int, int, int, int, int); // The Complex one for movements back

// create servo object to control a servo
// 16 servo objects can be created on the ESP32
Servo myservo_base;  
Servo myservo_elbow;
Servo myservo_arm;
Servo myservo_wrist;
Servo myservo_gripper;
                          
int servoPin_base  = 13;        // change the pin
int servoPin_elbow = 15;
int servoPin_arm   = 16;   
int servoPin_wrist = 17;  
int servoPin_gripper = 14;

int pos = 0;
int LED_Shine = 13;             // change the LED pin 18-》13
int type_Int;
// <---- Added Code

void servo1()
{
    Serial.println("Setting LED 4 (PWM 20%)");
    ledcWrite(PWM_CHANNEL_1, 15); // 20%
}

void servo2()
{
    Serial.println("Setting LED 5 (PWM 40%)");
    ledcWrite(PWM_CHANNEL_2, 50); // 40%
}

void servo3()
{
    Serial.println("Setting LED 16 (PWM 60%)");
    ledcWrite(PWM_CHANNEL_3, 120); // 60%
}

void servo4()
{
    Serial.println("Setting LED 18 (PWM 80%)");
    ledcWrite(PWM_CHANNEL_4, 180); // 80%
}

void servo5()
{
    Serial.println("Setting LED 3 (PWM 100%)");
    ledcWrite(PWM_CHANNEL_5, 255); // 100%
}

void setup()
{
    Serial.begin(115200);
    Serial.println("ESP32 Ready, waiting for classification...");

    // Configure PWM
    ledcSetup(PWM_CHANNEL_1, PWM_FREQ, PWM_RESOLUTION);
    ledcSetup(PWM_CHANNEL_2, PWM_FREQ, PWM_RESOLUTION);
    ledcSetup(PWM_CHANNEL_3, PWM_FREQ, PWM_RESOLUTION);
    ledcSetup(PWM_CHANNEL_4, PWM_FREQ, PWM_RESOLUTION);
    ledcSetup(PWM_CHANNEL_5, PWM_FREQ, PWM_RESOLUTION);

    // Attach LEDs
    ledcAttachPin(LED_1, PWM_CHANNEL_1);
    ledcAttachPin(LED_2, PWM_CHANNEL_2);
    ledcAttachPin(LED_3, PWM_CHANNEL_3);
    ledcAttachPin(LED_4, PWM_CHANNEL_4);
    ledcAttachPin(LED_5, PWM_CHANNEL_5);


    //<===== Robotic Arm: Added Code
    
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
	myservo_wrist.attach(servoPin_wrist, 500, 2500);        //-< change the range of wrist
    myservo_gripper.attach(servoPin_gripper, 500, 2500); 

      
    SetInitialPos();                            //Set Initial Position
    // delay(1000);
    write_Pos(5,5, 40,15, 140,140, 80,80, 0,0); // initialized position -> grasp position
    //<======= Robotic Arm Added Code end

    Serial.println("Set up Finished");
}

void loop()
{
    // Send "READY" every second
    static unsigned long lastReadyTime = 0;

    if (millis() - lastReadyTime >= 1000)
    {
        Serial.println("READY");
        lastReadyTime = millis();
    }

    // Check for new data
    if (Serial.available())
    {
        String classification = Serial.readStringUntil('\n');
        classification.trim();

        if (classification.length() == 0)
        {
            return;
        }

        Serial.println("Received classification: " + classification);
        /*
        ledcWrite(PWM_CHANNEL_1, 0);
        ledcWrite(PWM_CHANNEL_2, 0);
        ledcWrite(PWM_CHANNEL_3, 0);
        ledcWrite(PWM_CHANNEL_4, 0);
        ledcWrite(PWM_CHANNEL_5, 0);

        // Classification
        if (classification == "1")
        {
            servo1();
        }
        else if (classification == "2")
        {
            servo2();
        }
        else if (classification == "3")
        {
            servo3();
        }
        else if (classification == "4")
        {
            servo4();
        }
        else if (classification == "5")
        {
            servo5();
        }
        else if (classification == "6")
        {
            Serial.println("Error :(");
        }
        else if (classification == "end")
        {
            Serial.println("Received 'end' - Stopping processing.");
        }
        */

        // <==== Added Code: Robotic Arm Movement
        int classification_Int = classification.toInt(); // <==  Convert input to INT type

        if (classification_Int <= 0 | classification_Int > 14)
        {
            Serial.print("Not a valid type number");
        }
        else
        {
            Serial.print("Begin to move with Type: ");
            Serial.print(classification_Int);

            move_arm(classification_Int);
        }

        // 1-second delay to model robotic arm movement
        delay(100);
        // <==== Added Code End: Robotic Arm Movement 

        // Send "READY" to receive next classification
        Serial.println("READY");
    }
}

// Move the arm to target location 
// INPUT: int type -- The type of the component 
void move_arm(int type) {

    // delay(1000);
    switch(type){
      case 1:
        //        Base   Elbow   Arm   Wrist  Gripper
        write_Pos(5,55, 15,12, 140,110, 80,200, 0,0);  // grasp position -> bin position 1
        write_Pos_Back(55,5, 12,15, 110,140, 200,80, 0,0);  // bin position 1 -> grasp position
        // Serial.print("");
        break;
  
      case 2: 
      //        Base   Elbow   Arm   Wrist  Gripper  
      write_Pos(5,70, 15,15, 140,110, 80,200, 0,0);  // grasp position -> bin position 2
      write_Pos_Back(70,5, 15,15, 110,140, 200,80, 0,0);  // bin position 2 -> grasp position
      break;
  
      case 3:
      //        Base   Elbow   Arm   Wrist  Gripper  
      write_Pos(5,85, 15,15, 140,110, 80,200, 0,0);  // grasp position -> bin position 3
      write_Pos_Back(85,5, 15,15, 110,140, 200,80, 0,0);  // bin position 3 -> grasp position
      break;
  
      case 4:
       //        Base   Elbow   Arm   Wrist  Gripper  
      write_Pos(5,100, 15,15, 140,110, 80,200, 0,0);  // grasp position -> bin position 3
      write_Pos_Back(100,5, 15,15, 110,140, 200,80, 0,0);  // bin position 3 -> grasp position
      break;
  
      case 5:
      //        Base   Elbow   Arm   Wrist  Gripper
      write_Pos(5,115, 15,15, 140,110, 80,200, 0,0);  // grasp position -> bin position 3
      write_Pos_Back(115,5, 15,15, 100,140, 200,80, 0,0);  // bin position 3 -> grasp position
      break;
  
      case 6:
      write_Pos(5,125, 15,15, 140,110, 80,200, 0,0);  // grasp position -> bin position 3
      write_Pos_Back(125,5, 15,15, 110,140, 200,80, 0,0);  // bin position 3 -> grasp position  
      break;

      case 13:
      //        Base   Elbow   Arm   Wrist  Gripper --- 1
      write_Pos(5,50, 15,50, 140,150, 80,200, 0,0);  // grasp position -> bin position 3
      // write_Pos(5,50, 15,50, 140,150, 80,200, 0,0);  // grasp position -> bin position 3
      write_Pos_Back(50,5, 50,15, 150,140, 200,80, 0,0);  // bin position 3 -> grasp position  
      break;

      
      case 8:
      //        Base   Elbow   Arm   Wrist  Gripper --- 2
      write_Pos(5,68, 15,50, 140,150, 80,200, 0,0);  // grasp position -> bin position 3
      write_Pos_Back(68,5, 50,15, 150,140, 200,80, 0,0);  // bin position 3 -> grasp position  
      break;

      case 9:
      //        Base   Elbow   Arm   Wrist  Gripper --- 3
      write_Pos(5,83, 15,50, 140,150, 80,200, 0,0);  // grasp position -> bin position 3
      write_Pos_Back(83,5, 50,15, 150,140, 200,80, 0,0);  // bin position 3 -> grasp position  
      break;

      case 10:
      //        Base   Elbow   Arm   Wrist  Gripper --- 4
      write_Pos(5,100, 15,50, 140,150, 80,200, 0,0);  // grasp position -> bin position 3
      write_Pos_Back(100,5, 50,15, 150,140, 200,80, 0,0);  // bin position 3 -> grasp position  
      break;

      case 11:
      //        Base   Elbow   Arm   Wrist  Gripper --- 5
      write_Pos(5,115, 15,50, 140,150, 80,200, 0,0);  // grasp position -> bin position 3
      write_Pos_Back(115,5, 50,15, 150,140, 200,80, 0,0);  // bin position 3 -> grasp position  
      break;

      case 12:
      //        Base   Elbow   Arm   Wrist  Gripper --- 6
      write_Pos(5,130, 15,50, 140,150, 80,200, 0,0);  // grasp position -> bin position 3
      write_Pos_Back(130,5, 50,15, 150,140, 200,80, 0,0);  // bin position 3 -> grasp position  
      break;
      
      case 7:  // Test
      //        Base   Elbow   Arm   Wrist  Gripper --- 6
      write_Pos(5,180, 15,30, 140,150, 80,200, 0,0);  // grasp position -> bin position 3
      write_Pos_Back(180,5, 30,15, 150,140, 200,80, 0,0);  // bin position 3 -> grasp position  
      break;
      
      // Set LED Pin output
      pinMode(LED_Shine, OUTPUT);
    }
}

void write_Pos(int base_pos_1, int base_pos_2, int elbow_pos_1, int elbow_pos_2,
               int arm_pos_1, int arm_pos_2, int wrist_pos_1, int wrist_pos_2,
               int gripper_pos_1, int gripper_pos_2)
{

    // Check Elbow: - lean forward, + lean backward
    if (elbow_pos_1 >= elbow_pos_2)
    {
        for (pos = elbow_pos_1; pos >= elbow_pos_2; pos -= 1)
        {
            myservo_elbow.write(pos);
            delay(30);
        }
    }
    else
    {
        for (pos = elbow_pos_1; pos <= elbow_pos_2; pos += 1)
        {
            myservo_elbow.write(pos);
            delay(30);
        }
    }
    delay(50);

    // Check Arm: + lean forward, - lean backward
    if (arm_pos_1 <= arm_pos_2)
    {
        for (pos = arm_pos_1; pos <= arm_pos_2; pos += 1)
        {
            myservo_arm.write(pos); // tell servo to go to position in variable 'pos'
            delay(15);
        }
    }
    else
    {
        for (pos = arm_pos_1; pos >= arm_pos_2; pos -= 1)
        {                           // goes from 100 degrees to 120 degrees
            myservo_arm.write(pos); // tell servo to go to position in variable 'pos'
            delay(15);
        }
    }
    delay(50);

    // Check Base: + counterclock, - lean clockwise
    //  Base same as initial position, goes from 5 degrees to 5 degrees
    if (base_pos_1 <= base_pos_2)
    {
        for (pos = base_pos_1; pos <= base_pos_2; pos += 1)
        { // goes from 90 degrees to 60 degrees
            myservo_base.write(pos);
            delay(15);
        }
    }
    else
    {
        for (pos = base_pos_1; pos >= base_pos_2; pos -= 1)
        { // goes from 90 degrees to 60 degrees
            myservo_base.write(pos);
            delay(15);
        }
    }
    delay(50);

    // Check Wrist: + counterclock, -clock
    if (wrist_pos_1 <= wrist_pos_2)
    {
        for (pos = wrist_pos_1; pos <= wrist_pos_2; pos += 1)
        {
            // in steps of 1 degree
            myservo_wrist.write(pos);
            delay(15);
        }
    }
    else
    {
        for (pos = wrist_pos_1; pos >= wrist_pos_2; pos -= 1)
        {
            // in steps of 1 degree
            myservo_wrist.write(pos);
            delay(15);
        }
    }
    delay(50);
}

void write_Pos_Back(int base_pos_1, int base_pos_2, int elbow_pos_1, int elbow_pos_2,
                    int arm_pos_1, int arm_pos_2, int wrist_pos_1, int wrist_pos_2,
                    int gripper_pos_1, int gripper_pos_2)
{

    // Check Wrist: + counterclock, -clock
    if (wrist_pos_1 <= wrist_pos_2)
    {
        for (pos = wrist_pos_1; pos <= wrist_pos_2; pos += 1)
        {
            // in steps of 1 degree
            myservo_wrist.write(pos);
            delay(15);
        }
    }
    else
    {
        for (pos = wrist_pos_1; pos >= wrist_pos_2; pos -= 1)
        {
            // in steps of 1 degree
            myservo_wrist.write(pos);
            delay(15);
        }
    }

    delay(50);

    // Check Base: + counterclock, - lean clockwise
    //  Base same as initial position, goes from 5 degrees to 5 degrees

    if (base_pos_1 <= base_pos_2)
    {
        for (pos = base_pos_1; pos <= base_pos_2; pos += 1)
        {
            myservo_base.write(pos);
            delay(15);
        }
    }
    else
    {
        for (pos = base_pos_1; pos >= base_pos_2; pos -= 1)
        { // goes from 90 degrees to 60 degrees
            myservo_base.write(pos);
            delay(15);
        }
    }
    delay(50);

    // Check Elbow: - lean forward, + lean backward
    if (elbow_pos_1 >= elbow_pos_2)
    {
        for (pos = elbow_pos_1; pos >= elbow_pos_2; pos -= 1)
        { // goes from 90 degrees to 60 degrees
            // Serial.print("Elbow: In the first branch!, angle: ");
            // Serial.println(pos);
            myservo_elbow.write(pos);
            delay(30);
        }
    }
    else
    {
        for (pos = elbow_pos_1; pos <= elbow_pos_2; pos += 1)
        { // goes from 90 degrees to 60 degrees
            // Serial.print("Elbow: In the 2nd branch!");
            myservo_elbow.write(pos);
            delay(30);
        }
    }

    delay(50);

    // Check Arm: + lean forward, - lean backward

    if (arm_pos_1 <= arm_pos_2)
    {
        for (pos = arm_pos_1; pos <= arm_pos_2; pos += 1)
        { 
            myservo_arm.write(pos); // tell servo to go to position in variable 'pos'
            delay(15);
        }
    }
    else
    {
        for (pos = arm_pos_1; pos >= arm_pos_2; pos -= 1)
        { 
            myservo_arm.write(pos); // tell servo to go to position in variable 'pos'
            delay(15);
        }
    }

    delay(50);
}

void SetInitialPos()
{  
    // Set Initial Position
    delay(15);
    myservo_base.write(5);    //Initial Pos of Base is 5 degree
    delay(30);
    myservo_elbow.write(40);  //Initial Pos of Elbow is 90 degree
    delay(30);
    myservo_arm.write(140);   //Initial Pos of Arm is 100 degree
    delay(30);
    myservo_wrist.write(80);  //Initial Pos of Wrist is 80 degree
    delay(30);
    myservo_gripper.write(50);
    delay(30);
  }