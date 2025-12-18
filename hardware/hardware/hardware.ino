#define SW1 33
#define SW2 33
#include <LiquidCrystal.h>
LiquidCrystal lcd(32,25,26,27,14,13);

char Q[4][50] = {
  "boy or girl",
  "new or old",
  "real or fantasy",
  "ONIGIRI or Hamburger"
};

int inputlog[3];

void setup() {
  Serial.begin(9600);
  pinMode(SW1, INPUT_PULLUP);
  pinMode(SW2, INPUT_PULLUP);

  lcd.begin(16, 2);
  /*
  lcd.clear();
  lcd.print("Hello World!");
  lcd.setCursor(0,1); 
  lcd.print ("LCD with ESP32");

  //文字列追加
  snprintf(buf,sizeof(buf),"%s","ア");
  Serial.println(buf);
  */

  

  for(int i=0;i<5;i++){
    int lastState1 = HIGH;
    int lastState2 = HIGH;

    while(true){
      int currentState1 = digitalRead(SW1);
      int currentState2 = digitalRead(SW2);

      lcd.clear();
      lcd.setCursor(0, 1);
      lcd.print(Q[i]);

      if(lastState1==HIGH && currentState1==LOW){
        inputlog[i] = 0;
        break;
      }else if(lastState2==HIGH && currentState2==LOW){
        inputlog[i] = 1;
        break;
      }

      lastState1 = currentState1;
      lastState2 = currentState2;
      delay(50);
    }
  }
}

void loop() {
  /*
  int state1 = digitalRead(SW1);
  Serial.println(state1);
  int state2 = digitalRead(SW2);
  Serial.println(state2);
  */
}

