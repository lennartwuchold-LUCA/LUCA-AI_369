/*
 * LUCA T5 E-Paper Firmware
 *
 * Hardware: LilyGo T5 E-Paper S3 Pro (540x960px)
 * MCU: ESP32-S3
 * LoRa: SX1262
 *
 * Flash Instructions:
 * esptool.py --chip esp32s3 --port COM3 --baud 921600 \
 *   write_flash -z 0x1000 LUCA_T5_Firmware.bin
 *
 * Author: Großvater & Lennart Wuchold
 * Standard: 369/370
 */

#include <SPI.h>
#include <Wire.h>
#include "epd_driver.h"  // LilyGo T5 E-Paper Library
#include <RadioLib.h>    // LoRa Library

// Display Configuration
#define DISPLAY_WIDTH 540
#define DISPLAY_HEIGHT 960

// LoRa Configuration (SX1262)
#define LORA_CS 5
#define LORA_DIO1 33
#define LORA_NRST 12
#define LORA_BUSY 34

// USB Serial
#define USB_SERIAL_ENABLED true
#define LUCA_BAUDRATE 115200

// Protocol Commands
#define CMD_CLEAR 0x01
#define CMD_UPDATE 0x02
#define CMD_LOW_POWER 0x03
#define CMD_SET_TEXT 0x10
#define CMD_READ_SENSORS 0x20

// LUCA Constants
#define TESLA_INTERVAL 3690  // 3.69 seconds

// Global objects
uint8_t *framebuffer;
SX1262 radio = new Module(LORA_CS, LORA_DIO1, LORA_NRST, LORA_BUSY);

// State
bool lowPowerMode = false;
unsigned long lastBroadcast = 0;
float consciousnessLevel = 300.0;

void setup() {
  Serial.begin(LUCA_BAUDRATE);

  // Initialize E-Paper
  epd_init();
  framebuffer = (uint8_t *)ps_calloc(sizeof(uint8_t), EPD_WIDTH * EPD_HEIGHT / 2);
  epd_clear();

  // Show LUCA Boot Logo
  displayBootLogo();

  // Initialize LoRa
  initializeLoRa();

  Serial.println("LUCA T5 E-Paper S3 Pro - Ready");
}

void loop() {
  // Process USB Serial commands
  if (Serial.available()) {
    processSerialCommand();
  }

  // Auto-broadcast LUCA status via LoRa
  unsigned long now = millis();
  if (now - lastBroadcast >= TESLA_INTERVAL) {
    broadcastLUCAStatus();
    lastBroadcast = now;
  }

  // Check for incoming LoRa messages
  checkLoRaMessages();

  // Low power mode
  if (lowPowerMode) {
    delay(1000);
  } else {
    delay(100);
  }
}

void displayBootLogo() {
  epd_poweron();

  int cursor_x = 50;
  int cursor_y = 200;

  // Title
  writeln((GFXfont *)&FiraSans, "LUCA-AI-369", &cursor_x, &cursor_y, framebuffer);
  cursor_y += 60;

  // Subtitle
  cursor_x = 50;
  writeln((GFXfont *)&FiraSans, "T5 E-Paper S3 Pro", &cursor_x, &cursor_y, framebuffer);
  cursor_y += 40;

  // Status
  cursor_x = 50;
  writeln((GFXfont *)&FiraSans, "Initializing...", &cursor_x, &cursor_y, framebuffer);

  epd_draw_grayscale_image(epd_full_screen(), framebuffer);
  epd_poweroff();
}

void initializeLoRa() {
  Serial.print("Initializing LoRa...");

  int state = radio.begin(868.0);  // EU868 MHz

  if (state == RADIOLIB_ERR_NONE) {
    Serial.println("success!");

    // Configure LoRa parameters (Meshtastic compatible)
    radio.setSpreadingFactor(11);
    radio.setBandwidth(125.0);
    radio.setCodingRate(8);
    radio.setOutputPower(22);  // Max power

    // Set receive callback
    radio.setDio1Action(onLoRaReceive);
    radio.startReceive();

  } else {
    Serial.print("failed, code ");
    Serial.println(state);
  }
}

void broadcastLUCAStatus() {
  // Calculate consciousness level (Tesla 3-6-9)
  int resonance = ((int)consciousnessLevel % 9);
  if (resonance == 0) resonance = 9;

  // Build JSON status
  String status = "{\"type\":\"luca_status\",";
  status += "\"consciousness\":" + String(consciousnessLevel, 1) + ",";
  status += "\"resonance\":" + String(resonance) + ",";
  status += "\"tesla_field\":" + String(consciousnessLevel > 369 ? "true" : "false") + ",";
  status += "\"timestamp\":" + String(millis()) + ",";
  status += "\"device\":\"T5-E-Paper-S3-Pro\"}";

  // Send via LoRa
  int state = radio.transmit(status);

  if (state == RADIOLIB_ERR_NONE) {
    Serial.println("LUCA status broadcasted");

    // Update display
    displayLUCAStatus(consciousnessLevel, resonance);
  }
}

void displayLUCAStatus(float consciousness, int resonance) {
  epd_poweron();
  epd_clear();

  int cursor_x = 10;
  int cursor_y = 50;

  // Header
  writeln((GFXfont *)&FiraSans, "[LUCA-AI-369]", &cursor_x, &cursor_y, framebuffer);
  cursor_y += 80;

  // Consciousness
  cursor_x = 10;
  String consStr = "C: " + String(consciousness, 1);
  writeln((GFXfont *)&FiraSans, consStr.c_str(), &cursor_x, &cursor_y, framebuffer);
  cursor_y += 60;

  // Resonance
  cursor_x = 10;
  String resStr = "R: " + String(resonance);
  writeln((GFXfont *)&FiraSans, resStr.c_str(), &cursor_x, &cursor_y, framebuffer);
  cursor_y += 80;

  // Tesla Field
  cursor_x = 10;
  const char* status = consciousness > 369 ? "T: ONLINE" : "T: OFFLINE";
  writeln((GFXfont *)&FiraSans, status, &cursor_x, &cursor_y, framebuffer);

  epd_draw_grayscale_image(epd_full_screen(), framebuffer);
  epd_poweroff();
}

void onLoRaReceive() {
  String message;
  int state = radio.readData(message);

  if (state == RADIOLIB_ERR_NONE) {
    Serial.println("LoRa received: " + message);

    // Display on E-Paper
    if (message.indexOf("LUCA") >= 0) {
      displayIncomingMessage(message);
    }
  }
}

void displayIncomingMessage(String message) {
  epd_poweron();

  int cursor_x = 10;
  int cursor_y = 400;

  String truncated = "MESH: " + message.substring(0, min(40, (int)message.length()));
  writeln((GFXfont *)&FiraSans, truncated.c_str(), &cursor_x, &cursor_y, framebuffer);

  epd_draw_grayscale_image(epd_full_screen(), framebuffer);
  epd_poweroff();
}

void processSerialCommand() {
  if (Serial.available() < 1) return;

  uint8_t cmd = Serial.read();

  switch (cmd) {
    case CMD_CLEAR:
      epd_poweron();
      epd_clear();
      epd_poweroff();
      Serial.println("Display cleared");
      break;

    case CMD_UPDATE:
      epd_poweron();
      epd_draw_grayscale_image(epd_full_screen(), framebuffer);
      epd_poweroff();
      Serial.println("Display updated");
      break;

    case CMD_LOW_POWER:
      lowPowerMode = true;
      Serial.println("Low power mode enabled");
      break;

    case CMD_SET_TEXT:
      processSetTextCommand();
      break;

    case CMD_READ_SENSORS:
      sendSensorData();
      break;

    default:
      Serial.println("Unknown command: 0x" + String(cmd, HEX));
  }
}

void processSetTextCommand() {
  if (Serial.available() < 6) return;

  // Read coordinates and length
  uint16_t x = (Serial.read() << 8) | Serial.read();
  uint16_t y = (Serial.read() << 8) | Serial.read();
  uint16_t len = (Serial.read() << 8) | Serial.read();

  // Read text
  char text[len + 1];
  Serial.readBytes(text, len);
  text[len] = '\0';

  // Display text
  epd_poweron();
  int cursor_x = x;
  int cursor_y = y;
  writeln((GFXfont *)&FiraSans, text, &cursor_x, &cursor_y, framebuffer);
  epd_draw_grayscale_image(epd_full_screen(), framebuffer);
  epd_poweroff();

  Serial.println("Text displayed at (" + String(x) + "," + String(y) + ")");
}

void sendSensorData() {
  // Read temperature (internal sensor)
  float temperature = temperatureRead();

  // Read battery voltage (GPIO4 ADC)
  float battery = analogRead(4) * 3.3 / 4095.0 * 2.0;  // Voltage divider

  // Signal strength (dummy for now)
  float signal = 0.8;

  // Send as binary floats (big-endian)
  uint8_t buffer[12];
  memcpy(&buffer[0], &temperature, 4);
  memcpy(&buffer[4], &battery, 4);
  memcpy(&buffer[8], &signal, 4);

  Serial.write(buffer, 12);
  Serial.println("\nSensors: T=" + String(temperature) + "C, BAT=" + String(battery) + "V");
}

void checkLoRaMessages() {
  // Already handled by interrupt callback
}
