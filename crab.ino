#define B0  31
#define C1  33
#define CS1 35
#define D1  37
#define DS1 39
#define E1  41
#define F1  44
#define FS1 46
#define G1  49
#define GS1 52
#define A1  55
#define AS1 58
#define B1  62
#define C2  65
#define CS2 69
#define D2  73
#define DS2 78
#define E2  82
#define F2  87
#define FS2 93
#define G2  98
#define GS2 104
#define A2  110
#define AS2 117
#define B2  123
#define C3  131
#define CS3 139
#define D3  147
#define DS3 156
#define E3  165
#define F3  175
#define FS3 185
#define G3  196
#define GS3 208
#define A3  220
#define AS3 233
#define B3  247
#define C4  262
#define CS4 277
#define D4  294
#define DS4 311
#define E4  330
#define F4  349
#define FS4 370
#define G4  392
#define GS4 415
#define A4  440
#define AS4 466
#define B4  494
#define C5  523
#define CS5 554
#define D5  587
#define DS5 622
#define E5  659
#define F5  698
#define FS5 740
#define G5  784
#define GS5 831
#define A5  880
#define AS5 932
#define B5  988
#define C6  1047
#define CS6 1109
#define D6  1175
#define DS6 1245
#define E6  1319
#define F6  1397
#define FS6 1480
#define G6  1568
#define GS6 1661
#define A6  1760
#define AS6 1865
#define B6  1976
#define C7  2093
#define CS7 2217
#define D7  2349
#define DS7 2489
#define E7  2637
#define F7  2794
#define FS7 2960
#define G7  3136
#define GS7 3322
#define A7  3520
#define AS7 3729
#define B7  3951
#define C8  4186
#define CS8 4435
#define D8  4699
#define DS8 4978
int tonePin = 11;
int tones[] = {AS4,A4,A4,AS4,AS4,A4,A4,AS4,AS4,A4,A4,AS4,AS4,A4,A4,AS4,D4,AS3,A3,A3,A3,A3,A3,AS3,AS3,AS3,C4,A3,AS3,AS3,A3,A3,A3,A3,A3,AS3,AS3,AS3,A3,AS3,AS3,A3,A3,A3,A3,A3,AS3,AS3,AS3,A3,G3,G3,G3,G3,AS3,A3,CS4,D4,D4,AS4,G4,G4,D4,D4,A4,F4,F4,D4,D4,A4,F4,F4,C4,C4,E4,E4,F4,D4,AS4,G4,G4,D4,D4,A4,F4,F4,D4,D4,A4,F4,F4,C4,C4,E4,E4,F4,D3,AS3,G3,G3,D3,D3,A3,F3,F3,D3,D3,A3,F3,F3,C3,C3,E3,E3,F3,D4,AS4,G4,G4,D4,D4,A4,F4,F4,D4,D4,A4,F4,F4,C4,C4,E4,E4,F4,AS4,A4,A4,AS4,AS4,A4,A4,AS4,AS4,A4,A4,AS4,AS4,A4,A4,AS4,D4,AS3,A3,A3,A3,A3,A3,AS3,AS3,AS3,A3,AS3,AS3,A3,A3,A3,A3,A3,AS3,AS3,AS3,A3,AS3,AS3,A3,A3,A3,A3,A3,AS3,AS3,AS3,A3,G3,G3,G3,G3,AS3,A3,CS4,D4,D4,AS4,G4,G4,D4,D4,A4,F4,F4,D4,D4,A4,F4,F4,C4,C4,E4,E4,F4,D4,AS4,G4,G4,D4,D4,A4,F4,F4,D4,D4,A4,F4,F4,C4,C4,E4,E4,F4,D3,AS3,G3,G3,D3,D3,A3,F3,F3,D3,D3,A3,F3,F3,C3,C3,E3,E3,F3,D4,AS4,G4,G4,D4,D4,A4,F4,F4,D4,D4,A4,F4,F4,C4,C4,E4,E4,F4,AS4,D5,A4,A4,F4,F4,F4,A4,F4,AS4,D5,A4,A4,F4,F4,F4,A4,F4,AS4,D5,A4,A4,F4,F4,F4,A4,F4,AS4,D5,A4,A4,F4,F4,F4,A4,F4};
int delays[] = {889,889,889,889,889,889,889,889,889,889,889,889,889,889,889,889,444,333,223,334,444,444,333,334,223,111,111,222,444,333,223,334,444,444,333,334,223,222,222,444,333,223,334,444,444,333,334,223,222,222,444,444,444,444,444,444,444,444,222,222,222,111,223,111,222,222,111,223,111,222,222,111,223,223,223,111,222,222,222,222,111,223,111,222,222,111,223,111,222,222,111,223,223,223,111,222,222,222,222,111,223,111,222,222,111,223,111,222,222,111,223,223,223,111,222,222,222,222,111,223,111,222,222,111,223,111,222,222,111,223,223,223,111,222,889,889,889,889,889,889,889,889,889,889,889,889,889,889,889,889,444,333,223,334,444,444,333,334,223,222,222,444,333,223,334,444,444,333,334,223,222,222,444,333,223,334,444,444,333,334,223,222,222,444,444,444,444,444,444,444,444,222,222,222,111,223,111,222,222,111,223,111,222,222,111,223,223,223,111,222,222,222,222,111,223,111,222,222,111,223,111,222,222,111,223,223,223,111,222,222,222,222,111,223,111,222,222,111,223,111,222,222,111,223,223,223,111,222,222,222,222,111,223,111,222,222,111,223,111,222,222,111,223,223,223,111,222,444,444,444,444,666,222,222,222,444,444,444,444,444,666,222,222,222,444,444,444,444,444,666,222,222,222,444,444,444,444,444,666,222,222,210,421};
void song() {  bool playing = true;    for (int i = 0; i < sizeof(delays) / sizeof(delays[0]); i++) {    tone(9, tones[i], delays[i]);    delay(delays[i] + 25);    if (analogRead(A0) <= 950) break;  }}void setup() {}void loop() {  if (analogRead(A0) > 950) song();}