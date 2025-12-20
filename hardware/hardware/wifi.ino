#include <WiFi.h>
#include <HTTPClient.h>

//discordに送ったやつコピペ（wifi関連）


void wifi(){
  /* --- Wi-Fi 接続 --- */
  lcd.begin(16, 2);
  lcd.clear();
  lcd.print("Connecting...");

  Serial.print("Connecting to WiFi");
  WiFi.begin(ssid, password);

  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }

  Serial.println("\nWiFi connected");
  Serial.print("IP address: ");
  Serial.println(WiFi.localIP());
}

void senddata(){
   /* --- サーバー へ送信 --- */
  if (WiFi.status() == WL_CONNECTED) {
    HTTPClient http;

    http.begin(serverUrl);
    http.addHeader("Content-Type", "text/plain");

    int responseCode = http.POST(ans);

    Serial.print("HTTP Response code: ");
    Serial.println(responseCode);

    http.end();
  } else {
    Serial.println("WiFi not connected");
  }
}