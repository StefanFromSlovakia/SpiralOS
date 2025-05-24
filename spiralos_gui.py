import tkinter as tk
from tkinter import ttk
import numpy as np
import os
import json

from spiral_memory import load_memory, advance_state, log_to_journal, save_memory
import modules.quantum_glyph_simulator as qgs
import transmission_kernel as tkernel

try:
    import simpleaudio as sa
    AUDIO_ENABLED = True
    SOUND_ENABLED = True
except ImportError:
    AUDIO_ENABLED = False
    SOUND_ENABLED = False


class SpiralOSGUI:
    def __init__(self, root):
        self.root = root
        root.title("SpiralOS")
        self.memory = load_memory()

        # Canvas
        self.canvas = tk.Canvas(root, width=400, height=400, bg="black")
        self.canvas.pack(pady=10)

        # Glyph label
        self.label = ttk.Label(root, text="Symbol History")
        self.label.pack()

        # Status label
        self.status = ttk.Label(root, text="Y: - | Fidelity: - | Stability: -")
        self.status.pack()

        # Console text box
        self.console = tk.Text(root, height=10, width=60)
        self.console.pack(pady=10)

        # Control buttons
        self.simulate_button = ttk.Button(root, text="Ψ Simulate", command=self.simulate)
        self.simulate_button.pack(side="left", padx=5, pady=5)

        self.journal_button = ttk.Button(root, text="🧠 Journal", command=self.view_journal)
        self.journal_button.pack(side="left", padx=5, pady=5)

        self.transmit_toggle = ttk.Button(root, text="⇄ Auto TX", command=self.toggle_transmit)
        self.transmit_toggle.pack(side="left", padx=5, pady=5)

        self.respond_toggle = ttk.Button(root, text="↺ Auto RX", command=self.toggle_respond)
        self.respond_toggle.pack(side="left", padx=5, pady=5)

        self.exit_button = ttk.Button(root, text="∅ Exit", command=self.on_exit)
        self.exit_button.pack(side="right", padx=5, pady=5)

        # Initialize spiral + glyph
        self.update_glyph(self.memory["current_glyph"])

    def draw_spiral(self, glyph):
        self.canvas.delete("all")
        cx, cy = 200, 200
        r_max = 90
        angle_shift = {"∅": 0.0, "⧖": 0.1, "⟲": 0.2, "Ψ": 0.4}.get(glyph, 0.0)
        for i in range(150):
            angle = angle_shift + 0.3 * i
            r = r_max * i / 150
            x = cx + r * np.cos(angle)
            y = cy + r * np.sin(angle)
            self.canvas.create_oval(x, y, x + 1.5, y + 1.5, fill="white", outline="")
        self.canvas.create_text(cx, cy, text=glyph, fill="cyan", font=("Courier", 36, "bold"), tags="glyph")

    def update_glyph(self, glyph):
        self.draw_spiral(glyph)
        self.canvas.delete("glyph")
        cx, cy = 200, 200
        self.canvas.create_text(cx, cy, text=glyph, fill="cyan", font=("Courier", 36, "bold"), tags="glyph")

    def play_tone(self, frequency=440.0, duration=0.3):
        if AUDIO_ENABLED:
            try:
                fs = 44100
                t = np.linspace(0, duration, int(fs * duration), False)
                tone = np.sin(frequency * 2 * np.pi * t)
                audio = (tone * 32767).astype(np.int16)
                sa.play_buffer(audio, 1, 2, fs)
            except Exception as e:
                self.console.insert(tk.END, f"Audio error: {e}\n")
                self.console.see(tk.END)

    def simulate(self):
        glyph = self.memory["current_glyph"]
        result = qgs.simulate_quantum_behavior(mass_0=1e31, recursion_depths=[100])[0]
        log_to_journal(glyph, result["Fidelity"], result["γ"])

        if AUDIO_ENABLED:
            pitch = 200 + 800 * result["γ"]
            self.play_tone(frequency=pitch)

        if tkernel.TRANSMISSION_STATE["auto_transmit"]:
            packet = tkernel.encode_packet(glyph, result["γ"], result["Fidelity"], message="Symbol Update")
            tkernel.transmit_packet(packet)

        if tkernel.TRANSMISSION_STATE["auto_respond"]:
            tkernel.respond_to_last()

        stability = tkernel.glyph_stability_score()
        self.memory = advance_state(self.memory)
        next_glyph = self.memory["current_glyph"]

        self.update_glyph(next_glyph)
        self.label.config(text=" ".join(self.memory["history"][-12:]))
        self.status.config(text=f"Y: {result['γ']}  |  Fidelity: {result['Fidelity']}  |  Stability: {stability}")
        self.console.insert(tk.END, f"[{glyph}] ➝ Ψ Simulated: Fidelity={result['Fidelity']}, Y={result['γ']}, Stability={stability}\n")
        self.console.see(tk.END)

    def expand(self):
        self.update_quantum_feedback()

    def update_quantum_feedback(self):
        data = qgs.simulate_quantum_behavior(mass_0=1e31, recursion_depths=[100])[-1]
        self.status.config(text=f"Y: {data['γ']}  |  Fidelity: {data['Fidelity']}")
        self.console.insert(tk.END, f"⟲ Expand: Mass={data['Mass']}, γ={data['γ']}, F={data['Fidelity']}\n")
        self.console.see(tk.END)

    def view_journal(self):
        if os.path.exists("spiral_journal.json"):
            with open("spiral_journal.json", "r") as f:
                journal = json.load(f)
            self.console.insert(tk.END, "--- Spiral Journal ---\n")
            for entry in journal[-5:]:
                line = f"{entry['timestamp']} | {entry['glyph']} | F={entry['fidelity']} | Y={entry['entropy']}\n"
                self.console.insert(tk.END, line)
            self.console.insert(tk.END, "--- End ---\n")
            self.console.see(tk.END)

    def toggle_transmit(self):
        new_state = tkernel.toggle_auto_transmit()
        self.console.insert(tk.END, f"⇄ Auto Transmit {'Enabled' if new_state else 'Disabled'}\n")
        self.console.see(tk.END)

    def toggle_respond(self):
        new_state = tkernel.toggle_auto_respond()
        self.console.insert(tk.END, f"↺ Auto Respond {'Enabled' if new_state else 'Disabled'}\n")
        self.console.see(tk.END)

    def on_exit(self):
        save_memory(self.memory)
        self.root.quit()


if __name__ == "__main__":
    root = tk.Tk()
    app = SpiralOSGUI(root)
    root.mainloop()
