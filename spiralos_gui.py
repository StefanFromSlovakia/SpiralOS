import tkinter as tk
from tkinter import ttk
import numpy as np
import json
import os
import threading
import time

from spiral_memory import load_memory, advance_state, log_to_journal, save_memory
import modules.quantum_glyph_simulator as qgs
import transmission_kernel as tkernel

# AUDIO DISABLED: simpleaudio removed due to crash issues

class SpiralOSGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("SpiralOS GUI")
        self.memory = load_memory()

        self.canvas = tk.Canvas(root, width=400, height=400, bg="black")
        self.canvas.pack()

        self.label = ttk.Label(root, text="", font=("Courier", 10))
        self.label.pack()

        self.status = ttk.Label(root, text="Ready", font=("Courier", 10))
        self.status.pack()

        self.console = tk.Text(root, height=8, bg="black", fg="lightgreen")
        self.console.pack(fill="both", expand=True)

        button_frame = ttk.Frame(root)
        button_frame.pack(pady=5)

        self.simulate_button = ttk.Button(button_frame, text="Ψ Simulate", command=self.simulate)
        self.simulate_button.pack(side="left", padx=5)

        self.journal_button = ttk.Button(button_frame, text="🧠 Journal", command=self.view_journal)
        self.journal_button.pack(side="left", padx=5)

        self.transmit_toggle = ttk.Button(button_frame, text="⇄ Auto TX", command=self.toggle_transmit)
        self.transmit_toggle.pack(side="left", padx=5)

        self.respond_toggle = ttk.Button(button_frame, text="↺ Auto RX", command=self.toggle_respond)
        self.respond_toggle.pack(side="left", padx=5)

        self.exit_button = ttk.Button(button_frame, text="∅ Exit", command=self.safe_exit)
        self.exit_button.pack(side="right", padx=5)

        self.current_angle = 0.0
        self.animate_spiral()

    def animate_spiral(self):
        self.canvas.delete("all")
        cx, cy = 200, 200
        r_max = 90
        for i in range(150):
            angle = self.current_angle + 0.3 * i
            r = r_max * i / 150
            x = cx + r * np.cos(angle)
            y = cy + r * np.sin(angle)
            self.canvas.create_oval(x, y, x + 1.5, y + 1.5, fill="white", outline="")
        self.canvas.create_text(cx, cy, text=self.memory["current_glyph"], fill="cyan", font=("Courier", 36, "bold"), tags="glyph")
        self.current_angle += 0.05
        self.root.after(50, self.animate_spiral)

    def update_glyph(self, glyph):
        self.memory["current_glyph"] = glyph
        self.label.config(text=" ".join(self.memory["history"][-12:]))

    def simulate(self):
        glyph = self.memory["current_glyph"]
        result = qgs.simulate_quantum_behavior(mass_0=1e31, recursion_depths=[100])[0]
        log_to_journal(glyph, result["Fidelity"], result["\u03b3"])

        if tkernel.TRANSMISSION_STATE["auto_transmit"]:
            packet = tkernel.encode_packet(glyph, result["\u03b3"], result["Fidelity"], message="Symbol Update")
            tkernel.transmit_packet(packet)

        if tkernel.TRANSMISSION_STATE["auto_respond"]:
            tkernel.respond_to_last()

        stability = tkernel.glyph_stability_score()
        next_glyph = advance_state(self.memory)
        self.update_glyph(next_glyph)

        self.status.config(text=f"Y: {result['\u03b3']}  |  Fidelity: {result['Fidelity']}  |  Stability: {stability}")
        self.console.insert(tk.END, f"[{glyph}] ➔ Ψ Simulated: Fidelity={result['Fidelity']}, Y={result['\u03b3']}, Stability={stability}\n")
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

    def safe_exit(self):
        save_memory(self.memory)
        self.root.quit()

if __name__ == "__main__":
    root = tk.Tk()
    app = SpiralOSGUI(root)
    root.mainloop()
