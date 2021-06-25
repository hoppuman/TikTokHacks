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
#include <Servo.h>

const int testServo = 0;

typedef float coord_t;

const float SPOOL_RAD = 42; // in mm
const int TICKS_PER_ROT = 200;
const float TICKS_PER_MM = TICKS_PER_ROT / (2 * PI * SPOOL_RAD);
const long DEF_VEL = static_cast<long>(100 * TICKS_PER_MM); // in ticks per second

const int DEBUG_MODE = 1;

const int SERVO_POSITION_ON = 0;
const int SERVO_POSITION_OFF = 60;

int servo_activated = 1;
int MultiLetterOffset = 0;
// The purpose of this is to go down a row when to write another word 
int rowCount = 0;

int xOffSet = 130;
int yOffSet = 190;
int boardHeight = 630;

float fontSize = 1;

int currentX = 0;
int currentY = 0;


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

Servo myservo;

static byte ndx = 0;
char endMarker = '\n';
char rc;
int commandLen = 200;
int numParts = 6;

typedef float coord_t;

int lengthBoard = 820;

float targetX = 0;
float targetY = 0;
float targetZ = 0;

float IValue = 0;
float JValue = 0;

int skipCurrentCommand = 0;

  int LettersUpsideDown = 1;

void setup() {
  Serial.begin(9600);
  shield.begin();

  Serial.print("VEL: ");
  Serial.println(DEF_VEL);

  left.setAcceleration(DEF_VEL * 2);
  right.setAcceleration(DEF_VEL * 2);
  left.setMaxSpeed(DEF_VEL);
  right.setMaxSpeed(DEF_VEL);

  // so 0,0 is our base but the lengths of the ropes need to be at 130, 190
  left.setCurrentPosition(calculateLeftMotorPosition(xOffSet,yOffSet));
  right.setCurrentPosition(calculateRightMotorPosition(xOffSet,yOffSet));

  ms.addStepper(left);
  ms.addStepper(right);

  myservo.attach(10);
  myservo.write(SERVO_POSITION_OFF);

  Serial.println("// Hello world!");
}

void PrintDebugInfo(String message, int printMode){
    if(DEBUG_MODE == 1){
      Serial.println(message);
    }
}

void TestServo(){
  activateTool();
  delay(1000);
  deactivateTool();
  delay(1000);
}

void moveMotorsToPosition(int x, int y) {
  long positions[] = {x, y};
  ms.moveTo(positions);
  ms.runSpeedToPosition();
}

void activateTool() {
  if(servo_activated == 0){
    PrintDebugInfo("Activating Tool", 1);
    myservo.write(SERVO_POSITION_ON);
    servo_activated = 1;
  }
}

void deactivateTool() {
  if(servo_activated == 1){
    PrintDebugInfo("Deactivating Tool", 1);
    myservo.write(SERVO_POSITION_OFF);
    servo_activated = 0;
  }
}

long calculateLeftMotorPosition(float x, float y) {

  // a^2 + b^2 = c^2
  float xSquared = pow(x, 2);
  float ySquared = pow(y, 2);

  int len = sqrt(xSquared + ySquared);

  // Take the len and normalize it to the position of the motor ( 200 strokes / 40mm )
  double motorPosition = len * (TICKS_PER_ROT / SPOOL_RAD); // This is the position the motor should be at
  return motorPosition;
}

long calculateRightMotorPosition(float x, float y) {
  
  float xSquared = pow(lengthBoard - x , 2);
  float ySquared = pow(y, 2);
  int len = sqrt(xSquared + ySquared);
  // Take the len and normalize it to the position of the motor ( 200 strokes / 40mm )
  double motorPosition = len * (TICKS_PER_ROT / SPOOL_RAD); // This is the position the motor should be at
  return motorPosition;
}

void moveBothTo(long l, long r) {
  long positions[] = {l, r};
  ms.moveTo(positions);
  ms.runSpeedToPosition();
}

void interpolate(float t, coord_t currX, coord_t currY, coord_t targetX, coord_t targetY, float curvature, bool clockwise, coord_t& interpX, coord_t& interpY) {
    if (curvature == 0) {
        // If this is a line, interpolation is easy peasy
        float interpX = currX + t * (targetX - currX);
        float interpY = currY + t * (targetY - currY);
    } else {
        // Get vector from current to target
        float dx = targetX - currX;
        float dy = targetY - currY;
        float dist = hypot(dx, dy);

        // normalize that vector
        float dxNorm = dx / dist;
        float dyNorm = dy / dist;


        // This is the distance between the circle center and the chord
        float d = sqrt(sq(1 / curvature) - sq(dist / 2));


        // Calculate the circle center (find midpoint between curr and target and add normalized vector rotated CW or CCW 90 deg and scaled by d)
        float cX, cY;
        if (clockwise) {
            cX = currX + dx / 2 + dyNorm * d;
            cY = currY + dy / 2 - dxNorm * d;
        } else {
            cX = currX + dx / 2 - dyNorm * d;
            cY = currY + dy / 2 + dxNorm * d;
        }

        // Get vector from circle center to current position
        float fromCX = currX - cX;
        float fromCY = currY - cY;
        // This is the angle subtended by the chord from current to target
        float angle = 2 * asin(dist * curvature / 2) * t;
        if (!clockwise) angle = -angle; // Negative angle means CCW
        // Apply a CW rotation by angle (if angle < 0 then rotation is CCW)
        float x = cos(angle) * fromCX + sin(angle) * fromCY;
        float y = -sin(angle) * fromCX + cos(angle) * fromCY;
        // Add back to circle center to get interpolated point
        interpX = cX + x;
        interpY = cY + y;
    }
}

void loop() {

  if (testServo == 1){ 
    while(1){
      TestServo();
    }
  }
  
  Serial.println("Looking for Commmand");
  // Wait for a response from python script
  while (Serial.available() == 0) {
    delay(10);
  }

  Serial.println("Made It Here 2");

  // Read the message and put it into a buffer
  char command[commandLen] = {};
  size_t len = Serial.readBytesUntil('\n', command, commandLen - 1);
  command[len] = '\0';

  Serial.print("command received: ");
  Serial.println(command);

  
  if (skipCurrentCommand == 1){
    skipCurrentCommand = 0;
  }
  else{
    // Tokenize into space delimited parts
  char* parts[numParts] = {};
  char* part = strtok(command, " \n");
  for (size_t i = 0; i < numParts && part != nullptr; i++) {
    parts[i] = part;
    part = strtok(nullptr, " \n");
  }

  char* type = parts[0]; // Retrieve the first "section" of the buffer i.e. whether we want the tool up or down

  if(type[0] == 'l' and type[1] == 'n'){
    rowCount = int(type[3] - 48);
    Serial.println(int(type[3]) - 48);
    Serial.println("ok");
    MultiLetterOffset = 0;
    return;
  }

  if((strcmp(parts[0], "off") == 0)){
    xOffSet = static_cast<coord_t>(strtod(&parts[1][0], nullptr));
    yOffSet = static_cast<coord_t>(strtod(&parts[2][0], nullptr));
    Serial.println("ok");
  }

  // Signals to the python program that we finished
  if (strcmp(type, "fin") == 0) {
    
    MultiLetterOffset = MultiLetterOffset + 1;
    Serial.println("q");
    Serial.println('j');
  }
  else if (strcmp(type, "G01") == 0) {
    activateTool();
    delay(2000);
  }
  else if (strcmp(type, "G03") == 0) {
    activateTool();
    delay(2000);
  }
  else if (strcmp(type, "G00") == 0) {
    deactivateTool();
    delay(1000);
  }


  // type: refers to what type of command we're dealing with
  // part: the parts of the commands G0 X0 Y0 has parts[0] / parts[1] / parts[2] 
  
  if (type == nullptr) {
    PrintDebugInfo("// Empty command! Failing silently..." , 1);
    Serial.println('j');
  }
  else if (strcmp(type, "G28") == 0) { // If it's a home command
    targetX = 0;
    targetY = 0;
    targetZ = 0;
  }
  else if ((strcmp(type, "G01") == 0) || (strcmp(type, "G00") == 0) || (strcmp(type, "G0") == 0)){

    for (int i = 1; i < numParts && parts[i] != nullptr; i++) {
      if (parts[i][0] == 'X') {
        targetX = static_cast<coord_t>(strtod(&parts[i][1], nullptr));
      } else if (parts[i][0] == 'Y') {
        targetY = static_cast<coord_t>(strtod(&parts[i][1], nullptr));
      } else if (parts[i][0] == 'Z') {
        targetZ = static_cast<coord_t>(strtod(&parts[i][1], nullptr));
      }
    }

    // Scale down the x and y by the font size
    targetX = targetX * fontSize;
    targetY = targetY * fontSize;

    targetX = targetX + 280;
    //targetY = targetY - 200;

    // Instantiate some variables
    long leftMotorPosition = 0;
    long rightMotorPosition = 0;
    int LetterMode = 0;

    // MultiLetterOffset - Starts at 0 and increases by 1 for each letter
    // FontSize          - Controls how much to offset based on how big the characters are
    // LetterMode        - Whether to take multi letter offset into affect, 1 when not debugging 

    if (LetterMode == 1){
        if(LettersUpsideDown == 1){
          leftMotorPosition = calculateLeftMotorPosition(targetX + xOffSet + (MultiLetterOffset * 100 * (fontSize * 1.1)), boardHeight - targetY - yOffSet + (100 * (fontSize * 1.1) * rowCount));
          rightMotorPosition = calculateRightMotorPosition(targetX + xOffSet + (MultiLetterOffset * 100 * (fontSize * 1.1)), boardHeight - targetY - yOffSet + (100 * (fontSize * 1.1) * rowCount));
        }
        else{
          leftMotorPosition = calculateLeftMotorPosition(targetX + xOffSet + (MultiLetterOffset * 35), targetY - yOffSet + (100 * fontSize * rowCount));
          rightMotorPosition = calculateRightMotorPosition(targetX + xOffSet + (MultiLetterOffset * 35), targetY - yOffSet + (100 * fontSize * rowCount));  
        }
    }
    else{
          int destinationX = targetX + xOffSet;
          int destinationY = targetY + yOffSet;
          leftMotorPosition = calculateLeftMotorPosition  ( destinationX , destinationY);
          rightMotorPosition = calculateRightMotorPosition( destinationX , destinationY);  
          currentX = destinationX;
          currentY = destinationY;
    }

    // Printing some Debug info
    Serial.print("Target X: ");
    Serial.print(MultiLetterOffset);
    Serial.print(" : ");
    Serial.println(targetX);

    Serial.print("Target Y: ");
    Serial.println(targetY);

    Serial.print("Before, Left: ");
    Serial.print(left.currentPosition());
    Serial.print(" | Right: ");
    Serial.println(right.currentPosition());

    // Move the two motors to the positions specfied
    moveBothTo(leftMotorPosition, rightMotorPosition);

    Serial.print("After, Left: ");
    Serial.print(left.currentPosition());
    Serial.print(" | Right: ");
    Serial.println(right.currentPosition());
    
    Serial.println('j');

  } // for the G00 else-if
  else if ((strcmp(type, "G02") == 0) || (strcmp(type, "G03") == 0)){
    // Parse the request
    targetX = 0;
    targetY = 0;
    IValue = 0;
    JValue = 0;

    for (int i = 1; i < numParts && parts[i] != nullptr; i++) {
      if (parts[i][0] == 'X') {
        targetX = static_cast<coord_t>(strtod(&parts[i][1], nullptr));
      } else if (parts[i][0] == 'Y') {
        targetY = static_cast<coord_t>(strtod(&parts[i][1], nullptr));
      } else if (parts[i][0] == 'I') {
        IValue = static_cast<coord_t>(strtod(&parts[i][1], nullptr));
      } else if (parts[i][0] == 'J') {
        JValue = static_cast<coord_t>(strtod(&parts[i][1], nullptr));
      }
    }

    targetX = targetX + 280;
    //t argetY = targetY - 200;

    bool clockwise;

    if (strcmp(type, "G02") == 0){
      clockwise = 1;
    }
    else{
      clockwise = 0;
    }

    float rad = hypot(IValue, JValue);
    Serial.print("radius: ");
    Serial.println(rad);
    float curvature = 1 / rad;

    float numSegs = 30;
    for (int i = 0; i < numSegs; i++) {
        float t = static_cast<float>(i + 1) / numSegs;
        coord_t interpX, interpY;
        interpolate(t, currentX, currentY, targetX + xOffSet, targetY + yOffSet, curvature, clockwise, interpX, interpY); // calculate target x and y positions
        Serial.print("(x,y): ");
        Serial.print(interpX);
        Serial.print(" , ");
        Serial.println(interpY);

        if (isnan(interpX) or isnan(interpY)) {
          Serial.println('Coordinate Not understood, next command');
          Serial.println('j');
          return;
        }

        long leftMotorPosition = calculateLeftMotorPosition  ( interpX , interpY);
        long rightMotorPosition = calculateRightMotorPosition( interpX , interpY);  

        moveBothTo(leftMotorPosition, rightMotorPosition);
        currentX = interpX;
        currentY = interpY;
    }
    Serial.println('j');
  }
  else{
    Serial.println("command not recognized, skipping");
    Serial.println('j');
  }
    
  }

}
