# define SW1 33
# define SW2 33
#include <LiquidCrystal.h>
LiquidCrystal lcd(32,25,26,27,14,13);

char buf[50];

void setup() {
  Serial.begin(9600);
  pinMode(SW1,INPUT_PULLUP);
  pinMode(SW2,INPUT_PULLUP);

  lcd.begin(16, 2);
  lcd.clear();
  lcd.print("Hello World!");
  lcd.setCursor(0,1); 
  lcd.print ("LCD with ESP32");

  snprintf(buf,sizeof(buf),"%s","ア");
  Serial.println(buf);
}

void loop() {
  int state1 = digitalRead(SW1);
  Serial.println(state1);
  int state2 = digitalRead(SW2);
  Serial.println(state2);
}

