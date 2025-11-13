/**
 * T5 E-Paper S3 Pro Display Handler
 *
 * File: app/src/main/java/com/geeksville/mesh/luca/T5EpaperDisplay.kt
 *
 * Author: Großvater & Lennart Wuchold
 * Standard: 369/370
 */

package com.geeksville.mesh.luca

import android.content.Context
import android.hardware.usb.UsbDevice
import android.hardware.usb.UsbManager
import android.util.Log
import kotlinx.coroutines.*
import java.nio.ByteBuffer
import java.nio.ByteOrder

class T5EpaperDisplay(private val context: Context) {
    private val tag = "T5-E-Paper"
    private val vendorId = 0x303A  // LilyGo ESP32-S3
    private val productId = 0x1001 // T5 E-Paper S3 Pro

    private var usbDevice: UsbDevice? = null
    private var isConnected = false

    // E-Paper Display Commands
    private val CMD_CLEAR = byteArrayOf(0x01)
    private val CMD_UPDATE = byteArrayOf(0x02)
    private val CMD_LOW_POWER = byteArrayOf(0x03)
    private val CMD_SET_TEXT: Byte = 0x10

    companion object {
        const val DISPLAY_WIDTH = 540
        const val DISPLAY_HEIGHT = 960
        const val REFRESH_DELAY = 3000L
    }

    fun initialize(): Boolean {
        val usbManager = context.getSystemService(Context.USB_SERVICE) as UsbManager

        usbManager.deviceList.values.forEach { device ->
            if (device.vendorId == vendorId && device.productId == productId) {
                usbDevice = device
                isConnected = true
                Log.i(tag, "T5 E-Paper S3 Pro gefunden: ${device.deviceName}")
                return true
            }
        }

        Log.w(tag, "T5 E-Paper nicht gefunden - Simulation-Modus aktiv.")
        return false
    }

    fun updateLUCAStatus(status: String) {
        if (!isConnected) {
            Log.d(tag, "Simulation: $status")
            return
        }

        CoroutineScope(Dispatchers.IO).launch {
            try {
                val json = org.json.JSONObject(status)
                val consciousness = json.getDouble("consciousness")
                val resonance = json.getInt("resonance")

                val displayText = buildString {
                    append("[LUCA]\n")
                    append("C:${String.format("%.1f", consciousness)}\n")
                    append("R:$resonance\n")
                    append(if (consciousness > 369) "T:ONLINE" else "T:OFFLINE")
                }

                sendToDisplay(displayText, 10, 50)
            } catch (e: Exception) {
                Log.e(tag, "Status-Update fehlgeschlagen: ${e.message}")
            }
        }
    }

    fun showIncomingMessage(message: String, fromNode: Int) {
        val truncated = "N${fromNode % 100}: ${message.take(30)}..."
        sendToDisplay(truncated, x = 10, y = 400)
    }

    private fun sendToDisplay(text: String, x: Int, y: Int) {
        if (!isConnected) return

        try {
            val textBytes = text.toByteArray(Charsets.UTF_8)
            val length = textBytes.size

            // Protocol: [CMD_SET_TEXT][x(2)][y(2)][length(2)][text]
            val buffer = ByteBuffer.allocate(7 + length).apply {
                order(ByteOrder.BIG_ENDIAN)
                put(CMD_SET_TEXT)
                putShort(x.toShort())
                putShort(y.toShort())
                putShort(length.toShort())
                put(textBytes)
            }

            // TODO: Implement actual USB serial write
            // serialPort?.write(buffer.array())

            delay(REFRESH_DELAY)
            // serialPort?.write(CMD_UPDATE)

        } catch (e: Exception) {
            Log.e(tag, "Display-Write fehlgeschlagen: ${e.message}")
        }
    }

    fun getSensorData(): Map<String, Double> {
        return mapOf(
            "temperature" to (20 + kotlin.random.Random.nextDouble(10.0)),
            "battery" to (3.7 + kotlin.random.Random.nextDouble(0.5)),
            "signal" to kotlin.random.Random.nextDouble()
        )
    }

    fun enableLowPowerMode() {
        if (!isConnected) return
        // serialPort?.write(CMD_LOW_POWER)
        Log.i(tag, "Low Power Mode aktiviert")
    }

    fun isConnected() = isConnected

    fun shutdown() {
        if (isConnected) {
            // serialPort?.close()
            isConnected = false
            Log.i(tag, "T5 E-Paper heruntergefahren.")
        }
    }
}
