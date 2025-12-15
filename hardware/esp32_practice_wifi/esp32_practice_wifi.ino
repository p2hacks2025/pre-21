#define BLUE 32
#define RED 33

void setup()
{
  pinMode(BLUE, OUTPUT);
  pinMode(RED, OUTPUT);
}

void loop()
{
  digitalWrite(BLUE, HIGH);
  delay(500);
  digitalWrite(RED, HIGH);
  delay(500);
  digitalWrite(BLUE, LOW);
  delay(500);
  digitalWrite(RED, LOW);
  delay(500);
}
