#include <SoftwareSerial.h>

// Replace with your LED pin connections
const int red_led = 11;
const int green_led = 10;
const int blue_led = 9;

// Adjust these pins to ones suitable for your setup
SoftwareSerial arduinoSerial(0, 1); // RX, TX

void setup() {
  pinMode(red_led, OUTPUT);
  pinMode(green_led, OUTPUT);
  pinMode(blue_led, OUTPUT);
  arduinoSerial.begin(9600); // Make sure the baud rate matches what you're using on the other end
}

void turnOffLEDs() {
  digitalWrite(red_led, LOW);
  digitalWrite(green_led, LOW);
  digitalWrite(blue_led, LOW);
}

void loop() {
  if (arduinoSerial.available()) {
    char command = arduinoSerial.read();
    switch (command) {
      case 'S': // Sad (blue)
        digitalWrite(red_led, LOW);
        digitalWrite(green_led, HIGH);
        digitalWrite(blue_led, LOW);
        break;
      case 'A': // Angry (purple)
        digitalWrite(red_led, HIGH);
        digitalWrite(green_led, LOW);
        digitalWrite(blue_led, LOW);
        break;
      // case 'F': // Fear (example implementation)
      //   digitalWrite(red_led, LOW);
      //   digitalWrite(green_led, HIGH); // Example: green for Fear
      //   digitalWrite(blue_led, LOW);
      //   break;
      case 'H': // Happy (example implementation)
        digitalWrite(red_led, LOW); // Example: yellow (red + green) for Happy
        digitalWrite(green_led, LOW);
        digitalWrite(blue_led, HIGH);
        break;

      case 'O': // Turn off all LEDs
        turnOffLEDs();
        break;

      default:
        // Turn off all LEDs
        digitalWrite(red_led, LOW);
        digitalWrite(green_led, LOW);
        digitalWrite(blue_led, LOW);
        break;
    }
  }
}
