"""
File: Rig.py
Description: Defines the Rig class used in the "Into the Grid" simulation.
             A Rig represents the hacker's computer system within the digital underworld.
             It manages assets such as Data Spikes, Removable Drives, and generated items.
             Each Rig can take damage, be upgraded, repaired, or broken.
             Its upgrade level influences storage capacity, durability, and combat effectiveness.
             The Rig interacts closely with the Hacker and Asset classes to simulate battles,
             repairs, upgrades, and storage operations as part of the object-oriented program.
Author: Seyedvahid Hashemian
ID:  110426111
Username: Hassy043
This is my own work as defined by the University's Academic Misconduct Policy.
"""

# Rig.py
from typing import List, Optional
from Asset import Asset


class Rig:
    """
    Represents a cyber rig.
    Starts with:
      - damage = 0
      - broken = False
      - upgrade_level = 0
      - storage = [2 x Data Spike, 1 x Removable Drive]
    """

    def __init__(self, name: str):
        self.name = name
        self.damage: float = 0.0
        self.broken: bool = False
        self.upgrade_level: int = 0
        self.storage: List[Asset] = [
            Asset.data_spike(),
            Asset.data_spike(),
            Asset.removable_drive(),
        ]

    # ---------- Core mechanics ----------

    @property
    def storage_capacity(self) -> int:
        """
        Capacity increases with upgrades.
        Base 5 + 2 per upgrade.
        """
        return 5 + 2 * self.upgrade_level

    @property
    def break_threshold(self) -> int:
        """
        Level 0 breaks at 2 damage.
        Each upgrade adds +1 tolerance (spec: upgrades reduce battle damage).
        This is a simple, transparent model.
        """
        return 2 + self.upgrade_level

    def condition_text(self) -> str:
        state = "Broken" if self.broken else "Pristine" if self.damage == 0 else "Damaged"
        return f"{state} (Level {self.upgrade_level})"

    def take_hit(self) -> None:
        """
        Increase damage by 1 (you could model mitigation here if desired).
        Break the rig if threshold reached.
        """
        if self.broken:
            return
        self.damage += 1
        if self.damage >= self.break_threshold:
            self.broken = True

    def repair(self, token: Optional[Asset]) -> bool:
        """
        Repairs the rig using a CryptoToken.
        Returns True if repaired.
        """
        if not token or token.name != "CryptoToken":
            print("Repair failed: A CryptoToken is required.")
            return False

        if self.damage == 0 and not self.broken:
            print("No repair needed.")
            return False

        self.damage = 0
        self.broken = False
        print(f"{self.name} repaired to pristine condition.")
        return True

    def upgrade(self, patch: Optional[Asset]) -> bool:
        """
        Upgrades rig using a Hardware Patch.
        """
        if not patch or patch.name != "Hardware Patch":
            print("Upgrade failed: A Hardware Patch is required.")
            return False
        self.upgrade_level += 1
        print(f"{self.name} upgraded to Level {self.upgrade_level}.")
        return True

    # ---------- Storage operations ----------

    def can_store(self, asset: Asset) -> bool:
        return len(self.storage) < self.storage_capacity

    def store(self, asset: Asset) -> bool:
        if asset.encrypted:
            print("Cannot store: asset is encrypted (must stay with owner).")
            return False
        if not self.can_store(asset):
            print("Rig storage is full.")
            return False
        self.storage.append(asset)
        return True

    def release(self, name: Optional[str] = None, all_items: bool = False) -> List[Asset]:
        """
        Release assets from rig storage.
        - If encrypted, cannot be released.
        - If name provided, release first match.
        - If all_items True, release all non-encrypted assets.
        """
        released: List[Asset] = []
        if all_items:
            keep: List[Asset] = []
            for a in self.storage:
                if a.encrypted:
                    keep.append(a)
                else:
                    released.append(a)
            self.storage = keep
            return released

        if name:
            for i, a in enumerate(self.storage):
                if (a.name.lower() == name.lower()) and not a.encrypted:
                    released.append(self.storage.pop(i))
                    break
        return released

    def generate_asset(self, asset: Asset) -> bool:
        """
        Adds an externally generated asset.
        """
        if not self.can_store(asset):
            print("Rig storage is full; cannot generate asset.")
            return False
        self.storage.append(asset)
        return True

    def __str__(self) -> str:
        stored = ", ".join(a.name + ("[E]" if a.encrypted else "") for a in self.storage) or "—"
        return f"Rig: {self.name} | {self.condition_text()} | Capacity {len(self.storage)}/{self.storage_capacity} | Stored: {stored}"

