/* ESP32でLCDに文字表示 
 *
 */
 
 #include <LiquidCrystal.h>

LiquidCrystal lcd(32,25,26,27,14,13);

void setup()
{
    lcd.begin(16, 2);
    lcd.clear();
    lcd.print("Hello World!");
    lcd.setCursor(0,1); 
    lcd.print ("LCD with ESP32");
}
void loop() {
}