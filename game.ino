const int buttonPin1 = 4;  // Button to move left
const int buttonPin2 = 3;  // Button to move right
const int buttonPin3 = 2;  // Button to rotate

int buttonState1 = 0;
int buttonState2 = 0;
int buttonState3 = 0;

int lastButtonState1 = 0;
int lastButtonState2 = 0;
int lastButtonState3 = 0;

unsigned long lastDebounceTime1 = 0;
unsigned long lastDebounceTime2 = 0;
unsigned long lastDebounceTime3 = 0;

const unsigned long debounceDelay = 50;  // Debounce delay in milliseconds

void setup() {
  Serial.begin(9600);
  pinMode(buttonPin1, INPUT);
  pinMode(buttonPin2, INPUT);
  pinMode(buttonPin3, INPUT);
}

void loop() {
  int reading1 = digitalRead(buttonPin1);
  int reading2 = digitalRead(buttonPin2);
  int reading3 = digitalRead(buttonPin3);

  if (reading1 != lastButtonState1) {
    lastDebounceTime1 = millis();
  }
  if (reading2 != lastButtonState2) {
    lastDebounceTime2 = millis();
  }
  if (reading3 != lastButtonState3) {
    lastDebounceTime3 = millis();
  }

  if ((millis() - lastDebounceTime1) > debounceDelay) {
    if (reading1 != buttonState1) {
      buttonState1 = reading1;
      if (buttonState1 == HIGH) {
        Serial.println("LEFT");
      }
    }
  }

  if ((millis() - lastDebounceTime2) > debounceDelay) {
    if (reading2 != buttonState2) {
      buttonState2 = reading2;
      if (buttonState2 == HIGH) {
        Serial.println("RIGHT");
      }
    }
  }

  if ((millis() - lastDebounceTime3) > debounceDelay) {
    if (reading3 != buttonState3) {
      buttonState3 = reading3;
      if (buttonState3 == HIGH) {
        Serial.println("ROTATE");
      }
    }
  }

  lastButtonState1 = reading1;
  lastButtonState2 = reading2;
  lastButtonState3 = reading3;
}
