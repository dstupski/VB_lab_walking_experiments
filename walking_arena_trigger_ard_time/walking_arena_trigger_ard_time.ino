 int mode = -1;
int Freq;
char incomingByte;
int pin1=3;
int pin2=5;
int pin3= 6;
int fanp1 =9;
int fanp2 =10;
int fanp3 =11;
unsigned long flash_dur1 = 10;
unsigned long flash_dur2 = 500;
unsigned long flash_dur3 = 1000;
int ar1_state = 0;
int ar2_state = 0;
int ar3_state =0;
unsigned long ar1_call = millis();
unsigned long ar2_call = millis();
unsigned long ar3_call = millis();
//int refrac =5000;
void setup() {
  Serial.begin(9600);
  pinMode(pin1, OUTPUT);
  pinMode(pin2, OUTPUT);
  pinMode(pin3, OUTPUT);
  pinMode(fanp1, OUTPUT);
  pinMode(fanp2, OUTPUT);
  pinMode(fanp3, OUTPUT);
  analogWrite(pin1, 0);
  analogWrite(pin2, 0);
  analogWrite(pin3, 0);
  analogWrite(fanp1, 255/3);
  analogWrite(fanp2, 255/3);
  analogWrite(fanp3, 255/3);
  
  // put your setup code here, to run once:

}

void loop() {
  if (Serial.available()){
    incomingByte = Serial.read();
  }

if(incomingByte=='a'){  
  incomingByte =' ';
 }
if(incomingByte=='b'){
  analogWrite(pin1, 255);
  ar1_state =1;
  ar1_call = millis();
  flash_dur1 = 40;
  incomingByte =' ';
 }

if(incomingByte=='c'){
  analogWrite(pin1, 255);
  ar1_state =1;
  ar1_call = millis();
  flash_dur1 = 200;
  incomingByte =' ';
 }
 if(incomingByte=='d'){
  analogWrite(pin1,255);
  ar1_state =1;
  ar1_call = millis();
  flash_dur1 = 1000;
  incomingByte =' ';
 }
if(incomingByte=='e'){
  analogWrite(pin1, 255);
  ar1_state =1;
  ar1_call = millis();
  flash_dur1 = 5000;
  incomingByte =' ';
 }
 if(ar1_state ==1 and millis() > ar1_call + flash_dur1){
  analogWrite(pin1, 0);
  ar1_state =0;
  
 }
if(incomingByte=='f'){  
  incomingByte =' ';
 }
 if(incomingByte=='g'){
  analogWrite(pin2, 255);
  ar2_state =1;
  flash_dur2 = 40;
  ar2_call =millis();
  incomingByte =' ';
 }
 if(incomingByte=='h'){
  analogWrite(pin2, 255);
  ar2_state =1;
  flash_dur2 = 200;
  ar2_call =millis();
  incomingByte =' ';
 }
 if(incomingByte=='i'){
  analogWrite(pin2, 255);
  ar2_state =1;
  flash_dur2 = 1000;
  ar2_call =millis();
  incomingByte =' ';
 }
 if(incomingByte=='j'){
  analogWrite(pin2, 255);
  ar2_state =1;
  flash_dur2 = 5000;
  ar2_call =millis();
  incomingByte =' ';
 }

if(ar2_state ==1 and millis() > ar2_call + flash_dur2){
  analogWrite(pin2, 0);
  ar2_state =0;
  }

 if(incomingByte=='k'){
  incomingByte =' ';
 }
if(incomingByte=='l'){
  analogWrite(pin3, 255);
  ar3_state =1;
  flash_dur3 = 40;
  ar3_call =millis();
  incomingByte =' ';
 }
 if(incomingByte=='m'){
  analogWrite(pin3, 255);
  ar3_state =1;
  flash_dur3 = 200;
  ar3_call =millis();
  incomingByte =' ';
 }
if(incomingByte=='n'){
  analogWrite(pin3, 255);
  ar3_state =1;
  flash_dur3 = 1000;
  ar3_call =millis();
  incomingByte =' ';
 }
if(incomingByte=='0'){
  analogWrite(pin3, 255);
  ar3_state =1;
  flash_dur3 = 5000;
  ar3_call =millis();
  incomingByte =' ';
 }
    
if(ar3_state ==1 and millis() > ar3_call + flash_dur3){
  analogWrite(pin3, 0);
  ar3_state =0;
  }
     
  
 
 
 
}
