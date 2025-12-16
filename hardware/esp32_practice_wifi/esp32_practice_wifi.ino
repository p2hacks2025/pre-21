// GPTからコピペ状態
#include <WiFi.h>
#include <HTTPClient.h>

/* ===== Wi-Fi設定 ===== */
const char *ssid = "YOUR_SSID";
const char *password = "YOUR_PASSWORD";

/* ===== 送信先サーバー ===== */
// 例: http://192.168.1.10/api
// 例: http://example.com/api
const char *serverUrl = "http://example.com/api";

void setup()
{
  Serial.begin(115200);
  delay(1000);

  /* ===== Wi-Fi接続 ===== */
  WiFi.begin(ssid, password);
  Serial.print("WiFi connecting");

  while (WiFi.status() != WL_CONNECTED)
  {
    delay(500);
    Serial.print(".");
  }

  Serial.println();
  Serial.println("WiFi connected!");
  Serial.print("IP address: ");
  Serial.println(WiFi.localIP());
}

void loop()
{
  if (WiFi.status() == WL_CONNECTED)
  {

    HTTPClient http;

    /* ===== サーバー接続 ===== */
    http.begin(serverUrl);
    http.addHeader("Content-Type", "application/json");

    /* ===== 送信データ（例） ===== */
    int sensorValue = analogRead(34); // GPIO34（例）
    String jsonData = "{";
    jsonData += "\"sensor\":" + String(sensorValue);
    jsonData += "}";

    /* ===== POST送信 ===== */
    int httpCode = http.POST(jsonData);

    if (httpCode > 0)
    {
      Serial.print("HTTP Response code: ");
      Serial.println(httpCode);
      Serial.print("Response body: ");
      Serial.println(http.getString());
    }
    else
    {
      Serial.print("Error on sending POST: ");
      Serial.println(httpCode);
    }

    http.end();
  }
  else
  {
    Serial.println("WiFi not connected");
  }

  delay(5000); // 5秒ごとに送信
}
