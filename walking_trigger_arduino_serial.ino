int state_1=0;
int state_2 =0;
int Intensity =100;
int mode = -1;
int Freq;
int incomingByte;
int pin1=5;
int pin2=6;
int fanp1 =10;
int fanp2 =3;


void setup() {
  Serial.begin(9600);
  pinMode(pin1, OUTPUT);
 pinMode(pin2, OUTPUT);
 pinMode(fanp1, OUTPUT);
 pinMode(fanp2, OUTPUT);
  digitalWrite(pin1, LOW);
  digitalWrite(pin2, LOW);
  analogWrite(fanp1, 175);
  analogWrite(fanp2, 175);
   // 1600 is the max, use lower value to prevent "singing"
  Freq = 100;
  
  
  

}

void loop() {
  if (Serial.available()){
    incomingByte = Serial.read();
  }
  if(incomingByte =='y'){
    digitalWrite(5, HIGH);
    digitalWrite(pin2, HIGH);
  }
  if(incomingByte =='n'){
    digitalWrite(5, LOW);
    digitalWrite(pin2, LOW);
    }
   
  }    
  
