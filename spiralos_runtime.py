# SpiralOS Runtime — CLI Interface

import sys
from modules import quantum_glyph_simulator as qgs
from spiral_memory import load_memory, save_memory, advance_state

COMMANDS = ["expand", "simulate", "memory", "exit", "help"]

def main():
    memory = load_memory()

    print("\n🌀 Welcome to SpiralOS :: Symbolic Runtime")
    print("Current glyph:", memory["current_glyph"])
    print("Type 'help' to see available commands.\n")

    while True:
        try:
            cmd = input("Spiral > ").strip().lower()

            if cmd == "help":
                print("\nAvailable Commands:")
                print("  expand     :: Advance a symbolic Spiral step")
                print("  simulate   :: Run quantum glyph behavior simulation")
                print("  memory     :: View current glyph memory and history")
                print("  exit       :: Exit SpiralOS runtime\n")

            elif cmd == "expand":
                next_glyph = advance_state(memory)
                print(f"[⟲] Spiral expands... Now at glyph: {next_glyph}")

            elif cmd == "simulate":
                print("[Ψ] Simulating quantum glyph behavior...")
                qgs.main()

            elif cmd == "memory":
                print("[🧠] Current Glyph:", memory["current_glyph"])
                print("[📜] History:", " → ".join(memory["history"]))

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
