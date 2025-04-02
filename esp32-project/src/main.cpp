#include <Arduino.h>

// Define LED pins
#define LED_1 4   // Available GPIO Pins
#define LED_2 5   //
#define LED_3 16  //
#define LED_4 18  // 
#define LED_5 3   // 

// PWM configuration
#define PWM_CHANNEL_1 0
#define PWM_CHANNEL_2 1
#define PWM_CHANNEL_3 2
#define PWM_CHANNEL_4 3
#define PWM_CHANNEL_5 4

#define PWM_FREQ 5000
#define PWM_RESOLUTION 8  // 8-bit resolution (0-255)

void servo1() 
{
    Serial.println("Setting LED 4 (PWM 20%)");
    ledcWrite(PWM_CHANNEL_1, 15);  // 20%
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

    Serial.println("READY");
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
            return;
        }

        // 1-second delay to model robotic arm movement
        delay(1000);

        // Send "READY" to receive next classification
        Serial.println("READY");
    }
}
