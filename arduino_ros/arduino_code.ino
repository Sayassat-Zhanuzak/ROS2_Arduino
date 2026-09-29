// This code has to be placed inside Arduino IDE

#include <Servo.h>

const int S1 = A0;
const int S2 = A1;
Servo my_servo;

void setup() {
  pinMode(S1, INPUT);
  pinMode(S2, INPUT);
  Serial.begin(9600);
  my_servo.attach(9);
  my_servo.write(90);
}

void loop() {
  int signal1 = analogRead(S1);
  int signal2 = analogRead(S2);

  Serial.print(signal1);
  Serial.print(",");
  Serial.println(signal2);

  if(Serial.available() > 0) {
    int angle = Serial.parseInt();
    my_servo.write(angle);
  }
  

  delay(50);
}