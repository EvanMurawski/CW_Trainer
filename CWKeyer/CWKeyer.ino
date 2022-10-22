
int led_pin = 6;
int dah_pin = 13;
int dit_pin = 11;

int DAH = 3;
int DIT = 1;

int dit_time = 80;

int lastTone = DIT;
  
void setup()
{
  pinMode(led_pin, OUTPUT);
  pinMode(dah_pin, INPUT_PULLUP);
  pinMode(dit_pin, INPUT_PULLUP);
  Serial.begin(115200);
}

void loop() {
  
  int dahStatus = digitalRead(dah_pin);
  int ditStatus = digitalRead(dit_pin);

  if (dahStatus == 0 && ditStatus == 0) {
    makeIambic();
  }
    else if(dahStatus == 0) {
    makeTone(DAH);
  } else if (ditStatus ==0) {
    makeTone(DIT);
  }
}

void makeTone(int toneLength){

  Serial.write(toneLength == 3 ? "a" : "i");
  analogWrite(led_pin, 127);
  delay(dit_time * toneLength);
  analogWrite(led_pin, 0);
  delay(dit_time);
  lastTone = toneLength;
}

void makeIambic() {
  if (lastTone == DIT) {
    makeTone(DAH);
  } else {
    makeTone(DIT);
  }
}
