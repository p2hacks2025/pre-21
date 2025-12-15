/* ESP32でLCDに文字表示（半角カタカナ対応） */

#include <LiquidCrystal.h>

LiquidCrystal lcd(32, 25, 26, 27, 14, 13);

void setup()
{
    lcd.begin(16, 2);
    lcd.clear();

    lcd.print("3.14");

    lcd.setCursor(0, 1);

    // 「ｶﾀｶﾅ」を半角カタカナで表示
    lcd.write(0xB6); // ｶ
    lcd.write(0xC0); // ﾀ
    lcd.write(0xB6); // ｶ
    lcd.write(0xC5); // ﾅ
}

void loop() {
}
