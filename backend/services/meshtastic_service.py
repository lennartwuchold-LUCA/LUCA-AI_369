"""
Meshtastic Service - Decentralized Communication
Enables LUCA to work in offline/censored environments via Meshtastic mesh network

This allows people in Gaza, Ukraine, Africa, and other areas with limited internet
to access LUCA through Meshtastic devices.
"""

import json
import asyncio
from typing import Optional, Dict, Any, List
from datetime import datetime
from sqlalchemy.orm import Session
from backend.models import MeshtasticMessage
from backend.config import settings
import logging

logger = logging.getLogger(__name__)


class MeshtasticService:
    """
    Service for Meshtastic mesh network integration

    Meshtastic is a project that lets you use inexpensive LoRa radios as a long-range,
    off-grid communication platform. Perfect for:
    - Disaster scenarios
    - Censored regions
    - Remote areas without internet
    - Conflict zones
    """

    def __init__(self, db: Session):
        self.db = db
        self.enabled = settings.MESHTASTIC_ENABLED
        self.interface = None
        self.connected = False

        if self.enabled:
            self._initialize_connection()

    def _initialize_connection(self):
        """Initialize Meshtastic connection"""
        try:
            # Try to import meshtastic (optional dependency)
            import meshtastic
            import meshtastic.serial_interface
            import meshtastic.tcp_interface

            if settings.MESHTASTIC_INTERFACE == "serial":
                # Serial connection (USB)
                port = settings.MESHTASTIC_PORT or "/dev/ttyUSB0"
                self.interface = meshtastic.serial_interface.SerialInterface(port)
                logger.info(f"✅ Meshtastic connected via serial: {port}")

            elif settings.MESHTASTIC_INTERFACE == "tcp":
                # TCP connection (network)
                host = settings.MESHTASTIC_HOST or "localhost"
                self.interface = meshtastic.tcp_interface.TCPInterface(hostname=host)
                logger.info(f"✅ Meshtastic connected via TCP: {host}")

            else:
                logger.warning(f"⚠️  Unsupported Meshtastic interface: {settings.MESHTASTIC_INTERFACE}")
                return

            self.connected = True
            self._setup_message_handler()

        except ImportError:
            logger.warning("⚠️  Meshtastic library not installed. To enable Meshtastic:")
            logger.warning("    pip install meshtastic")
            self.enabled = False
        except Exception as e:
            logger.error(f"❌ Failed to initialize Meshtastic: {e}")
            self.enabled = False

    def _setup_message_handler(self):
        """Setup handler for incoming Meshtastic messages"""
        if not self.interface:
            return

        def on_receive(packet, interface):
            """Handle received packet"""
            try:
                asyncio.create_task(self._handle_incoming_message(packet))
            except Exception as e:
                logger.error(f"Error handling Meshtastic message: {e}")

        self.interface.on_receive = on_receive

    async def _handle_incoming_message(self, packet: Dict[str, Any]):
        """Process incoming Meshtastic message"""
        try:
            # Extract message data
            if "decoded" not in packet:
                return

            decoded = packet["decoded"]

            # Check if it's a text message for LUCA
            if decoded.get("portnum") != "TEXT_MESSAGE_APP":
                return

            payload = decoded.get("text", "")

            # Check if message is for LUCA (starts with !luca)
            if not payload.lower().startswith("!luca"):
                return

            # Extract the actual query
            query = payload[5:].strip()  # Remove "!luca" prefix

            # Get sender info
            from_id = packet.get("fromId", "unknown")
            to_id = packet.get("toId", "broadcast")

            # Save incoming message
            mesh_msg = MeshtasticMessage(
                mesh_id=packet.get("id", ""),
                mesh_from=from_id,
                mesh_to=to_id,
                channel=settings.MESHTASTIC_CHANNEL,
                message_type="query",
                payload={"query": query, "packet": packet},
                status="received",
                created_at=datetime.utcnow()
            )
            self.db.add(mesh_msg)
            self.db.commit()

            logger.info(f"📡 Meshtastic query from {from_id}: {query}")

            # Process will be handled by separate task
            return mesh_msg

        except Exception as e:
            logger.error(f"Error processing Meshtastic message: {e}")

    async def send_message(
        self,
        message: str,
        to_id: Optional[str] = None,
        channel: Optional[int] = None
    ) -> bool:
        """
        Send message via Meshtastic

        Args:
            message: Text message to send
            to_id: Recipient node ID (None for broadcast)
            channel: Channel number (uses default if None)

        Returns:
            bool: Success status
        """
        if not self.enabled or not self.connected:
            logger.warning("Meshtastic not enabled or not connected")
            return False

        try:
            # Compress message if too long
            if len(message) > 200:
                message = message[:197] + "..."

            # Send via interface
            self.interface.sendText(
                message,
                destinationId=to_id,
                channelIndex=channel or settings.MESHTASTIC_CHANNEL
            )

            # Log sent message
            mesh_msg = MeshtasticMessage(
                mesh_id="",  # Will be filled when confirmed
                mesh_from="self",
                mesh_to=to_id or "broadcast",
                channel=channel or settings.MESHTASTIC_CHANNEL,
                message_type="response",
                payload={"message": message},
                status="sent",
                created_at=datetime.utcnow()
            )
            self.db.add(mesh_msg)
            self.db.commit()

            logger.info(f"📡 Sent Meshtastic message to {to_id or 'broadcast'}")
            return True

        except Exception as e:
            logger.error(f"Error sending Meshtastic message: {e}")
            return False

    async def send_response(
        self,
        response: str,
        original_message: MeshtasticMessage
    ) -> bool:
        """
        Send response to a Meshtastic query

        Args:
            response: LUCA's response
            original_message: The original query message

        Returns:
            bool: Success status
        """
        # Format response for Meshtastic
        formatted = f"LUCA: {response}"

        # Send to original sender
        success = await self.send_message(
            message=formatted,
            to_id=original_message.mesh_from,
            channel=original_message.channel
        )

        if success:
            # Update original message status
            original_message.status = "processed"
            original_message.processed_at = datetime.utcnow()
            self.db.commit()

        return success

    def get_pending_messages(self) -> List[MeshtasticMessage]:
        """Get pending Meshtastic messages that need processing"""
        return self.db.query(MeshtasticMessage).filter(
            MeshtasticMessage.status == "received",
            MeshtasticMessage.message_type == "query"
        ).all()

    def get_node_info(self) -> Optional[Dict[str, Any]]:
        """Get information about connected Meshtastic node"""
        if not self.connected or not self.interface:
            return None

        try:
            node_info = self.interface.getMyNodeInfo()
            return {
                "node_id": node_info.get("user", {}).get("id", "unknown"),
                "long_name": node_info.get("user", {}).get("longName", "Unknown"),
                "short_name": node_info.get("user", {}).get("shortName", "UNK"),
                "connected": self.connected,
                "interface": settings.MESHTASTIC_INTERFACE
            }
        except Exception as e:
            logger.error(f"Error getting node info: {e}")
            return None

    def get_mesh_stats(self) -> Dict[str, Any]:
        """Get Meshtastic message statistics"""
        total = self.db.query(MeshtasticMessage).count()
        pending = self.db.query(MeshtasticMessage).filter(
            MeshtasticMessage.status == "received"
        ).count()
        processed = self.db.query(MeshtasticMessage).filter(
            MeshtasticMessage.status == "processed"
        ).count()
        failed = self.db.query(MeshtasticMessage).filter(
            MeshtasticMessage.status == "failed"
        ).count()

        return {
            "enabled": self.enabled,
            "connected": self.connected,
            "total_messages": total,
            "pending": pending,
            "processed": processed,
            "failed": failed,
            "node_info": self.get_node_info()
        }

    def close(self):
        """Close Meshtastic connection"""
        if self.interface:
            try:
                self.interface.close()
                logger.info("Meshtastic connection closed")
            except Exception as e:
                logger.error(f"Error closing Meshtastic: {e}")


# Meshtastic Setup Instructions
MESHTASTIC_SETUP_GUIDE = """
# 🌐 LUCA Meshtastic Integration Setup

## What is Meshtastic?
Meshtastic creates a long-range mesh network using inexpensive LoRa radios.
Perfect for areas without internet access or in censored regions.

## Hardware Needed
- Meshtastic compatible device (e.g., LILYGO T-Beam, Heltec LoRa32)
- USB cable or network connection
- Optional: Solar panel for off-grid operation

## Software Installation

1. **Install Meshtastic Python library:**
   ```bash
   pip install meshtastic
   ```

2. **Configure .env:**
   ```bash
   MESHTASTIC_ENABLED=True
   MESHTASTIC_INTERFACE=serial  # or tcp
   MESHTASTIC_PORT=/dev/ttyUSB0  # adjust for your device
   MESHTASTIC_CHANNEL=0
   ```

3. **Connect your device:**
   - Serial: Connect via USB
   - TCP: Ensure device is on network

4. **Test connection:**
   ```bash
   python -c "import meshtastic; meshtastic.serial_interface.SerialInterface()"
   ```

## Usage

### Sending Queries
Users with Meshtastic devices can query LUCA:
```
!luca What is 3+3?
!luca How do I purify water?
!luca Medical: treating burns
```

### Response Format
LUCA responds with compressed, essential information:
```
LUCA: 3+3=6. Tesla resonance detected! 369!
```

## Use Cases

### 🚨 Emergency Scenarios
- Disaster response coordination
- Medical information
- Resource location

### 🌍 Remote Areas
- Rural communities without internet
- Off-grid operations
- Maritime/aviation

### 🔒 Censored Regions
- Bypassing internet restrictions
- Secure mesh communication
- Gaza, Ukraine, etc.

## Security Notes
- Messages are public by default
- Use encryption for sensitive data
- Be aware of local regulations

## Range
- Urban: 1-3 km
- Rural: 5-10 km
- Line of sight: up to 20+ km
- With repeaters: much further

## Power Consumption
- Battery: 24-48 hours typical
- Solar: Indefinite operation
- Low power mode available

---

For more info: https://meshtastic.org
LUCA + Meshtastic = AI for everyone, everywhere! 🌐🧬
"""
