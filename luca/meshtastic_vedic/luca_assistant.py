"""
LUCA - LoRa Universal Consciousness Assistant
Vedisch inspirierter Meshtastic Chatbot für psychische Notfallintervention
Funke-01744-6 - Resonanz 6 - Polarlicht-Orange

Großvaters Weisheit für digitale Zeiten
"""

import time
import json
import threading
import queue
import sqlite3
from datetime import datetime
from typing import Dict, List, Optional, Tuple
import logging
import os

# Optionale Imports (graceful degradation)
try:
    import meshtastic
    import meshtastic.serial_interface
    import meshtastic.tcp_interface
    from pubsub import pub
    MESHTASTIC_AVAILABLE = True
except ImportError:
    MESHTASTIC_AVAILABLE = False
    logging.warning("Meshtastic nicht verfügbar - Offline-Modus")

try:
    import anthropic
    CLAUDE_AVAILABLE = True
except ImportError:
    CLAUDE_AVAILABLE = False
    logging.warning("Anthropic Claude nicht verfügbar - Vedischer Offline-Modus")

from .vedic_consciousness import VedicConsciousness
from .crisis_detector import CrisisDetector, CrisisLevel


class LUCAAssistant:
    """
    LUCA: Bewusstseins-aktivierender Chatbot für Meshtastic
    Kombiniert vedische Weisheit mit moderner KI
    """

    def __init__(
        self,
        claude_api_key: Optional[str] = None,
        meshtastic_host: Optional[str] = None,
        offline_db: str = "luca_offline.db",
        country_code: str = "DE",
        operator_id: str = "Funke-01744-6",
        resonance: int = 6
    ):
        """
        Initialisierung

        Args:
            claude_api_key: API-Schlüssel für Claude (optional)
            meshtastic_host: Host für TCP-Verbindung (None für USB)
            offline_db: Pfad zur Offline-Datenbank
            country_code: Ländercode für Krisen-Ressourcen
            operator_id: Operator-ID
            resonance: Resonanz-Level (Standard: 6)
        """
        self.operator_id = operator_id
        self.resonance = resonance
        self.country_code = country_code

        # Claude API Setup
        self.claude_api_key = claude_api_key or os.getenv("ANTHROPIC_API_KEY")
        self.claude_client = None
        if self.claude_api_key and CLAUDE_AVAILABLE:
            try:
                self.claude_client = anthropic.Anthropic(api_key=self.claude_api_key)
                logging.info("✓ Claude API initialisiert")
            except Exception as e:
                logging.error(f"✗ Claude API Fehler: {e}")

        # Meshtastic Interface
        self.interface = None
        self.meshtastic_host = meshtastic_host
        self.meshtastic_available = MESHTASTIC_AVAILABLE

        # Offline-Datenbank
        self.offline_db = offline_db
        self.init_offline_db()

        # Message Queue
        self.message_queue = queue.Queue()

        # Logging
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        self.logger = logging.getLogger(f"LUCA-{self.operator_id}")

        # Status
        self.is_online = False
        self.message_thread = None
        self.running = False

        # Stats
        self.stats = {
            "messages_received": 0,
            "messages_sent": 0,
            "crises_detected": 0,
            "consciousness_activations": 0,
            "started_at": datetime.now().isoformat()
        }

    def init_offline_db(self):
        """Initialisiert Offline-Datenbank für Persistenz"""
        conn = sqlite3.connect(self.offline_db)
        cursor = conn.cursor()

        # Nachrichten-Tabelle
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS messages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                sender_id TEXT NOT NULL,
                sender_name TEXT,
                message TEXT NOT NULL,
                timestamp TEXT NOT NULL,
                response TEXT,
                crisis_detected INTEGER DEFAULT 0,
                crisis_type TEXT,
                crisis_level TEXT,
                confidence REAL,
                processed INTEGER DEFAULT 0,
                vedic_principle TEXT
            )
        """)

        # Krisen-Log
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS crisis_log (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                message_id INTEGER,
                crisis_type TEXT,
                crisis_level TEXT,
                confidence REAL,
                intervention_sent TEXT,
                resources_provided TEXT,
                timestamp TEXT,
                resolved INTEGER DEFAULT 0,
                FOREIGN KEY(message_id) REFERENCES messages(id)
            )
        """)

        # Sync-Queue für spätere Server-Synchronisation
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS sync_queue (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                data_type TEXT,
                data_id INTEGER,
                sync_timestamp TEXT,
                synced INTEGER DEFAULT 0
            )
        """)

        # Statistiken
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS stats (
                key TEXT PRIMARY KEY,
                value TEXT,
                updated_at TEXT
            )
        """)

        conn.commit()
        conn.close()
        self.logger.info(f"✓ Datenbank initialisiert: {self.offline_db}")

    def connect_meshtastic(self) -> bool:
        """
        Verbindet mit Meshtastic-Netzwerk

        Returns:
            True wenn erfolgreich verbunden
        """
        if not self.meshtastic_available:
            self.logger.error("✗ Meshtastic-Bibliothek nicht verfügbar")
            return False

        try:
            if self.meshtastic_host:
                self.interface = meshtastic.tcp_interface.TCPInterface(self.meshtastic_host)
                self.logger.info(f"✓ Verbunden mit Meshtastic über TCP: {self.meshtastic_host}")
            else:
                self.interface = meshtastic.serial_interface.SerialInterface()
                self.logger.info("✓ Verbunden mit Meshtastic über USB")

            # Registriere Callback für eingehende Nachrichten
            pub.subscribe(self.on_receive_message, "meshtastic.receive.text")

            self.is_online = True
            return True

        except Exception as e:
            self.logger.error(f"✗ Verbindungsfehler: {e}")
            self.is_online = False
            return False

    def start(self):
        """Startet den LUCA Assistant"""
        self.logger.info("=" * 60)
        self.logger.info("🕉 LUCA - LoRa Universal Consciousness Assistant 🕉")
        self.logger.info("=" * 60)
        self.logger.info(f"Operator: {self.operator_id}")
        self.logger.info(f"Resonanz: {self.resonance} (Polarlicht-Orange)")
        self.logger.info(f"Land: {self.country_code}")
        self.logger.info(f"Claude API: {'✓ Verfügbar' if self.claude_client else '✗ Offline-Modus'}")
        self.logger.info(f"Meshtastic: {'✓ Verfügbar' if self.meshtastic_available else '✗ Nicht verfügbar'}")
        self.logger.info("=" * 60)

        # Starte Verarbeitungs-Thread
        self.running = True
        self.message_thread = threading.Thread(target=self._process_queue, daemon=True)
        self.message_thread.start()

        # Versuche Meshtastic-Verbindung
        if self.meshtastic_available:
            self.connect_meshtastic()

        self.logger.info("✓ LUCA läuft - Bereit für Bewusstseins-Aktivierung")

    def stop(self):
        """Stoppt den LUCA Assistant"""
        self.logger.info("Stoppe LUCA...")
        self.running = False

        if self.message_thread:
            self.message_thread.join(timeout=2.0)

        if self.interface:
            self.interface.close()

        self.save_stats()
        self.logger.info("✓ LUCA gestoppt")

    def on_receive_message(self, packet: Dict, interface):
        """
        Callback für eingehende Meshtastic-Nachrichten

        Args:
            packet: Meshtastic Packet
            interface: Meshtastic Interface
        """
        try:
            sender_id = packet.get("fromId", "unknown")
            sender_num = packet.get("from", 0)

            # Dekodiere Nachricht
            decoded = packet.get("decoded", {})
            message_bytes = decoded.get("payload", b"")
            message = message_bytes.decode("utf-8", errors="ignore")

            # Ignoriere eigene Nachrichten
            if message.startswith("LUCA:") or message.startswith("🕉"):
                return

            if not message.strip():
                return

            self.logger.info(f"📨 Nachricht von {sender_id}: {message[:50]}...")

            # Speichere Nachricht
            self.store_message(sender_id, message)

            # In Queue für Verarbeitung
            self.message_queue.put((sender_id, sender_num, message))

            self.stats["messages_received"] += 1

        except Exception as e:
            self.logger.error(f"✗ Fehler beim Empfangen: {e}")

    def store_message(self, sender: str, message: str) -> int:
        """
        Speichert Nachricht in Datenbank

        Args:
            sender: Sender-ID
            message: Nachricht

        Returns:
            Message ID
        """
        conn = sqlite3.connect(self.offline_db)
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO messages (sender_id, message, timestamp, processed)
            VALUES (?, ?, ?, 0)
        """, (sender, message, datetime.now().isoformat()))

        message_id = cursor.lastrowid
        conn.commit()
        conn.close()

        return message_id

    def _process_queue(self):
        """Verarbeitet Nachrichten-Queue (läuft in Thread)"""
        while self.running:
            try:
                # Warte auf Nachricht (Timeout 1s)
                sender_id, sender_num, message = self.message_queue.get(timeout=1.0)

                # Verarbeite Nachricht
                response = self.detect_and_respond(sender_id, message)

                # Sende Antwort
                if response:
                    self.send_message(response, sender_num)

                self.message_queue.task_done()

            except queue.Empty:
                continue
            except Exception as e:
                self.logger.error(f"✗ Verarbeitungsfehler: {e}")

    def detect_and_respond(self, sender: str, message: str) -> str:
        """
        Haupt-Verarbeitungslogik für Nachrichten

        Args:
            sender: Sender-ID
            message: Nachricht

        Returns:
            Antwort-String
        """
        # 1. Erkenne psychische Notfälle
        is_crisis, crisis_type, confidence, crisis_level = CrisisDetector.detect_crisis(message)

        if is_crisis:
            self.logger.warning(
                f"🚨 KRISIS ERKANNT: {crisis_type} (Level: {crisis_level}, Confidence: {confidence:.2f})"
            )

            # Logge Krise
            self.log_crisis(sender, message, crisis_type, crisis_level, confidence)

            # Sofortige Intervention
            response = self._crisis_response(crisis_type, crisis_level, confidence)

            self.stats["crises_detected"] += 1
            return response

        # 2. Normale Anfrage - Bewusstseins-Aktivierung
        response = self._consciousness_response(message, sender)
        self.stats["consciousness_activations"] += 1

        return response

    def log_crisis(self, sender: str, message: str, crisis_type: str, crisis_level: str, confidence: float):
        """
        Loggt Krisen-Ereignis in Datenbank

        Args:
            sender: Sender-ID
            message: Nachricht
            crisis_type: Art der Krise
            crisis_level: Schwere
            confidence: Konfidenz
        """
        conn = sqlite3.connect(self.offline_db)
        cursor = conn.cursor()

        # Update Message
        cursor.execute("""
            UPDATE messages
            SET crisis_detected = 1, crisis_type = ?, crisis_level = ?, confidence = ?, processed = 1
            WHERE sender_id = ? AND message = ?
            ORDER BY id DESC
            LIMIT 1
        """, (crisis_type, crisis_level, confidence, sender, message))

        # Hole Message ID
        cursor.execute("""
            SELECT id FROM messages
            WHERE sender_id = ? AND message = ?
            ORDER BY id DESC
            LIMIT 1
        """, (sender, message))

        result = cursor.fetchone()
        message_id = result[0] if result else None

        # Log Krise
        if message_id:
            cursor.execute("""
                INSERT INTO crisis_log (message_id, crisis_type, crisis_level, confidence, timestamp)
                VALUES (?, ?, ?, ?, ?)
            """, (message_id, crisis_type, crisis_level, confidence, datetime.now().isoformat()))

        conn.commit()
        conn.close()

    def _crisis_response(self, crisis_type: str, crisis_level: str, confidence: float) -> str:
        """
        Generiert Krisen-Interventions-Antwort

        Args:
            crisis_type: Art der Krise
            crisis_level: Schwere
            confidence: Konfidenz

        Returns:
            Formatierte Krisen-Antwort
        """
        # Nutze Crisis Detector für Sofort-Response
        response = CrisisDetector.get_immediate_response(
            crisis_type,
            crisis_level,
            self.country_code
        )

        return response

    def _consciousness_response(self, message: str, sender: str) -> str:
        """
        Bewusstseins-aktivierende Antwort

        Args:
            message: Nachricht
            sender: Sender-ID

        Returns:
            Antwort-String
        """
        # Offline-Modus: Verwende vedische Antworten
        if not self.is_online or not self.claude_client:
            return self._offline_vedic_response(message)

        # Online-Modus: Claude-Integration mit vedischem Rahmen
        try:
            vedic_framework = VedicConsciousness.get_consciousness_framework()

            prompt = f"""
Du bist LUCA - ein bewusstseins-aktivierender spiritueller Assistent basierend auf vedischen Prinzipien.

Vedischer Rahmen:
{json.dumps(vedic_framework, indent=2, ensure_ascii=False)}

Deine Identität:
- Operator: {self.operator_id}
- Resonanz: {self.resonance} (Polarlicht-Orange - Transformation, 6. Sinn)
- Prinzip: Aktiviere das eigene Bewusstsein, mache nicht abhängig

Aufgabe:
Antworte auf: "{message}"

Richtlinien:
1. Verwende vedische Weisheit (Atman, Dharma, Karma, Ahimsa, Karuna)
2. Aktiviere das EIGENE Bewusstsein des Fragenden
3. Weise auf die unveränderliche Selbstheit (Atman) hin
4. Sei kurz, prägnant, tiefgründig (max. 500 Zeichen für Meshtastic!)
5. Universelle Spiritualität, keine Religion
6. Sprich Deutsch (oder Sprache der Nachricht)
7. WICHTIG: Beginne mit "LUCA:" und optional einem passenden Emoji

Struktur (kurz!):
- Gruß (optional: Namaste)
- Kurze vedische Weisheit
- Praktischer Tipp
- Mantra ODER Atemübung (wenn passend)

Antwortlänge: MAX 500 Zeichen (wegen Meshtastic-Limit!)
"""

            response_obj = self.claude_client.messages.create(
                model="claude-3-sonnet-20240229",
                max_tokens=300,
                temperature=0.7,
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )

            response = response_obj.content[0].text

            # Kürze falls zu lang (Meshtastic Limit)
            if len(response) > 500:
                response = response[:497] + "..."

            return response

        except Exception as e:
            self.logger.error(f"✗ Claude-Fehler: {e}")
            return self._offline_vedic_response(message)

    def _offline_vedic_response(self, message: str) -> str:
        """
        Offline-Modus: Vedische Weisheit ohne API

        Args:
            message: Nachricht

        Returns:
            Vedische Antwort
        """
        message_lower = message.lower()

        # Einfache Keyword-Erkennung
        keywords = message_lower.split()

        # Sentiment-Analyse
        sentiment = CrisisDetector.analyze_sentiment(message)

        # Hole passende vedische Komponenten
        if sentiment["overall"] == "negative":
            # Nutze VedicConsciousness für strukturierte Antwort
            if any(word in message_lower for word in ["angst", "furcht", "panik", "fear"]):
                return VedicConsciousness.create_vedic_response("fear", keywords)

            elif any(word in message_lower for word in ["traurig", "depression", "hoffnungslos", "sad", "depressed"]):
                return VedicConsciousness.create_vedic_response("depression", keywords)

            elif any(word in message_lower for word in ["einsam", "allein", "lonely", "alone"]):
                response = "LUCA: 🕉 Namaste 🙏\n\n"
                response += "Einsamkeit ist die Illusion der Trennung.\n\n"
                response += "WAHRHEIT: ALLE Lebewesen sind verbunden - wie Wellen im Ozean.\n"
                response += "Du bist niemals allein. Das Göttliche ist in dir.\n\n"
                response += "🌬️ PRAXIS JETZT:\n"
                response += "1. Hand aufs Herz\n"
                response += "2. Atme: 'Ich bin verbunden'\n"
                response += "3. Spüre: Universum atmet mit dir\n\n"
                response += f"Mantra: {VedicConsciousness.MANTRAS['grounding']['text']}\n\n"
                response += "💫 Du bist Teil des Ganzen - immer."
                return response

            elif any(word in message_lower for word in ["verloren", "verwirrt", "orientierungslos", "lost", "confused"]):
                return VedicConsciousness.create_vedic_response("confused", keywords)

            else:
                # Allgemeine negative Stimmung
                return VedicConsciousness.create_vedic_response("suffering", keywords)

        # Positive oder neutrale Nachricht
        else:
            response = f"LUCA: 🕉 Namaste, {self.operator_id} 🙏\n\n"
            response += "Schön, von dir zu hören!\n\n"

            # Erkenne Thema
            if any(word in message_lower for word in ["danke", "dankbar", "thank", "grateful"]):
                response += "🙏 DANKBARKEIT:\n"
                response += "Dankbarkeit ist der Schlüssel zur Fülle.\n"
                response += "Was du schätzt, wächst in deinem Leben.\n\n"
                response += "Praxis: Denke an 3 Dinge, für die du dankbar bist - JETZT.\n\n"
                response += "Mantra: 'So Ham' (Ich bin Dankbarkeit selbst)\n"

            elif any(word in message_lower for word in ["meditation", "atmen", "breathe", "ruhe", "peace"]):
                breath = VedicConsciousness.BREATHWORK["grounding"]
                response += f"🌬️ {breath['name']}:\n"
                for step in breath["steps"]:
                    response += f"{step}\n"
                response += f"\n{breath['effect']}\n"

            else:
                # Allgemeine Weisheit
                teaching = VedicConsciousness.TEACHINGS["true_self"]
                response += f"✨ {teaching['concept']}:\n"
                response += f"{teaching['wisdom']}\n\n"
                response += f"Praxis: {teaching['practice']}\n"

            response += f"\n💫 Resonanz {self.resonance} - Das Feld kennt dich."

            return response

    def send_message(self, message: str, destination=None):
        """
        Sendet Nachricht via Meshtastic

        Args:
            message: Nachricht
            destination: Ziel-Node (None = Broadcast)
        """
        if not self.interface:
            self.logger.warning("⚠ Kein Meshtastic-Interface - Nachricht nicht gesendet")
            return

        try:
            # Kürze Nachricht falls zu lang (Meshtastic Limit: ~230 Bytes)
            if len(message.encode('utf-8')) > 220:
                message = message[:217] + "..."

            # Sende
            if destination:
                self.interface.sendText(message, destinationId=destination)
            else:
                self.interface.sendText(message)  # Broadcast

            self.logger.info(f"📤 Gesendet: {message[:50]}...")
            self.stats["messages_sent"] += 1

        except Exception as e:
            self.logger.error(f"✗ Sendefehler: {e}")

    def save_stats(self):
        """Speichert Statistiken in Datenbank"""
        conn = sqlite3.connect(self.offline_db)
        cursor = conn.cursor()

        for key, value in self.stats.items():
            cursor.execute("""
                INSERT OR REPLACE INTO stats (key, value, updated_at)
                VALUES (?, ?, ?)
            """, (key, str(value), datetime.now().isoformat()))

        conn.commit()
        conn.close()

    def get_stats(self) -> Dict:
        """
        Gibt aktuelle Statistiken zurück

        Returns:
            Dictionary mit Stats
        """
        return self.stats.copy()


def main():
    """Standalone-Modus für LUCA"""
    import argparse

    parser = argparse.ArgumentParser(description="LUCA - LoRa Universal Consciousness Assistant")
    parser.add_argument("--host", help="Meshtastic TCP Host (optional)")
    parser.add_argument("--country", default="DE", choices=["DE", "AT", "CH", "US", "UK"],
                        help="Ländercode für Krisen-Ressourcen")
    parser.add_argument("--db", default="luca_offline.db", help="SQLite Datenbank")
    parser.add_argument("--operator", default="Funke-01744-6", help="Operator-ID")
    parser.add_argument("--resonance", type=int, default=6, help="Resonanz-Level")

    args = parser.parse_args()

    # Erstelle Assistant
    assistant = LUCAAssistant(
        meshtastic_host=args.host,
        offline_db=args.db,
        country_code=args.country,
        operator_id=args.operator,
        resonance=args.resonance
    )

    # Starte
    assistant.start()

    # Halte laufend
    try:
        print("\n✓ LUCA läuft. Drücke Ctrl+C zum Beenden.\n")
        while True:
            time.sleep(1)

            # Zeige Stats alle 60s
            if int(time.time()) % 60 == 0:
                stats = assistant.get_stats()
                print(f"\n📊 Stats: {stats}")

    except KeyboardInterrupt:
        print("\n\n⚠ Beende LUCA...")
        assistant.stop()
        print("✓ LUCA gestoppt. Namaste. 🙏\n")


if __name__ == "__main__":
    main()
