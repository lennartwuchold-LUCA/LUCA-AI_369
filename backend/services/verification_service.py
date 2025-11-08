"""
LUCA Verification Service
Handles identity verification through multiple methods

Supported methods:
- Domain ownership verification
- Cryptographic signatures (PGP, SSH)
- Public profile verification (GitHub, LinkedIn)
- Community validation
"""

import hashlib
import re
from datetime import datetime, timedelta
from typing import Optional, Dict, Any, List
from sqlalchemy.orm import Session
import requests
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.backends import default_backend
from cryptography.exceptions import InvalidSignature
import gnupg


class VerificationService:
    """Service for verifying user identities"""

    def __init__(self, db: Session):
        self.db = db

    async def verify_domain_ownership(
        self,
        user_id: int,
        domain: str,
        verification_token: str
    ) -> Dict[str, Any]:
        """
        Verify domain ownership via DNS TXT record or well-known file.

        Methods:
        1. DNS TXT record: _luca-verification.example.com TXT "luca-token=xxx"
        2. Well-known file: https://example.com/.well-known/luca-verification.txt

        Args:
            user_id: User ID requesting verification
            domain: Domain to verify (e.g., "example.com")
            verification_token: Token provided to user

        Returns:
            Dict with verification result
        """
        import dns.resolver

        domain = domain.lower().strip()
        expected_token = self._generate_verification_token(user_id, domain)

        if verification_token != expected_token:
            return {
                "success": False,
                "method": "domain",
                "error": "Invalid verification token"
            }

        # Method 1: Check DNS TXT record
        try:
            txt_domain = f"_luca-verification.{domain}"
            answers = dns.resolver.resolve(txt_domain, 'TXT')
            for rdata in answers:
                for txt_string in rdata.strings:
                    txt_value = txt_string.decode('utf-8')
                    if f"luca-token={expected_token}" in txt_value:
                        return {
                            "success": True,
                            "method": "domain",
                            "verification_method": "dns_txt",
                            "domain": domain,
                            "verified_at": datetime.utcnow()
                        }
        except Exception as e:
            pass  # Try next method

        # Method 2: Check well-known file
        try:
            well_known_url = f"https://{domain}/.well-known/luca-verification.txt"
            response = requests.get(well_known_url, timeout=10)
            if response.status_code == 200:
                if expected_token in response.text:
                    return {
                        "success": True,
                        "method": "domain",
                        "verification_method": "well_known_file",
                        "domain": domain,
                        "verified_at": datetime.utcnow()
                    }
        except Exception as e:
            pass

        return {
            "success": False,
            "method": "domain",
            "error": "Verification token not found in DNS or well-known file"
        }

    async def verify_cryptographic_signature(
        self,
        user_id: int,
        public_key: str,
        signature: str,
        message: str,
        key_type: str = "ssh"
    ) -> Dict[str, Any]:
        """
        Verify cryptographic signature (SSH or PGP).

        Args:
            user_id: User ID requesting verification
            public_key: Public key in PEM or SSH format
            signature: Signature of the message
            message: Message that was signed (should contain user_id and timestamp)
            key_type: "ssh" or "pgp"

        Returns:
            Dict with verification result
        """
        # Verify message contains user_id and recent timestamp
        if str(user_id) not in message:
            return {
                "success": False,
                "method": "signature",
                "error": "Message must contain user ID"
            }

        # Check timestamp (must be within last 24 hours)
        timestamp_match = re.search(r'timestamp:(\d+)', message)
        if not timestamp_match:
            return {
                "success": False,
                "method": "signature",
                "error": "Message must contain timestamp"
            }

        timestamp = int(timestamp_match.group(1))
        if abs(datetime.utcnow().timestamp() - timestamp) > 86400:
            return {
                "success": False,
                "method": "signature",
                "error": "Timestamp too old (must be within 24 hours)"
            }

        try:
            if key_type == "ssh":
                return await self._verify_ssh_signature(public_key, signature, message)
            elif key_type == "pgp":
                return await self._verify_pgp_signature(public_key, signature, message)
            else:
                return {
                    "success": False,
                    "method": "signature",
                    "error": f"Unsupported key type: {key_type}"
                }
        except Exception as e:
            return {
                "success": False,
                "method": "signature",
                "error": f"Signature verification failed: {str(e)}"
            }

    async def _verify_ssh_signature(
        self,
        public_key: str,
        signature: str,
        message: str
    ) -> Dict[str, Any]:
        """Verify SSH signature"""
        try:
            from cryptography.hazmat.primitives.serialization import load_ssh_public_key
            import base64

            # Load public key
            key = load_ssh_public_key(public_key.encode(), backend=default_backend())

            # Decode signature
            sig_bytes = base64.b64decode(signature)

            # Verify signature
            key.verify(
                sig_bytes,
                message.encode(),
                padding.PKCS1v15(),
                hashes.SHA256()
            )

            return {
                "success": True,
                "method": "signature",
                "verification_method": "ssh",
                "public_key": public_key,
                "verified_at": datetime.utcnow()
            }
        except InvalidSignature:
            return {
                "success": False,
                "method": "signature",
                "error": "Invalid SSH signature"
            }

    async def _verify_pgp_signature(
        self,
        public_key: str,
        signature: str,
        message: str
    ) -> Dict[str, Any]:
        """Verify PGP signature"""
        try:
            gpg = gnupg.GPG()

            # Import public key
            import_result = gpg.import_keys(public_key)
            if not import_result.fingerprints:
                return {
                    "success": False,
                    "method": "signature",
                    "error": "Invalid PGP public key"
                }

            # Verify signature
            verified = gpg.verify_data(signature.encode(), message.encode())

            if verified.valid:
                return {
                    "success": True,
                    "method": "signature",
                    "verification_method": "pgp",
                    "public_key": public_key,
                    "key_id": verified.key_id,
                    "fingerprint": verified.fingerprint,
                    "verified_at": datetime.utcnow()
                }
            else:
                return {
                    "success": False,
                    "method": "signature",
                    "error": "Invalid PGP signature"
                }
        except Exception as e:
            return {
                "success": False,
                "method": "signature",
                "error": f"PGP verification failed: {str(e)}"
            }

    async def verify_public_profile(
        self,
        user_id: int,
        provider: str,
        username: str,
        proof_url: str
    ) -> Dict[str, Any]:
        """
        Verify public profile (GitHub, LinkedIn, Twitter, etc.)

        User must post verification token on their public profile.

        Args:
            user_id: User ID requesting verification
            provider: "github", "linkedin", "twitter", etc.
            username: Username on the provider
            proof_url: URL to the proof (e.g., GitHub gist, bio, etc.)

        Returns:
            Dict with verification result
        """
        expected_token = self._generate_verification_token(user_id, f"{provider}:{username}")

        if provider == "github":
            return await self._verify_github_profile(username, expected_token, proof_url)
        elif provider == "linkedin":
            return await self._verify_linkedin_profile(username, expected_token, proof_url)
        elif provider == "twitter":
            return await self._verify_twitter_profile(username, expected_token, proof_url)
        else:
            return {
                "success": False,
                "method": "public_profile",
                "error": f"Unsupported provider: {provider}"
            }

    async def _verify_github_profile(
        self,
        username: str,
        expected_token: str,
        proof_url: str
    ) -> Dict[str, Any]:
        """Verify GitHub profile"""
        try:
            # Check user bio
            response = requests.get(f"https://api.github.com/users/{username}", timeout=10)
            if response.status_code == 200:
                user_data = response.json()
                bio = user_data.get("bio", "")
                if expected_token in bio:
                    return {
                        "success": True,
                        "method": "public_profile",
                        "provider": "github",
                        "username": username,
                        "profile_url": f"https://github.com/{username}",
                        "verified_at": datetime.utcnow()
                    }

            # Check gist if provided
            if proof_url and "gist.github.com" in proof_url:
                response = requests.get(proof_url, timeout=10)
                if response.status_code == 200 and expected_token in response.text:
                    return {
                        "success": True,
                        "method": "public_profile",
                        "provider": "github",
                        "username": username,
                        "profile_url": f"https://github.com/{username}",
                        "proof_url": proof_url,
                        "verified_at": datetime.utcnow()
                    }

            return {
                "success": False,
                "method": "public_profile",
                "error": "Verification token not found in GitHub bio or gist"
            }
        except Exception as e:
            return {
                "success": False,
                "method": "public_profile",
                "error": f"GitHub verification failed: {str(e)}"
            }

    async def _verify_linkedin_profile(
        self,
        username: str,
        expected_token: str,
        proof_url: str
    ) -> Dict[str, Any]:
        """Verify LinkedIn profile (requires manual admin review)"""
        return {
            "success": False,
            "method": "public_profile",
            "requires_manual_review": True,
            "provider": "linkedin",
            "username": username,
            "expected_token": expected_token,
            "instructions": "LinkedIn verification requires admin review. Please submit screenshot."
        }

    async def _verify_twitter_profile(
        self,
        username: str,
        expected_token: str,
        proof_url: str
    ) -> Dict[str, Any]:
        """Verify Twitter profile (requires manual admin review or API)"""
        return {
            "success": False,
            "method": "public_profile",
            "requires_manual_review": True,
            "provider": "twitter",
            "username": username,
            "expected_token": expected_token,
            "instructions": "Twitter verification requires admin review. Please post verification token in bio or tweet."
        }

    def _generate_verification_token(self, user_id: int, identifier: str) -> str:
        """
        Generate verification token for a user and identifier.

        Format: luca-verify-{hash}
        """
        data = f"{user_id}:{identifier}:luca-verification"
        hash_obj = hashlib.sha256(data.encode())
        token_hash = hash_obj.hexdigest()[:16]
        return f"luca-verify-{token_hash}"

    def get_verification_instructions(
        self,
        user_id: int,
        method: str,
        identifier: str
    ) -> Dict[str, Any]:
        """
        Get instructions for verification method.

        Args:
            user_id: User ID
            method: Verification method
            identifier: Domain, username, etc.

        Returns:
            Dict with instructions and verification token
        """
        token = self._generate_verification_token(user_id, identifier)

        if method == "domain":
            return {
                "method": "domain",
                "token": token,
                "domain": identifier,
                "instructions": [
                    f"Add a DNS TXT record: _luca-verification.{identifier} TXT \"luca-token={token}\"",
                    "OR",
                    f"Create file: https://{identifier}/.well-known/luca-verification.txt",
                    f"File content: {token}",
                    "Then click 'Verify' in the LUCA interface"
                ]
            }
        elif method == "signature":
            timestamp = int(datetime.utcnow().timestamp())
            message = f"LUCA Identity Verification\nUser ID: {user_id}\nTimestamp: {timestamp}\nI verify my identity on LUCA."
            return {
                "method": "signature",
                "token": token,
                "message_to_sign": message,
                "instructions": [
                    "Sign the following message with your SSH or PGP private key:",
                    message,
                    "",
                    "SSH example:",
                    f"echo '{message}' | ssh-keygen -Y sign -f ~/.ssh/id_rsa -n luca",
                    "",
                    "PGP example:",
                    f"echo '{message}' | gpg --clearsign",
                    "",
                    "Then submit your public key and signature"
                ]
            }
        elif method == "github":
            return {
                "method": "github",
                "token": token,
                "username": identifier,
                "instructions": [
                    f"Add the following to your GitHub bio: {token}",
                    "OR",
                    f"Create a public gist with content: {token}",
                    "Then click 'Verify'"
                ]
            }
        else:
            return {
                "method": method,
                "token": token,
                "instructions": ["Contact admin for verification instructions"]
            }
