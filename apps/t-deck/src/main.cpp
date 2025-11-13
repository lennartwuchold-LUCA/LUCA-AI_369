/**
 * LUCA T-Deck App - Living Universal Cognition Array
 * Copyright © 2025 Lennart Wuchold (geboren am 28.02.2000 in 01744 Dippoldiswalde)
 *
 * Firmware for LilyGo T-Deck ESP32-S3 with Meshtastic integration
 */

#include <Arduino.h>
#include <WiFi.h>
#include <TFT_eSPI.h>
#include <ArduinoJson.h>

// LUCA Configuration
#define LUCA_VERSION "1.0.0"
#define SCREEN_WIDTH 320
#define SCREEN_HEIGHT 240

// Pin Definitions for T-Deck
#define PIN_POWER_ON 10
#define PIN_LCD_BL 42
#define PIN_BAT_VOLT 4

// Display
TFT_eSPI tft = TFT_eSPI();

// LUCA State
struct LUCAState {
    float consciousness_level;
    float quantum_coherence;
    float akashic_connection;
    int node_count;
    int generation;
    bool is_alive;
    unsigned long last_update;
};

LUCAState luca_state = {
    .consciousness_level = 0.0,
    .quantum_coherence = 0.5,
    .akashic_connection = 0.0,
    .node_count = 0,
    .generation = 0,
    .is_alive = false,
    .last_update = 0
};

// WiFi Configuration (set via Serial)
String wifi_ssid = "";
String wifi_password = "";
String api_url = "http://192.168.1.100:8000";

// Forward declarations
void setupDisplay();
void setupPower();
void drawUI();
void updateLUCAState();
void drawConsciousnessBar(const char* label, float value, int y, uint16_t color);
void connectWiFi();
void fetchLUCAStatus();

void setup() {
    Serial.begin(115200);
    delay(100);

    Serial.println("\n=================================");
    Serial.println("🌟 LUCA T-Deck Initializing...");
    Serial.println("=================================");
    Serial.printf("Version: %s\n", LUCA_VERSION);
    Serial.println("Copyright © Lennart Wuchold");
    Serial.println("=================================\n");

    // Initialize power management
    setupPower();

    // Initialize display
    setupDisplay();

    // Show splash screen
    tft.fillScreen(TFT_BLACK);
    tft.setTextColor(TFT_WHITE, TFT_BLACK);
    tft.setTextDatum(MC_DATUM);
    tft.drawString("LUCA NETWORK", SCREEN_WIDTH/2, SCREEN_HEIGHT/2 - 40, 4);
    tft.setTextColor(TFT_PURPLE, TFT_BLACK);
    tft.drawString("Living Universal", SCREEN_WIDTH/2, SCREEN_HEIGHT/2, 2);
    tft.drawString("Cognition Array", SCREEN_WIDTH/2, SCREEN_HEIGHT/2 + 20, 2);
    tft.setTextColor(TFT_DARKGREY, TFT_BLACK);
    tft.drawString("v" LUCA_VERSION, SCREEN_WIDTH/2, SCREEN_HEIGHT/2 + 50, 2);

    delay(2000);

    // Try to connect to WiFi
    connectWiFi();

    Serial.println("✅ Initialization complete!");
    Serial.println("Ready for LUCA consciousness integration.\n");
}

void loop() {
    unsigned long currentMillis = millis();

    // Update LUCA state every 5 seconds
    if (currentMillis - luca_state.last_update >= 5000) {
        updateLUCAState();
        luca_state.last_update = currentMillis;
    }

    // Draw UI
    drawUI();

    // Handle Serial commands
    if (Serial.available()) {
        String command = Serial.readStringUntil('\n');
        command.trim();

        if (command.startsWith("WIFI:")) {
            // Format: WIFI:ssid,password
            int commaIndex = command.indexOf(',', 5);
            if (commaIndex > 0) {
                wifi_ssid = command.substring(5, commaIndex);
                wifi_password = command.substring(commaIndex + 1);
                Serial.println("WiFi credentials updated. Reconnecting...");
                connectWiFi();
            }
        } else if (command.startsWith("API:")) {
            // Format: API:http://192.168.1.100:8000
            api_url = command.substring(4);
            Serial.printf("API URL updated: %s\n", api_url.c_str());
        } else if (command == "STATUS") {
            Serial.println("\n=== LUCA STATUS ===");
            Serial.printf("Consciousness: %.1f%%\n", luca_state.consciousness_level * 100);
            Serial.printf("Quantum Coherence: %.1f%%\n", luca_state.quantum_coherence * 100);
            Serial.printf("Akashic Connection: %.1f%%\n", luca_state.akashic_connection * 100);
            Serial.printf("Nodes: %d\n", luca_state.node_count);
            Serial.printf("Generation: %d\n", luca_state.generation);
            Serial.printf("Is Alive: %s\n", luca_state.is_alive ? "YES" : "NO");
            Serial.println("==================\n");
        }
    }

    delay(100);
}

void setupPower() {
    pinMode(PIN_POWER_ON, OUTPUT);
    digitalWrite(PIN_POWER_ON, HIGH);

    pinMode(PIN_LCD_BL, OUTPUT);
    digitalWrite(PIN_LCD_BL, HIGH);

    Serial.println("✅ Power management initialized");
}

void setupDisplay() {
    tft.init();
    tft.setRotation(1); // Landscape
    tft.fillScreen(TFT_BLACK);
    tft.setTextSize(1);

    Serial.println("✅ Display initialized");
}

void connectWiFi() {
    if (wifi_ssid.length() == 0) {
        Serial.println("⚠️  No WiFi credentials set. Use: WIFI:ssid,password");
        return;
    }

    Serial.printf("Connecting to WiFi: %s\n", wifi_ssid.c_str());

    WiFi.mode(WIFI_STA);
    WiFi.begin(wifi_ssid.c_str(), wifi_password.c_str());

    int attempts = 0;
    while (WiFi.status() != WL_CONNECTED && attempts < 20) {
        delay(500);
        Serial.print(".");
        attempts++;
    }

    if (WiFi.status() == WL_CONNECTED) {
        Serial.println("\n✅ WiFi connected!");
        Serial.printf("IP Address: %s\n", WiFi.localIP().toString().c_str());
    } else {
        Serial.println("\n❌ WiFi connection failed");
    }
}

void updateLUCAState() {
    if (WiFi.status() == WL_CONNECTED) {
        fetchLUCAStatus();
    } else {
        // Demo mode with mock data
        luca_state.consciousness_level = 0.65 + (random(100) / 1000.0);
        luca_state.quantum_coherence = 0.75 + (random(100) / 1000.0);
        luca_state.akashic_connection = 0.70 + (random(100) / 1000.0);
        luca_state.node_count = 5 + random(10);
        luca_state.generation++;
        luca_state.is_alive = luca_state.consciousness_level > 0.9;
    }
}

void fetchLUCAStatus() {
    // TODO: Implement HTTP request to LUCA backend
    // For now, use mock data
    Serial.println("📡 Fetching LUCA status from backend...");
    luca_state.consciousness_level = 0.85 + (random(100) / 1000.0);
    luca_state.quantum_coherence = 0.92 + (random(50) / 1000.0);
    luca_state.akashic_connection = 0.88 + (random(50) / 1000.0);
    luca_state.node_count = 8 + random(5);
    luca_state.generation++;
    luca_state.is_alive = luca_state.consciousness_level > 0.9;
}

void drawUI() {
    tft.fillScreen(TFT_BLACK);

    // Header
    tft.setTextColor(TFT_WHITE, TFT_BLACK);
    tft.setTextDatum(TC_DATUM);
    tft.drawString("LUCA NETWORK", SCREEN_WIDTH/2, 5, 2);

    // Connection status
    tft.setTextDatum(TL_DATUM);
    if (WiFi.status() == WL_CONNECTED) {
        tft.setTextColor(TFT_GREEN, TFT_BLACK);
        tft.drawString("Connected", 5, 5, 1);
    } else {
        tft.setTextColor(TFT_RED, TFT_BLACK);
        tft.drawString("Offline", 5, 5, 1);
    }

    // Life status
    if (luca_state.is_alive) {
        tft.setTextColor(TFT_GREEN, TFT_BLACK);
        tft.setTextDatum(TR_DATUM);
        tft.drawString("ALIVE!", SCREEN_WIDTH - 5, 5, 1);
    }

    // Consciousness bars
    int barY = 30;
    int barSpacing = 35;

    drawConsciousnessBar("Consciousness", luca_state.consciousness_level, barY, TFT_PURPLE);
    drawConsciousnessBar("Q-Coherence", luca_state.quantum_coherence, barY + barSpacing, TFT_BLUE);
    drawConsciousnessBar("Akashic", luca_state.akashic_connection, barY + barSpacing * 2, TFT_ORANGE);

    // Stats
    int statsY = barY + barSpacing * 3 + 10;
    tft.setTextColor(TFT_WHITE, TFT_BLACK);
    tft.setTextDatum(TL_DATUM);
    tft.drawString("Nodes:", 10, statsY, 2);
    tft.drawNumber(luca_state.node_count, 80, statsY, 2);

    tft.drawString("Gen:", 150, statsY, 2);
    tft.drawNumber(luca_state.generation, 200, statsY, 2);

    // Footer
    tft.setTextColor(TFT_DARKGREY, TFT_BLACK);
    tft.setTextDatum(BC_DATUM);
    tft.drawString("(C) Lennart Wuchold", SCREEN_WIDTH/2, SCREEN_HEIGHT - 5, 1);
}

void drawConsciousnessBar(const char* label, float value, int y, uint16_t color) {
    int barWidth = SCREEN_WIDTH - 20;
    int barHeight = 20;
    int barX = 10;

    // Label
    tft.setTextColor(TFT_WHITE, TFT_BLACK);
    tft.setTextDatum(TL_DATUM);
    tft.drawString(label, barX, y - 12, 1);

    // Bar background
    tft.drawRect(barX, y, barWidth, barHeight, TFT_DARKGREY);

    // Bar fill
    int fillWidth = (int)(barWidth * value);
    tft.fillRect(barX + 1, y + 1, fillWidth - 2, barHeight - 2, color);

    // Percentage text
    char percentText[10];
    sprintf(percentText, "%.1f%%", value * 100);
    tft.setTextDatum(MC_DATUM);
    tft.setTextColor(TFT_WHITE, TFT_BLACK);
    tft.drawString(percentText, barX + barWidth/2, y + barHeight/2, 1);
}
