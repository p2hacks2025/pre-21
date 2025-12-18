#define SW1 22
#define SW2 23
#include <LiquidCrystal.h>
LiquidCrystal lcd(32, 25, 26, 27, 14, 13);

//質問の配列
char Q[4][50] = {
  "boy or girl",
  "new or old",
  "real or fantasy",
  "ONIGIRI or Hamburger"
};

//回答を保存するための文字列
char ans = "";

//ボタンの状態を保存する変数
int state1 = 1;
int state2 = 1;

void setup() {
  //シリアルモニターを使用するため
  Serial.begin(9600);
  //ボタンの設定
  pinMode(SW1, INPUT_PULLUP);
  pinMode(SW2, INPUT_PULLUP);

  //LCDを使用するため
  lcd.begin(16, 2);

  //質問の数繰り返し
  for (int i = 0; i < 4; i++) {
    //2行目に質問の選択肢を表示
    lcd.clear();
    lcd.setCursor(0, 1);
    lcd.print(Q[i]);

    //ボタンの状態を変数に保存
    state1 = digitalRead(SW1);
    state2 = digitalRead(SW2);

    //ボタンがどちらか押されるまで先に進まない
    while (!state1 && !state2) {
      //ボタンの状態更新
      state1 = digitalRead(SW1);
      state2 = digitalRead(SW2);
    }

    //ボタン1が押されたら0,ボタン2が押されたら1で回答を保存
    if (!state1) {
      ans += "0";
    } else {
      ans += "1";
    }
    //確認用にシリアルモニターに出力
    Serial.println(ans);
  }
}

void loop() {
  //loopは使わない
}
