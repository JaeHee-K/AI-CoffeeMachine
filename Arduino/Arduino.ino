// Coffee Machine Control

/* Pin_information
 *  8 : Espresoo / Up
 *  9 : Americano / Down
 *  10 : ESC
 *  11 : Menu / Ok
 *  4 : Power
 */
int pin[] = {8, 9, 10, 11, 4};

/* 상태
 * 온도, 원두 분쇄 정도 (총 3단계)
 * 0 : Low
 * 1 : Medium
 * 2 : High
 */
int temp = 1;
int grind = 1;

// default : 70ml
int espresso = 5;
int e_arr[] = { 20, 30, 40, 50, 60, 70, 80, 90 };
// default : 160ml
int americano = 5;
int a_arr[] = { 90, 100, 120, 140, 150, 160, 180, 200 };

// 1 : 에스프레소, 2 : 아메리카노
int coffee = 0;

// 아메리카노 물 양 조절 여부
bool water = false;
 
void setup() {
  Serial.begin(9600);

  // pinMode 설정 및 릴레이 초기 상태 지정
  for (int i = 0; i < sizeof(pin); i++)
  {
    pinMode(pin[i], OUTPUT);
    digitalWrite(pin[i], LOW);
  }
}

void loop() {
  if (Serial.available()) {
    char c = Serial.read();

    int num = sync(c);

    // 서버로부터 들어온 데이터와 커피머신 이전 설정 비교
    if ('0' <= c && c <= '9') {
      // Americano
      if ('1' <= c && c <='5') {
        if (num != americano) {
          menu_select(c);
          move(americano, num, c);

          // 아메리카노 물양 갱신
          americano = num;
          // 커피 종류 아메리카노로 지정
          coffee = 2;
        }
      }
      // Espresso
      else {
        if (num != espresso) {
          menu_select(c);
          move(espresso, num, c);

          // 에스프레소 물양 갱신
          espresso = num;
          // 커피 종류 에스프레소로 지정
          coffee = 1;
        }
      }
      
      
    }
    else if ('a' <= c && c <= 'c') {
      if (num != temp) {
        // 온도 조절
        menu_select(c);
        move(temp, num, c);

        temp = num;
      }
    }
    else if ('d' <= c && c <= 'f') {
      if (num != grind) {
        // grind 조절
        menu_select(c);
        move(grind, num, c);

        grind = num;
      }

      // 커피 추출
      // 에스프레소 추출
      if (coffee == 1) { button(0); }     
      else if (coffee == 2) { button(1); }
    }
  }
    
  delay(100);
}

// 버튼 누르기
void button(int i)
{
  digitalWrite(pin[i], HIGH);
  delay(500);
  digitalWrite(pin[i], LOW);
  delay(500);
}

// 설정 메뉴 들어가기
void menu_select(char c)
{
  // Menu
  button(3);
  // Ok
  button(3);

  // 1. cup capacity
  if ('0' <= c && c <= '9') {
    button(3);
    // Americano = big cup
    if ('1' <= c && c <= '5') {
      // 바로 전에 아메리카노 물양을 바꿨으면 바로 확인버튼 누르기
      if (water) { button(3); }
      else {
        button(1);
        button(3);
      }
      water = true;
    }
    // Espresso = small cup
    else {
      if (water) {
        button(1);
        button(3);
      }
      else { button(3); }
      
      water = false;
    }
  }
  // 2. temperature
  else if ('a' <= c && c <= 'c') {
    button(1);
    button(3);
  }
  // 3. grind quantity
  else {
    button(1);
    button(1);
    button(3);
  }
}

// 물 양 조절
void move(int x, int y, char c)
{
  /* Menu Up&Down
   1 : Down
   0 : Up */
  int forward = 1;
  // 움직이는 횟수
  int move = (y - x);
  
  // 물 양 조절
  if ('0' <= c && c <= '9') {
    if (move > 0){
      if (move > 4) {
        forward = 0;
        move = 8 - move;
      }
    }
    else {
      move = abs(move);
      forward = 0;
      if (move > 4) { move = 8 - move; }
    }
    
    for (int i = 0; i < move; i++) {
      if (forward) { button(1); }
      else { button(0); }
    }
  }
  // 온도 조절
  else if ('a' <= c && c <= 'c') {
    if ((x > y) || (x == 0 && y == 2)) { forward = 0; }
    
    if (forward) { button(1); }
    else { button(0); }
  }
  // 분쇄 정도 조절
  else if ('d' <= c && c <= 'f') {
    if (x > y) {
      if ((x != 2) || (y != 0)) { forward = 0; }
    }
    else if (x == 0 && y == 2) {
      forward = 0;
    }
    
    for (int i = 0; i < 2; i++) {
      if (forward) { button(1); }
      else { button(0); }
    }
  }
  
  // Ok
  button(3);
  // Esc
  button(2);
  if ('0' <= c && c <= '9') {
    // Esc
  button(2);
  }
  // 1. No saving, 2. Saving --> 2번 선택하기 위해 Down
  button(1);
  // Ok
  button(3);
  // Esc (-> ready for use select)
  button(2);
}

// 서버에서 받은 값 -> 커피 레벨
int sync(char c)
{
  int i = -1;

  switch(c)
  {
    case '1':
          i = 7;
          break;
    case '2':
          i = 5;
          break;
    case '3':
          i = 4;
          break;
    case '4':
          i = 2;
          break;
    case '5':
          i = 0;
          break;
    case '6':
          i = 6;
          break;
    case '7':
          i = 5;
          break;
    case '8':
          i = 4;
          break;
    case '9':
          i = 3;
          break;
    case '0':
          i = 1;
          break;
    case 'a':
    case 'd':
          i = 0;
          break;
    case 'b':
    case 'e':
          i = 1;
          break;
    case 'c':
    case 'f':
          i = 2;
          break;
  }
  return i;
}
