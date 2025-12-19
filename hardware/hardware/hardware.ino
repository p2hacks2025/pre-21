#define SW1 22
#define SW2 23
#include <LiquidCrystal.h>
#include <WiFi.h>
#include <HTTPClient.h>
LiquidCrystal lcd(32, 25, 26, 27, 14, 13);
byte title[] = { 0xB1, 0xC5, 0xC0, 0xB6, 0xDE, 0xB4, 0xD7, 0xCC, 0xDE, 0xC9, 0xCA };  //ｱﾅﾀｶﾞｴﾗﾌﾞﾉﾊ

//質問の配列
char Q[4][50] = {
  "Boy/Girl",
  "New/Old",
  "Real/Fantasy",
  "Rice/Bread"
};

//回答を保存するための文字列
char ans = "";

//ボタンの状態を保存する変数
int state1 = 1;
int state2 = 1;

//wifi.inoにてWi-Fi情報をssid,passwordに記録

void setup() {
  //シリアルモニターを使用するため
  Serial.begin(115200);

  wifi_connect();

  //ボタンの設定
  pinMode(SW1, INPUT_PULLUP);
  pinMode(SW2, INPUT_PULLUP);

  //LCDを使用するため
  lcd.begin(16, 2);

  //質問の数繰り返し
  for (int i = 0; i < 4; i++) {
    lcd.clear();
    lcd.write(title, 11);  //1行目を表示
    //2行目に質問の選択肢を表示
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

  wifi_send();
}

void loop() {
  //loopは使わない
}

void wifi_connect() {
  //接続
  WiFi.begin(ssid, password);
  Serial.print("WiFi connecting");

  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }

  Serial.println();
  Serial.println("WiFi connected!");
  Serial.print("IP address: ");
  Serial.println(WiFi.localIP());
}

void wifi_send() {
  if (WiFi.status() == WL_CONNECTED) {

    HTTPClient http;

    //サーバー接続
    http.begin(serverUrl);
    http.addHeader("Content-Type", "application/json");

    //送信データ（例）
    int sensorValue = analogRead(34);  // GPIO34（例）
    String jsonData = "{";
    jsonData += "\"ans\":" + ans;
    jsonData += "}";

    //POST送信
    int httpCode = http.POST(jsonData);

    if (httpCode > 0) {
      Serial.print("HTTP Response code: ");
      Serial.println(httpCode);
      Serial.print("Response body: ");
      Serial.println(http.getString());
    } else {
      Serial.print("Error on sending POST: ");
      Serial.println(httpCode);
    }

    http.end();
  } else {
    Serial.println("WiFi not connected");
  }

  delay(5000);  // 5秒ごとに送信
}
