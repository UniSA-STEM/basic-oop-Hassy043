"""
File: Asset.py
Description: Defines the Asset class used to represent digital assets in the "Into the Grid" simulation.
             Each Asset has a name, description, and encryption state. Assets are used by hackers and rigs
             for actions such as encryption, upgrades, battles, and repairs in the object-oriented program.
Author: Seyedvahid Hashemian
ID:  110426111
Username: Hassy043
This is my own work as defined by the University's Academic Misconduct Policy.
"""

from dataclasses import dataclass


@dataclass
class Asset:
    """
    Represents a digital asset.
    - name: short identifier, e.g., "CryptoToken"
    - description: human-readable description
    - encrypted: True if protected; cannot be moved or used until decrypted
    """
    name: str
    description: str
    encrypted: bool = False

    def __str__(self) -> str:
        base = f"{self.name}: {self.description}"
        return f"{base} [Encrypted]" if self.encrypted else base

    # Helper factories (optional quality-of-life)
    @staticmethod
    def crypto_token() -> "Asset":
        return Asset("CryptoToken", "Used to get/repair rigs")

    @staticmethod
    def data_spike() -> "Asset":
        return Asset("Data Spike", "Offensive payload for rig battles")

    @staticmethod
    def removable_drive() -> "Asset":
        return Asset("Removable Drive", "Needed to extract from broken rigs")

    @staticmethod
    def security_chip() -> "Asset":
        return Asset("Security Chip", "Encrypts/Decrypts assets")

    @staticmethod
    def hardware_patch() -> "Asset":
        return Asset("Hardware Patch", "Upgrades rigs")

