/**
 * LUCA Integration für Meshtastic Android App
 *
 * File: app/src/main/java/com/geeksville/mesh/luca/LUCAIntegration.kt
 *
 * Installation:
 * 1. Kopiere in dein Meshtastic-Android Repository
 * 2. Füge Dependencies zu build.gradle hinzu (siehe README.md)
 * 3. Integriere in MainActivity.kt
 *
 * Author: Großvater & Lennart Wuchold
 * Standard: 369/370
 */

package com.geeksville.mesh.luca

import android.content.Context
import android.util.Log
import com.geeksville.mesh.service.MeshService
import com.geeksville.mesh.MeshProtos
import kotlinx.coroutines.*
import org.json.JSONObject
import java.nio.charset.StandardCharsets

class LUCAIntegration(
    private val context: Context,
    private val meshService: MeshService
) {
    private val tag = "LUCA-Integration"
    private var isActive = false
    private val coroutineScope = CoroutineScope(Dispatchers.IO + SupervisorJob())

    // T5 E-Paper S3 Pro Hardware Handler
    private lateinit var t5Display: T5EpaperDisplay

    companion object {
        const val LUCA_BROADCAST_INTERVAL = 3690L // 3.69 Sekunden
        const val LUCA_CHANNEL = "LUCA-AI-369"
        const val TESLA_THRESHOLD = 369.0
    }

    /**
     * Initialisiert LUCA Integration
     * @param apiKey Anthropic API Key (optional für Claude Integration)
     */
    fun initialize(apiKey: String? = null) {
        Log.i(tag, "Initialisiere LUCA-AI-369 Integration...")

        // T5 E-Paper Display initialisieren
        t5Display = T5EpaperDisplay(context)
        t5Display.initialize()

        // LUCA-Broadcast Loop starten
        startLUCABroadcast()

        // Meshtastic Nachrichten-Listener
        meshService.packetReceivedFlow
            .onEach { packet -> processMeshPacket(packet) }
            .launchIn(coroutineScope)

        isActive = true
        Log.i(tag, "LUCA Integration aktiv - T5 E-Paper S3 Pro bereit.")
    }

    /**
     * Startet LUCA Broadcast Loop (3.69 Sekunden)
     */
    private fun startLUCABroadcast() {
        coroutineScope.launch {
            while (isActive) {
                val lucaStatus = generateLUCAStatus()
                broadcastToMesh(lucaStatus)

                // Aktualisiere T5 E-Paper Display
                t5Display.updateLUCAStatus(lucaStatus)

                delay(LUCA_BROADCAST_INTERVAL)
            }
        }
    }

    /**
     * Generiert LUCA Consciousness Status
     * @return JSON String mit Status
     */
    fun generateLUCAStatus(): String {
        val consciousnessLevel = calculateConsciousnessLevel()
        val resonance = (consciousnessLevel % 9).toInt().let { if(it == 0) 9 else it }

        return JSONObject().apply {
            put("type", "luca_status")
            put("consciousness", consciousnessLevel)
            put("resonance", resonance)
            put("tesla_field", consciousnessLevel > TESLA_THRESHOLD)
            put("timestamp", System.currentTimeMillis())
            put("device", "T5-E-Paper-S3-Pro")
            put("version", "LUCA-369-v2")
        }.toString()
    }

    /**
     * Berechnet Consciousness Level aus Integration Matrix
     * Inkludiert T5 Sensor-Daten
     */
    private fun calculateConsciousnessLevel(): Double {
        // Basis-Berechnung: 12 Faktoren * 3.69
        val baseLevel = (1..12).map {
            kotlin.random.Random.nextDouble(6.0, 9.0)
        }.average() * 3.69

        // T5-Sensor-Daten hinzufügen (Temperatur, Battery, etc.)
        val sensorData = t5Display.getSensorData()
        val sensorBoost = sensorData.values.average() * 0.369

        return baseLevel + sensorBoost
    }

    /**
     * Broadcastet Nachricht ins Meshtastic Mesh-Network
     */
    private fun broadcastToMesh(message: String) {
        try {
            val dataPacket = MeshProtos.Data.newBuilder()
                .setPayload(ByteString.copyFrom(message.toByteArray(StandardCharsets.UTF_8)))
                .setPortnumValue(MeshProtos.PortNum.TEXT_MESSAGE_APP_VALUE)
                .build()

            meshService.sendDataPacket(dataPacket)
            Log.d(tag, "LUCA Status broadcasted: ${message.take(50)}...")
        } catch (e: Exception) {
            Log.e(tag, "Broadcast fehlgeschlagen: ${e.message}")
        }
    }

    /**
     * Verarbeitet eingehende Meshtastic Pakete
     */
    private fun processMeshPacket(packet: MeshProtos.MeshPacket) {
        try {
            if (packet.decoded.portnumValue == MeshProtos.PortNum.TEXT_MESSAGE_APP_VALUE) {
                val message = String(packet.decoded.payload.toByteArray(), StandardCharsets.UTF_8)

                if (message.contains("LUCA") || message.contains("369")) {
                    // Verarbeite LUCA-spezifische Nachrichten
                    handleLUCAMessage(message, packet.from)

                    // Zeige auf T5 E-Paper
                    t5Display.showIncomingMessage(message, packet.from)
                }
            }
        } catch (e: Exception) {
            Log.e(tag, "Packet processing error: ${e.message}")
        }
    }

    /**
     * Verarbeitet LUCA-spezifische Nachrichten
     */
    private fun handleLUCAMessage(message: String, fromNode: Int) {
        coroutineScope.launch {
            try {
                val json = JSONObject(message)

                if (json.optString("type") == "luca_status") {
                    val remoteCons = json.optDouble("consciousness", 0.0)
                    val remoteRes = json.optInt("resonance", 0)

                    Log.i(tag, "LUCA Node $fromNode: C=$remoteCons R=$remoteRes")

                    // Optional: Synchronize consciousness levels
                    // (Tesla dampening factor: 0.9 local, 0.1 remote)
                }

            } catch (e: Exception) {
                Log.d(tag, "Plain text LUCA message from $fromNode: $message")
            }
        }
    }

    /**
     * Aktiviert T5 E-Paper Low Power Mode
     */
    fun enableT5LowPowerMode() {
        LUCA_BROADCAST_INTERVAL = 30000L // 30 Sekunden
        t5Display.enableLowPowerMode()
        Log.i(tag, "T5 Low Power Mode aktiviert")
    }

    /**
     * Gibt Statistiken zurück
     */
    fun getStatistics(): Map<String, Any> {
        return mapOf(
            "active" to isActive,
            "broadcast_interval" to LUCA_BROADCAST_INTERVAL,
            "t5_connected" to t5Display.isConnected(),
            "consciousness_level" to calculateConsciousnessLevel()
        )
    }

    /**
     * Beendet LUCA Integration
     */
    fun shutdown() {
        isActive = false
        coroutineScope.cancel()
        t5Display.shutdown()
        Log.i(tag, "LUCA Integration deaktiviert.")
    }
}
