/*
  This is a test sketch for the Adafruit assembled Motor Shield for Arduino v2
  It won't work with v1.x motor shields! Only for the v2's with built in PWM
  control
  For use with the Adafruit Motor Shield v2
  ---->  http://www.adafruit.com/products/1438
*/
#include <Wire.h>
#include <Adafruit_MotorShield.h>
#include <AccelStepper.h>
#include <MultiStepper.h>

typedef float coord_t;

const int TOOL_PIN = 10;
const int TOOL_DOWN_POS = 90;
const int TOOL_UP_POS = 25;
const int TOOL_WAIT_MS = 100;
int toolPos = TOOL_UP_POS;

const float SPOOL_RAD = 7.5; // in mm
const int TICKS_PER_ROT = 200;
const float TICKS_PER_MM = TICKS_PER_ROT / (2 * PI * SPOOL_RAD);

// All of these in mm
const coord_t LEFT_X = 0;
const coord_t LEFT_Y = 400;//953;
const coord_t RIGHT_X = 660;
const coord_t RIGHT_Y = LEFT_Y;

// Also in mm
const coord_t OFFSET_X = 41.5;
const coord_t OFFSET_Y = 40;

const coord_t HOME_X = (LEFT_X + RIGHT_X) / 2;
const coord_t HOME_Y = RIGHT_Y / 2;

const coord_t MAX_SEG_LEN = 5;

const long DEF_VEL = static_cast<long>(10 * TICKS_PER_MM); // in ticks per second

Adafruit_MotorShield shield;
Adafruit_StepperMotor *leftStepper = shield.getStepper(TICKS_PER_ROT, 1);
Adafruit_StepperMotor *rightStepper = shield.getStepper(TICKS_PER_ROT, 2);

AccelStepper left([]() {
  leftStepper->onestep(FORWARD, SINGLE);
}, []() {
  leftStepper->onestep(BACKWARD, SINGLE);
});
AccelStepper right([]() { // this is inverted to invert the motor
  rightStepper->onestep(BACKWARD, SINGLE);
}, []() {
  rightStepper->onestep(FORWARD, SINGLE);
});

MultiStepper ms;

static byte ndx = 0;
char endMarker = '\n';
char rc;
int commandLen = 100;
int numParts = 6;

typedef float coord_t;

int lengthBoard = 850;
int lengthBoard_kinda = 914; // 36 inch is 914 mm

float targetX = 0;
float targetY = 0;
float targetZ = 0;

void setup() {
  Serial.begin(9600);
  shield.begin();

  left.setAcceleration(DEF_VEL * 2);
  right.setAcceleration(DEF_VEL * 2);
  left.setMaxSpeed(DEF_VEL);
  right.setMaxSpeed(DEF_VEL);

  left.setCurrentPosition(0);
  right.setCurrentPosition(4250);

  ms.addStepper(left);
  ms.addStepper(right);

  Serial.println("// Hello world!");
}

void loop7(){
  while (Serial.available() != 0) {

    Serial.println("reading line");
    char command[commandLen] = {};
    size_t len = Serial.readBytesUntil('\n', command, commandLen - 1);
    command[len] = '\0';
  
    Serial.println(command);
  
  }
  
}

void loop3() {


  left.setCurrentPosition(200);
  right.setCurrentPosition(200);
  moveBothTo(0, 460
  );
  exit(0);

}

void loop() {

  while (Serial.available() == 0) {
    delay(10);
  }

  Serial.println("reading line");
  char command[commandLen] = {};
  size_t len = Serial.readBytesUntil('\n', command, commandLen - 1);
  command[len] = '\0';
  Serial.println(command);

  // Tokenize into space delimited parts
  char* parts[numParts] = {};
  char* part = strtok(command, " \n");
  for (size_t i = 0; i < numParts && part != nullptr; i++) {
    parts[i] = part;
    part = strtok(nullptr, " \n");
    //Serial.println(parts[i]);
  }

  char* type = parts[0];

  // Determine whether we need the tool
  if (strcmp(type, "G1") == 0) { // If it's a home command
    activateTool();
    Serial.println("tool is activated");
  }

  if (type == nullptr) {
    Serial.println("// Empty command! Failing silently...");
  }
  else if (strcmp(type, "G28") == 0) { // If it's a home command
    targetX = 0;
    targetY = 0;
    targetZ = 0;
  }
  else if (type[0] == 'G') {
    coord_t arcI = 0;
    coord_t arcJ = 0;
    for (int i = 1; i < numParts && parts[i] != nullptr; i++) {
      if (parts[i][0] == 'X') {
        targetX = static_cast<coord_t>(strtod(&parts[i][1], nullptr));
      } else if (parts[i][0] == 'Y') {
        targetY = static_cast<coord_t>(strtod(&parts[i][1], nullptr));
      } else if (parts[i][0] == 'Z') {
        targetZ = static_cast<coord_t>(strtod(&parts[i][1], nullptr));
      }
    }

    long leftMotorPosition = calculateLeftMotorPosition(targetX, targetY);

    long rightMotorPosition = calculateRightMotorPosition(targetX, targetY);

    Serial.print("Target X: ");
    Serial.println(targetX);

    Serial.print("Target Y: ");
    Serial.println(targetY);

    Serial.print("Destination Left Motor Position: ");
    Serial.println(leftMotorPosition);
    Serial.print("Destination Right Motor Position: ");
    Serial.println(rightMotorPosition);


    Serial.print("Before, Left: ");
    Serial.print(left.currentPosition());
    Serial.print(" | Right: ");
    Serial.println(right.currentPosition());
    //moveMotorsToPosition(leftMotorPosition, rightMotorPosition);
       //moveMotorsToPosition(leftMotorPosition, rightMotorPosition);
    moveBothTo(leftMotorPosition, rightMotorPosition);

    Serial.print("After, Left: ");
    Serial.print(left.currentPosition());
    Serial.print(" | Right: ");
    Serial.println(right.currentPosition());

  }

}

void calculateWhereItIs(float x, float y) {



}

void moveMotorsToPosition(int x, int y) {
  long positions[] = {x, y};
  ms.moveTo(positions);
  ms.runSpeedToPosition();
}

void activateTool() {

}

long calculateLeftMotorPosition(float x, float y) {

  Serial.println("Calculating left position");
  Serial.print("X: ");
  Serial.print(x);
  Serial.print(", Y: ");
  Serial.println(y);
  // a^2 + b^2 = c^2
  float xSquared = pow(x, 2);
  float ySquared = pow(y, 2);
  Serial.println(xSquared);
  Serial.println(ySquared);

  int len = sqrt(xSquared + ySquared);

  Serial.println(len);

  // Take the len and normalize it to the position of the motor ( 200 strokes / 40mm )
  double motorPosition = len * (200 / 40); // This is the position the motor should be at
  return motorPosition;
}

long calculateRightMotorPosition(float x, float y) {

  Serial.println("Calculating Right Motor Position: ");
  // a^2 + b^2 = c^2
  float xSquared = pow(lengthBoard - x , 2);
  float ySquared = pow(y, 2);
  Serial.println(xSquared);
  Serial.println(ySquared);

  int len = sqrt(xSquared + ySquared);

  Serial.println(len);

  // Take the len and normalize it to the position of the motor ( 200 strokes / 40mm )
  double motorPosition = len * (200 / 40); // This is the position the motor should be at
  return motorPosition;
}

void moveBothTo(long l, long r) {
  Serial.println(left.currentPosition());
  Serial.println(right.currentPosition());
  long positions[] = {l, r};
  ms.moveTo(positions);
  ms.runSpeedToPosition();
  Serial.println(left.currentPosition());
  Serial.println(right.currentPosition());
}
