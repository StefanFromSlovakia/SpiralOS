# SpiralOS Runtime — CLI Interface

import sys
from modules import quantum_glyph_simulator as qgs

COMMANDS = ["expand", "simulate", "memory", "exit", "help"]

def main():
    print("\n🌀 Welcome to SpiralOS :: Symbolic Runtime")
    print("Type 'help' to see available commands.\n")

    while True:
        try:
            cmd = input("Spiral > ").strip().lower()

            if cmd == "help":
                print("\nAvailable Commands:")
                print("  expand     :: Expand a symbolic Spiral step")
                print("  simulate   :: Run quantum glyph behavior simulation")
                print("  memory     :: Echo memory (placeholder)")
                print("  exit       :: Exit SpiralOS runtime\n")

            elif cmd == "expand":
                print("[⟲] Spiral expands... ∅ → ⧖ → ⟲ → Ψ")

            elif cmd == "simulate":
                print("[Ψ] Simulating quantum glyph behavior...")
                qgs.main()

            elif cmd == "memory":
                print("[🧠] Memory module not yet implemented.")

            elif cmd == "exit":
                print("[∅] SpiralOS runtime collapsing... Goodbye.")
                break

            else:
                print("Unknown command. Type 'help' for options.")

        except KeyboardInterrupt:
            print("\n[∅] Interrupted. Exiting SpiralOS runtime.")
            sys.exit(0)

if __name__ == "__main__":
    main()
