"""
File: Main.py
Description: Provides the main testing and demonstration script for the "Into the Grid" simulation.
             Imports the Hacker, Rig, and Asset classes and runs scenarios to verify functionality:
             rig acquisition, encryption/decryption, combat, rig damage/repair, upgrades, and trace management.
Author: Seyedvahid Hashemian
ID:  110426111
Username: Hassy043
This is my own work as defined by the University's Academic Misconduct Policy.
"""


from Asset import Asset
from Rig import Rig
from Hacker import Hacker


def scenario_basics():
    print("\n=== Scenario: Basics (acquire rig, store/retrieve, upgrade) ===")
    alice = Hacker("CipherAlice")
    print(alice)

    alice.acquire_rig()
    print(alice.rig)

    alice.rig.generate_asset(Asset.security_chip())
    alice.rig.generate_asset(Asset.hardware_patch())
    print(alice.rig)

    alice.retrieve_from_rig(name="Hardware Patch")
    print(alice)
    alice.upgrade_rig()
    print(alice.rig)

    alice.store_to_rig(all_items=True)
    print(alice)
    print(alice.rig)


def scenario_security_and_transfer():
    print("\n=== Scenario: Security & Transfer (encrypt/decrypt) ===")
    bob = Hacker("ShadowBob")
    bob.acquire_rig(Rig("Obsidian"))
    bob.inventory.append(Asset("Prototype Keys", "High-value credentials"))
    bob.inventory.append(Asset.security_chip())
    bob.inventory.append(Asset.security_chip())

    print(bob)
    bob.encrypt_asset(where="inventory", name="Prototype Keys")
    print(bob)

    bob.store_to_rig(name="Prototype Keys")  # should fail (encrypted)
    print(bob)
    print(bob.rig)

    bob.decrypt_asset(where="inventory", name="Prototype Keys")
    bob.store_to_rig(name="Prototype Keys")
    print(bob.rig)


def scenario_battle_and_extraction():
    print("\n=== Scenario: Battle & Extraction (trace, break, extract) ===")
    eve = Hacker("NullEve")
    eve.acquire_rig(Rig("Noir"))

    mallory = Hacker("Mallory")
    mallory.inventory.append(Asset.hardware_patch())
    mallory.acquire_rig(Rig("Raptor"))
    mallory.upgrade_rig()  # Level 1

    eve.launch_data_spike(mallory)
    eve.launch_data_spike(mallory)
    print(mallory.rig)

    eve.launch_data_spike(mallory)  # likely breaks mallory rig (threshold 3)
    print(mallory.rig)
    print(f"Eve trace: {eve.trace_level}")

    eve.extract_from_broken_rig(mallory)
    print(eve)
    print(mallory.rig)

    eve.trace_level = 6
    eve.launch_data_spike(mallory)  # blocked
    eve.cool_down()
    eve.launch_data_spike(mallory)  # allowed if <=5


def scenario_repairs_and_edge_cases():
    print("\n=== Scenario: Repairs & Edge Cases ===")
    trent = Hacker("Trent")
    trent.acquire_rig(Rig("Mamba"))

    trent.upgrade_rig()  # no patch
    trent.inventory.append(Asset.crypto_token())
    trent.rig.repair(trent.take_first("CryptoToken"))  # no repair needed

    trent.rig.take_hit()
    trent.rig.take_hit()
    print(trent.rig)
    trent.inventory.append(Asset.crypto_token())
    trent.rig.repair(trent.take_first("CryptoToken"))
    print(trent.rig)

    trent.inventory.append(Asset("Map Cache", "Coordinates"))
    trent.encrypt_asset("inventory", "Map Cache")  # fail (no chip)
    trent.inventory.append(Asset.security_chip())
    trent.encrypt_asset("inventory", "Map Cache")
    trent.decrypt_asset("inventory", "Map Cache")


def main():
    scenario_basics()
    scenario_security_and_transfer()
    scenario_battle_and_extraction()
    scenario_repairs_and_edge_cases()


if __name__ == "__main__":
    main()
