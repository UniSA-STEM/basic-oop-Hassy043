"""
File: Hacker.py
Description: Defines the Hacker class for the "Into the Grid" simulation.
             A Hacker represents a player character operating within a dystopian digital underworld.
             Each Hacker manages a personal inventory, a Rig, and a trace level that increases during
             risky actions such as launching attacks or extracting assets. Hackers can acquire and
             upgrade Rigs, launch data spikes at opponents, extract assets from broken Rigs, and
             encrypt or decrypt digital assets using Security Chips. They can also manage storage
             transfers between their inventory and Rig, and reduce their trace level to avoid exposure.
             This class integrates closely with Rig and Asset to demonstrate object-oriented concepts
             such as encapsulation, inheritance, and interaction between multiple classes.
Author: Seyedvahid Hashemian
ID:  110426111
Username: Hassy043
This is my own work as defined by the University's Academic Misconduct Policy.
"""

# Hacker.py

from typing import List, Optional
from Asset import Asset
from Rig import Rig


class Hacker:
    """
    Represents a hacker with:
      - name (string)
      - inventory (starts with 1 CryptoToken)
      - rig (initially None; must acquire using 1 CryptoToken)
      - trace_level (starts at 0; risky actions increase; >5 blocks certain actions)
    """

    TRACE_BLOCK_THRESHOLD = 5

    def __init__(self, name: str):
        self.name = name
        self.inventory: List[Asset] = [Asset.crypto_token()]
        self.rig: Optional[Rig] = None
        self.trace_level: int = 0

    # ---------- Utility ----------

    def has_asset(self, name: str) -> bool:
        return any(a.name.lower() == name.lower() for a in self.inventory)

    def take_first(self, name: str) -> Optional[Asset]:
        """
        Find (case-insensitive) and remove the first matching asset from inventory.
        """
        for i, a in enumerate(self.inventory):
            if a.name.lower() == name.lower():
                return self.inventory.pop(i)
        return None

    # ---------- Rig lifecycle ----------

    def acquire_rig(self, rig: Optional[Rig] = None) -> bool:
        """
        Costs 1 CryptoToken. Accepts an existing rig or instantiates a basic one.
        """
        if self.rig is not None:
            print(f"{self.name} already has a rig.")
            return False
        token = self.take_first("CryptoToken")
        if not token:
            print(f"{self.name} needs a CryptoToken to acquire a rig.")
            return False
        self.rig = rig if rig else Rig(name=f"{self.name}'s Rig")
        print(f"{self.name} activated rig: {self.rig.name}")
        return True

    def upgrade_rig(self) -> bool:
        """
        Requires a rig and a Hardware Patch in inventory.
        """
        if not self.rig:
            print("Upgrade failed: no rig.")
            return False
        patch = self.take_first("Hardware Patch")
        if not patch:
            print("Upgrade failed: need a Hardware Patch.")
            return False
        return self.rig.upgrade(patch)

    # ---------- Security / Trace ----------

    def _check_trace_blocked(self) -> bool:
        if self.trace_level > self.TRACE_BLOCK_THRESHOLD:
            print(f"{self.name} is exposed (trace {self.trace_level}). Action blocked.")
            return True
        return False

    def cool_down(self, amount: int = 2) -> None:
        """
        Reduces trace level.
        """
        self.trace_level = max(0, self.trace_level - amount)
        print(f"{self.name} cooled down. Trace now {self.trace_level}.")

    def encrypt_asset(self, where: str, name: str) -> bool:
        """
        Encrypts an asset in 'inventory' or 'rig' storage.
        Requires a Security Chip.
        """
        chip = self.take_first("Security Chip")
        if not chip:
            print("Encryption failed: need a Security Chip.")
            return False

        asset = self._locate_asset(where, name)
        if not asset:
            print("Encryption failed: asset not found.")
            self.inventory.append(chip)  # return chip if nothing encrypted
            return False

        if asset.encrypted:
            print("Encryption failed: asset already encrypted.")
            self.inventory.append(chip)
            return False

        asset.encrypted = True
        print(f"{self.name} encrypted {asset.name}.")
        return True

    def decrypt_asset(self, where: str, name: str) -> bool:
        """
        Decrypts an asset in 'inventory' or 'rig' storage.
        Requires a Security Chip.
        """
        chip = self.take_first("Security Chip")
        if not chip:
            print("Decryption failed: need a Security Chip.")
            return False

        asset = self._locate_asset(where, name)
        if not asset:
            print("Decryption failed: asset not found.")
            self.inventory.append(chip)
            return False

        if not asset.encrypted:
            print("Decryption failed: asset is not encrypted.")
            self.inventory.append(chip)
            return False

        asset.encrypted = False
        print(f"{self.name} decrypted {asset.name}.")
        return True

    def _locate_asset(self, where: str, name: str) -> Optional[Asset]:
        target_name = name.lower()
        if where.lower() == "inventory":
            for a in self.inventory:
                if a.name.lower() == target_name:
                    return a
        elif where.lower() == "rig":
            if not self.rig:
                return None
            for a in self.rig.storage:
                if a.name.lower() == target_name:
                    return a
        return None

    # ---------- Transfers ----------

    def store_to_rig(self, name: Optional[str] = None, all_items: bool = False) -> None:
        """
        Move assets from hacker inventory to rig storage.
        """
        if not self.rig:
            print("Store failed: no rig.")
            return
        if all_items:
            moving = [a for a in self.inventory if not a.encrypted]
        elif name:
            found = next((a for a in self.inventory if a.name.lower() == name.lower() and not a.encrypted), None)
            moving = [found] if found else []
        else:
            print("Store failed: provide a name or all_items=True.")
            return

        for a in list(moving):
            if a and self.rig.store(a):
                self.inventory.remove(a)

    def retrieve_from_rig(self, name: Optional[str] = None, all_items: bool = False) -> None:
        """
        Move assets from rig storage to hacker inventory.
        """
        if not self.rig:
            print("Retrieve failed: no rig.")
            return
        released = self.rig.release(name=name, all_items=all_items)
        if not released and not all_items and name:
            print(f"No transferable '{name}' found in rig.")
        self.inventory.extend(released)

    def scan_and_take(self, name: str) -> Optional[Asset]:
        """
        Returns and removes the first named asset from inventory.
        """
        asset = self.take_first(name)
        if asset:
            print(f"{self.name} retrieved {asset.name} from inventory.")
        else:
            print(f"{name} not found in inventory.")
        return asset

    # ---------- Combat / Extraction ----------

    def launch_data_spike(self, target: "Hacker") -> bool:
        """
        Consumes a Data Spike from own rig storage and damages target's rig.
        Increases trace.
        """
        if self._check_trace_blocked():
            return False
        if not self.rig:
            print("Attack failed: no rig.")
            return False

        # Consume a Data Spike from own rig
        spikes = self.rig.release(name="Data Spike")
        if not spikes:
            print("Attack failed: no Data Spike available.")
            return False

        # Perform the hit
        if not target.rig:
            print("Attack: target has no rig; nothing to damage.")
        else:
            target.rig.take_hit()
            state = " (broken!)" if target.rig.broken else ""
            print(f"{self.name} hit {target.name}'s {target.rig.name}.{state}")

        # Risky action → raise trace
        self.trace_level += 1
        return True

    def extract_from_broken_rig(self, target: "Hacker") -> bool:
        """
        If target's rig is broken, consume a Removable Drive from your rig storage
        and transfer all NON-encrypted items from target rig to your inventory.
        Raises trace.
        """
        if self._check_trace_blocked():
            return False
        if not self.rig:
            print("Extraction failed: no rig.")
            return False
        if not target.rig or not target.rig.broken:
            print("Extraction failed: target rig is not broken.")
            return False

        drive = self.rig.release(name="Removable Drive")
        if not drive:
            print("Extraction failed: need a Removable Drive.")
            return False

        loot = target.rig.release(all_items=True)
        if loot:
            self.inventory.extend(loot)
            print(f"{self.name} extracted {len(loot)} asset(s) from {target.name}'s broken rig.")
        else:
            print("Extraction found no unsecured assets.")

        self.trace_level += 1
        return True

    # ---------- Presentation ----------

    def __str__(self) -> str:
        inv = ", ".join(a.name + ("[E]" if a.encrypted else "") for a in self.inventory) or "—"
        rig_name = self.rig.name if self.rig else "None"
        return f"Hacker: {self.name} | Rig: {rig_name} | Trace: {self.trace_level} | Inventory: {inv}"

