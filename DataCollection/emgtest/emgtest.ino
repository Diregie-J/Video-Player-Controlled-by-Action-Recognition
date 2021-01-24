const unsigned long READ_PERIOD = 10000;  // 10000(ms) = 1/(100Hz)
int sensorV[3]={0};

int flag=0;

void setup() {
  // put your setup code here, to run once:
  Serial.begin(19200);
}

void loop() {
  // put your main code here, to run repeatedly:
  //int sensorValue;
  //long currentMicros=0;
  static unsigned long lastRead;

  
  
  if (micros() - lastRead >= READ_PERIOD) {

    if(flag==0){
        while(Serial.available()==0){
          delay(100);
        }
        flag=1;
      }
    
    if(flag==1){
      delay(1000);
      flag=2;
    } 

    if(flag==2){
      lastRead += READ_PERIOD;
      sensorV[0] = analogRead(A0);
      sensorV[1] = analogRead(A1);
      sensorV[2] = analogRead(A2);
      Serial.println(sensorV[0]);
      Serial.println(sensorV[1]);
      Serial.println(sensorV[2]);
      Serial.println(micros());
    }
  }
  
}
