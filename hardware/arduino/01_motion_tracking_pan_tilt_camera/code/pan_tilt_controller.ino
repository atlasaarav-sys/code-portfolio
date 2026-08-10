/*
  Pan-Tilt Camera Controller
  ---------------------------
  Listens on Serial for lines like "P90 T45\n" (pan angle, tilt angle in degrees)
  and moves two servos accordingly. Designed to pair with a Python script on the
  PC that does motion detection on a webcam feed and sends target angles.

  Wiring:
    Pan servo  signal -> pin 9
    Tilt servo signal -> pin 10
    Servo power -> external 5V supply (NOT the Arduino 5V pin, to avoid brownouts)
    Servo ground -> shared ground with Arduino GND
*/

#include <Servo.h>

Servo panServo;
Servo tiltServo;

const int PAN_PIN = 9;
const int TILT_PIN = 10;

// Mechanical limits — adjust to match your bracket so it can't over-rotate
const int PAN_MIN = 0;
const int PAN_MAX = 180;
const int TILT_MIN = 30;   // tilt brackets often can't go full 0-180 without hitting the base
const int TILT_MAX = 150;

int currentPan = 90;   // start centered
int currentTilt = 90;

String inputBuffer = "";

void setup() {
  Serial.begin(115200);
  panServo.attach(PAN_PIN);
  tiltServo.attach(TILT_PIN);

  panServo.write(currentPan);
  tiltServo.write(currentTilt);
  delay(500);
}

void loop() {
  while (Serial.available() > 0) {
    char c = Serial.read();
    if (c == '\n') {
      parseAndMove(inputBuffer);
      inputBuffer = "";
    } else {
      inputBuffer += c;
    }
  }
}

void parseAndMove(String line) {
  line.trim();
  if (line.length() == 0) return;

  int pIndex = line.indexOf('P');
  int tIndex = line.indexOf('T');
  if (pIndex == -1 || tIndex == -1) return;

  int pan = line.substring(pIndex + 1, tIndex).toInt();
  int tilt = line.substring(tIndex + 1).toInt();

  pan = constrain(pan, PAN_MIN, PAN_MAX);
  tilt = constrain(tilt, TILT_MIN, TILT_MAX);

  currentPan = pan;
  currentTilt = tilt;

  panServo.write(currentPan);
  tiltServo.write(currentTilt);

  // Echo back so the PC side can log/confirm
  Serial.print("OK P");
  Serial.print(currentPan);
  Serial.print(" T");
  Serial.println(currentTilt);
}
