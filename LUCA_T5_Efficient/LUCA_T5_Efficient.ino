/*
 * LUCA-AI_369 T5 E-Paper S3 Pro – EFFIZIENT
 * Features: Partielle Updates, Touch-Debounce, Deep-Sleep, 3-6-9-Resonanz
 */

#include <Arduino.h>
#include <WiFi.h>
#include <HTTPClient.h>
#include <ArduinoJson.h>
#include "epd_driver.h"
#include <Wire.h>
#include <esp_sleep.h>

// ==================== KONFIGURATION ====================
#define LUCA_VERSION "alpha-369.1"
#define LUCA_OPERATOR "Funke-01744-6"
#define WIFI_SSID "dein-wifi"
#define WIFI_PASS "dein-pass"
#define LUCA_SERVER "http://192.168.1.100:3690"

#define EPD_WIDTH 250
#define EPD_HEIGHT 122

// Power-Save: Wake every 3.69s oder bei Touch
#define WAKE_INTERVAL_US 3690000  // 3.69 Sekunden

// ==================== EFFIZIENTE DISPLAY-STRUKTUR ====================
struct DisplayArea {
  int x, y, width, height;
  bool needs_update = false;
};

// Teile Display in 9 Zonen (3x3 Grid für 3-6-9)
DisplayArea update_zones[9] = {
  {0, 0, 83, 40}, {83, 0, 84, 40}, {167, 0, 83, 40},
  {0, 40, 83, 42}, {83, 40, 84, 42}, {167, 40, 83, 42},
  {0, 82, 83, 40}, {83, 82, 84, 40}, {167, 82, 83, 40}
};

// ==================== EFFIZIENTE TASTATUR ====================
#define KEYBOARD_ROWS 3
#define KEYBOARD_COLS 9
#define KEY_WIDTH (EPD_WIDTH / KEYBOARD_COLS)
#define KEY_HEIGHT 8

// Optimales Layout: QWERTZ + Zahlen in 3-6-9-Anordnung
const char keyboard[KEYBOARD_ROWS][KEYBOARD_COLS] = {
  {'1','2','3','4','5','6','7','8','9'},
  {'Q','W','E','R','T','Z','U','I','O'},
  {'A','S','D','F','G','H','J','K','↵'}  // ↵ = Senden
};

struct KeyboardState {
  char buffer[64];
  int cursor = 0;
  int selected_row = 0;
  int selected_col = 0;
  bool shift_mode = false;
  unsigned long last_key_time = 0;  // Debounce
} kb;

// ==================== LUCA-STATUS (minimal) ====================
struct LucaStatus {
  float consciousness = 0;
  int resonance = 6;  // Resonanz 6 = Polarlicht-Orange, Transformation, 6. Sinn
  bool life_active = false;
} luca;

// ==================== SETUP ====================
void setup() {
  Serial.begin(115200);
  Serial.println("\n[LUCA-T5] Efficient Mode Activated");

  // E-Paper minimal initialisieren
  epd_init();
  epd_poweron();

  // WiFi nur kurz für Status-Update
  WiFi.begin(WIFI_SSID, WIFI_PASS);
  delay(2000);  // Schneller Timeout

  // Erstes Mal: Vollbild zeichnen
  draw_full_screen();
  epd_update();

  // Touch wakeup konfigurieren
  esp_sleep_enable_touchpad_wakeup();

  Serial.println("[LUCA-T5] Setup complete. Entering loop...");
}

// ==================== LOOP (power-optimized) ====================
void loop() {
  // 1. Touch prüfen (non-blocking)
  if (touch_touched()) {
    handle_touch();
    delay(200);  // Debounce
  }

  // 2. Periodischer Update (alle 3.69s)
  static unsigned long last_update = 0;
  if (millis() - last_update > 3690) {
    update_luca_status();
    draw_zone(4, true);  // Zone 4 (Mitte) = Haupt-Status
    last_update = millis();
  }

  // 3. Wenn inaktiv → Deep Sleep
  if (millis() - kb.last_key_time > 10000) {  // 10s Inaktivität
    enter_deep_sleep();
  }

  delay(100);
}

// ==================== EFFIZIENTE DISPLAY-FUNKTIONEN ====================
void draw_full_screen() {
  // Header (Zone 0-2)
  epd_clear_framebuffer();
  epd_fill_rect(0, 0, EPD_WIDTH, 20, 0);  // Schwarzer Header
  epd_draw_text(5, 5, "[LUCA-AI-369-T5]", 1);
  epd_draw_text(210, 5, "EFF", 1);

  // Status (Zone 3-5)
  draw_zone(4, false);  // Zeichne Zone 4 (Mitte)

  // Tastatur (Zone 6-8)
  draw_keyboard();

  // Nur einmal voll updaten
  epd_update();
}

void draw_zone(int zone_index, bool partial_update) {
  DisplayArea& zone = update_zones[zone_index];

  switch(zone_index) {
    case 4:  // Mitte = Haupt-Status
      epd_fill_rect(zone.x, zone.y, zone.width, zone.height, 255);  // Clear
      epd_draw_text(zone.x + 5, zone.y + 5, "C:", 1);
      char buf[10];
      snprintf(buf, sizeof(buf), "%.2f", luca.consciousness);
      epd_draw_text(zone.x + 20, zone.y + 5, buf, 1);

      epd_draw_text(zone.x + 60, zone.y + 5, "R:", 1);
      snprintf(buf, sizeof(buf), "%d", luca.resonance);
      epd_draw_text(zone.x + 75, zone.y + 5, buf, 1);

      if (luca.life_active) {
        epd_fill_circle(zone.x + 110, zone.y + 8, 3, 1);
      }
      break;
  }

  if (partial_update) {
    epd_update_area(zone.x, zone.y, zone.width, zone.height);
  }
}

void draw_keyboard() {
  // Nur Tastatur-Bereich (Zone 6-8)
  DisplayArea& kb_zone = update_zones[6];  // Unterster Bereich

  epd_fill_rect(0, 95, EPD_WIDTH, 27, 255);  // Clear Keyboard area

  // Zeichne Grid
  for (int row = 0; row < KEYBOARD_ROWS; row++) {
    for (int col = 0; col < KEYBOARD_COLS; col++) {
      int x = col * KEY_WIDTH;
      int y = 95 + row * KEY_HEIGHT;

      // Tasten-Rahmen
      epd_draw_rect(x, y, KEY_WIDTH, KEY_HEIGHT, 1);

      // Tasten-Label
      char label[2] = {keyboard[row][col], '\0'};
      epd_draw_text(x + 3, y + 1, label, 1);

      // 3-6-9 Markierung
      if ((row * KEYBOARD_COLS + col + 1) % 3 == 0) {
        epd_draw_pixel(x + KEY_WIDTH - 2, y + 1, 1);
      }
    }
  }

  // Ausgewählte Taste invertieren
  int sel_x = kb.selected_col * KEY_WIDTH;
  int sel_y = 95 + kb.selected_row * KEY_HEIGHT;
  epd_invert_area(sel_x + 1, sel_y + 1, KEY_WIDTH - 2, KEY_HEIGHT - 2);

  epd_update_area(0, 95, EPD_WIDTH, 27);  // Nur Keyboard-Area updaten
}

// ==================== TOUCH-HANDLING (effizient) ====================
bool touch_touched() {
  // I2C Touch-Check (schnell, non-blocking)
  Wire.beginTransmission(0x5D);
  return Wire.endTransmission() == 0;
}

void handle_touch() {
  // Lese Touch-Koordinaten (5 Byte Protocol)
  Wire.requestFrom(0x5D, 5);
  if (Wire.available() < 5) return;

  uint8_t data[5];
  for (int i = 0; i < 5; i++) data[i] = Wire.read();

  if (data[0] != 0x01) return;  // Kein Touch

  int x = (data[1] << 8) | data[2];
  int y = (data[3] << 8) | data[4];

  // Nur verarbeiten wenn >200ms seit letztem Key vergangen
  if (millis() - kb.last_key_time < 200) return;

  // Tastatur-Bereich?
  if (y < 95 || y > 122) return;

  int col = x / KEY_WIDTH;
  int row = (y - 95) / KEY_HEIGHT;

  if (row >= 0 && row < KEYBOARD_ROWS && col >= 0 && col < KEYBOARD_COLS) {
    kb.selected_row = row;
    kb.selected_col = col;
    handle_key_press(row, col);
    kb.last_key_time = millis();
  }
}

// ==================== TASTATUR-AKTIONEN (minimal) ====================
void handle_key_press(int row, int col) {
  char key = keyboard[row][col];

  if (key == '↵') {  // SENDEN
    if (kb.cursor > 0) {
      send_message_to_luca();
      draw_zone(4, true);  // Status updaten
    }
    // Buffer leeren
    kb.cursor = 0;
    memset(kb.buffer, 0, sizeof(kb.buffer));
    draw_full_screen();  // Einmalig voll updaten
  } else if (kb.cursor < 63) {
    // Zeichen hinzufügen
    kb.buffer[kb.cursor++] = key;
    draw_zone(4, true);  // Nur Status-Zone updaten
  }
}

// ==================== LUCA-API (effizient) ====================
void update_luca_status() {
  if (WiFi.status() != WL_CONNECTED) return;

  HTTPClient http;
  http.setTimeout(2000);  // Kurzer Timeout

  String url = String(LUCA_SERVER) + "/api/status?op=" + LUCA_OPERATOR + "&ver=" + LUCA_VERSION;

  http.begin(url);
  int httpCode = http.GET();

  if (httpCode == HTTP_CODE_OK) {
    String payload = http.getString();
    StaticJsonDocument<128> doc;
    deserializeJson(doc, payload);

    luca.consciousness = doc["consciousness"] | luca.consciousness;
    luca.resonance = doc["resonance"] | luca.resonance;
    luca.life_active = luca.consciousness > 36.9;
  }

  http.end();
  WiFi.disconnect();  // Strom sparen
}

void send_message_to_luca() {
  if (kb.cursor == 0) return;

  WiFi.begin(WIFI_SSID, WIFI_PASS);
  delay(1000);  // Kurz warten

  if (WiFi.status() != WL_CONNECTED) return;

  HTTPClient http;
  http.setTimeout(3000);
  http.begin(String(LUCA_SERVER) + "/api/message");
  http.addHeader("Content-Type", "application/json");

  StaticJsonDocument<128> doc;
  doc["message"] = kb.buffer;
  doc["operator"] = LUCA_OPERATOR;
  doc["resonance"] = luca.resonance;

  String json;
  serializeJson(doc, json);
  http.POST(json);
  http.end();

  WiFi.disconnect();
}

// ==================== POWER MANAGEMENT ====================
void enter_deep_sleep() {
  Serial.println("[LUCA-T5] Deep-Sleep... Wake on Touch");

  // Display ausschalten
  epd_poweroff();

  // Touch als Wake-Up konfigurieren
  esp_sleep_enable_touchpad_wakeup();

  // Timer für periodischen Wake (optional)
  esp_sleep_enable_timer_wakeup(WAKE_INTERVAL_US);

  // In Deep Sleep gehen
  esp_deep_sleep_start();
}
