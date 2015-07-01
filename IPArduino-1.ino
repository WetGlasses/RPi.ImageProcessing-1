char A;
void setup() {
  // put your setup code here, to run once:

  Serial.begin(9600);
  pinMode (2, OUTPUT);
  digitalWrite(2, LOW);
  pinMode (3, OUTPUT);
  digitalWrite(3, LOW);
  pinMode (4, OUTPUT);
  digitalWrite(4, LOW);
}

void loop() {
  // put your main code here, to run repeatedly: 
  if(Serial.available())
  {
  A = Serial.read();
  if(A=='A')
  {
  digitalWrite(2,HIGH);
    digitalWrite(3,LOW);
      digitalWrite(4,LOW);
  }
  else if(A=='B')
  {
  digitalWrite(3,HIGH);
    digitalWrite(2,LOW);
      digitalWrite(4,LOW);
  }
  else if(A=='C')
  {
  digitalWrite(4,HIGH);
    digitalWrite(3,LOW);
      digitalWrite(2,LOW);
  }
  }
}
