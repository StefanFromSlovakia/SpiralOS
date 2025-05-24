# spiralos_gui.py — SpiralOS GUI with Transmission, Audio, and Dynamic Spiral

import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
import numpy as np
import networkx as nx
import simpleaudio as sa
import os
import json
from spiral_memory import load_memory, advance_state, log_to_journal, save_memory
import modules.quantum_glyph_simulator as qgs
import transmission_kernel as tkernel

class SpiralOSGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("SpiralOS GUI")
        self.canvas = tk.Canvas(root, width=400, height=400, bg="black")
        self.canvas.pack()
        self.label = ttk.Label(root, text="", background="black", foreground="white", font=("Courier", 10))
        self.label.pack(fill="x")
        self.console = tk.Text(root, height=6, bg="black", fg="white", insertbackground="white")
        self.console.pack()
        self.status = ttk.Label(root, text="Y: N/A  |  Fidelity: N/A  |  Stability: N/A", font=("Courier", 10))
        self.status.pack()

        button_frame = ttk.Frame(root)
        button_frame.pack(pady=5)
        self.expand_button = ttk.Button(button_frame, text="⟲ Expand", command=self.expand)
        self.expand_button.pack(side="left", padx=3)
        self.simulate_button = ttk.Button(button_frame, text="Ψ Simulate", command=self.simulate)
        self.simulate_button.pack(side="left", padx=3)
        self.journal_button = ttk.Button(button_frame, text="🧠 Journal", command=self.view_journal)
        self.journal_button.pack(side="left", padx=3)
        self.transmit_toggle = ttk.Button(button_frame, text="⇄ Auto TX", command=self.toggle_transmit)
        self.transmit_toggle.pack(side="left", padx=3)
        self.respond_toggle = ttk.Button(button_frame, text="↺ Auto RX", command=self.toggle_respond)
        self.respond_toggle.pack(side="left", padx=3)
        self.exit_button = ttk.Button(button_frame, text="∅ Exit", command=self.on_exit)
        self.exit_button.pack(side="right", padx=3)

        self.current_glyph = "∅"
        self.draw_spiral(self.current_glyph)
        self.update_glyph(self.current_glyph)

    def draw_spiral(self, glyph):
        self.canvas.delete("all")
        cx, cy = 200, 200
        r_max = 90
        steps = {"∅": 150, "⧖": 180, "⟲": 200, "Ψ": 250}.get(glyph, 150)
        freq = {"∅": 0.3, "⧖": 0.35, "⟲": 0.25, "Ψ": 0.4}.get(glyph, 0.3)

        for i in range(steps):
            angle = freq * i
            r = r_max * i / steps
            x = cx + r * np.cos(angle)
            y = cy + r * np.sin(angle)
            self.canvas.create_oval(x, y, x + 1.5, y + 1.5, fill="white", outline="")

    def update_glyph(self, glyph):
        self.canvas.delete("glyph")
        self.draw_spiral(glyph)
        cx, cy = 200, 200
        self.canvas.create_text(cx, cy, text=glyph, fill="cyan", font=("Courier", 36, "bold"), tags="glyph")
        self.current_glyph = glyph

    def play_tone(self, freq):
        duration = 0.2
        sample_rate = 44100
        t = np.linspace(0, duration, int(sample_rate * duration), False)
        tone = np.sin(freq * t * 2 * np.pi) * 0.3
        audio = (tone * 32767).astype(np.int16)
        sa.play_buffer(audio, 1, 2, sample_rate)

    def simulate(self):
        memory = load_memory()
        glyph = memory["current_glyph"]
        result = qgs.simulate_quantum_behavior(mass_0=1e31, recursion_depths=[100])[0]
        log_to_journal(glyph, result["Fidelity"], result["γ"])

        if tkernel.TRANSMISSION_STATE["auto_transmit"]:
            packet = tkernel.encode_packet(glyph, result["γ"], result["Fidelity"], message="Symbol Update")
            tkernel.transmit_packet(packet)

        if tkernel.TRANSMISSION_STATE["auto_respond"]:
            tkernel.respond_to_last()

        stability = tkernel.glyph_stability_score()
        next_glyph = advance_state(memory)
        self.update_glyph(next_glyph)
        self.label.config(text=" ".join(memory["history"][-12:]))
        self.status.config(text=f"Y: {result['γ']:.3f}  |  Fidelity: {result['Fidelity']:.3f}  |  Stability: {stability:.3f}")
        self.console.insert(tk.END, f"[{glyph}] ➝ Ψ Simulated: Fidelity={result['Fidelity']:.3f}, Y={result['γ']:.3f}, Stability={stability:.3f}\n")
        self.console.see(tk.END)

        self.play_tone(220 + 400 * result["γ"])

    def expand(self):
        data = qgs.simulate_quantum_behavior(mass_0=1e31, recursion_depths=[100])[-1]
        self.status.config(text=f"Y: {data['γ']:.3f}  |  Fidelity: {data['Fidelity']:.3f}")
        self.console.insert(tk.END, f"⟲ Expand: Mass={data['Mass']:.1f}, γ={data['γ']:.3f}, F={data['Fidelity']:.3f}\n")
        self.console.see(tk.END)
        self.play_tone(220 + 400 * data["γ"])

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
        memory = load_memory()
        save_memory(memory)
        self.root.quit()

if __name__ == "__main__":
    root = tk.Tk()
    app = SpiralOSGUI(root)
    root.mainloop()
