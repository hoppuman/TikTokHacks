// Example 2 - Receive with an end-marker

const byte numChars = 32;
char receivedChars[numChars];   // an array to store the received data
boolean newData = false;



void setup() {
    Serial.begin(9600);
    Serial.println("<Arduino is ready>");
    pinMode(10,OUTPUT);
}

void loop() {
    recvWithEndMarker();
}

void recvWithEndMarker() {
    static byte ndx = 0;
    char endMarker = '\n';
    char rc;
    int commandLen = 100;
    int numParts = 6;
   
    while (Serial.available() > 0 && newData == false) {

        char command[commandLen] = {};
        size_t len = Serial.readBytesUntil('\n', command, commandLen - 1);
        command[len] = '\0';


        // Tokenize into space delimited parts
        char* parts[numParts] = {};
        char* part = strtok(command, " \n");
        for (size_t i = 0; i < numParts && part != nullptr; i++) {
            parts[i] = part;
            part = strtok(nullptr, " \n");
            Serial.println(parts[i]);
            Serial.println(strcmp(parts[i], "test"));
            if(strcmp(parts[i], "test") == 0){
              Serial.println("found");
              digitalWrite(10,HIGH);
            }
        }
        
    }


}
