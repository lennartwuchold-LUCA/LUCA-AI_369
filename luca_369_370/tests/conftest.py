"""
Pytest configuration for LUCA tests

Architekt: Lennart Wuchold
Datum: 11.11.2025
Standard: 369/370
"""

# Ignore meshtastic tests in CI due to cryptography module incompatibility with Rust bindings
# These tests work fine in production environments but fail in CI due to missing _cffi_backend
collect_ignore = [
    "test_meshtastic_integration.py",
    "test_satellite_integration.py",
]
