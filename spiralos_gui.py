# spiralos_gui.py — SpiralOS GUI with Transmission Integration + Enhanced Styling

import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
import numpy as np
import networkx as nx
from spiral_memory import load_memory, advance_state, log_to_journal
import modules.quantum_glyph_simulator as qgs
import transmission_kernel as tkernel

class SpiralOSGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("SpiralOS GUI")

        style = ttk.Style()
        style.theme_use("clam")
        style.configure("TButton", font=("Courier", 10), padding=6)
        style.configure("TLabel", background="black", foreground="white")

        self.canvas = tk.Canvas(root, width=400, height=400, bg="black", highlightthickness=0)
        self.canvas.pack()

        self.label = ttk.Label(root, text="", font=("Courier", 10))
        self.label.pack(fill="x")

        self.console = tk.Text(root, height=5, bg="black", fg="white", insertbackground="white")
        self.console.tag_config("glyph", foreground="cyan")
        self.console.tag_config("transmit", foreground="magenta")
        self.console.tag_config("system", foreground="yellow")
        self.console.pack(fill="both", expand=True)

        self.status = ttk.Label(root, text="Y: N/A  |  Fidelity: N/A", font=("Courier", 10))
        self.status.pack(fill="x")

        button_frame = ttk.Frame(root)
        button_frame.pack(pady=5)

        self.expand_button = ttk.Button(button_frame, text="⟲ Expand", command=self.expand)
        self.expand_button.grid(row=0, column=0, padx=5)

        self.simulate_button = ttk.Button(button_frame, text="Ψ Simulate", command=self.simulate)
        self.simulate_button.grid(row=0, column=1, padx=5)

        self.journal_button = ttk.Button(button_frame, text="🧠 Journal", command=self.view_journal)
        self.journal_button.grid(row=0, column=2, padx=5)

        self.transmit_toggle = ttk.Button(button_frame, text="⇄ Auto TX", command=self.toggle_transmit)
        self.transmit_toggle.grid(row=0, column=3, padx=5)

        self.respond_toggle = ttk.Button(button_frame, text="↺ Auto RX", command=self.toggle_respond)
        self.respond_toggle.grid(row=0, column=4, padx=5)

        self.exit_button = ttk.Button(button_frame, text="∅ Exit", command=self.root.quit)
        self.exit_button.grid(row=0, column=5, padx=5)

        self.draw_spiral()
        self.update_glyph("∅")

    def draw_spiral(self):
        self.canvas.delete("all")
        cx, cy = 200, 200
        r_max = 90
        for i in range(150):
            angle = 0.3 * i
            r = r_max * i / 150
            x = cx + r * np.cos(angle)
            y = cy + r * np.sin(angle)
            self.canvas.create_oval(x, y, x + 1.5, y + 1.5, fill="white", outline="")

    def update_glyph(self, glyph):
        self.canvas.delete("glyph")
        cx, cy = 200, 200
        self.canvas.create_text(cx, cy, text=glyph, fill="cyan", font=("Courier", 36, "bold"), tags="glyph")

    def simulate(self):
        memory = load_memory()
        glyph = memory["current_glyph"]
        result = qgs.simulate_quantum_behavior(mass_0=1e31, recursion_depths=[100])[0]
        log_to_journal(glyph, result["Fidelity"], result["γ"])

        if tkernel.TRANSMISSION_STATE["auto_transmit"]:
            packet = tkernel.encode_packet(glyph, result["γ"], result["Fidelity"], message="Symbol Update")
            tkernel.transmit_packet(packet)
            self.console.insert(tk.END, f"⇄ Transmit: {packet}\n", "transmit")

        if tkernel.TRANSMISSION_STATE["auto_respond"]:
            tkernel.respond_to_last()
            self.console.insert(tk.END, "↺ Response generated\n", "system")

        stability = tkernel.glyph_stability_score()
        next_glyph = advance_state(memory)
        self.update_glyph(next_glyph)
        self.label.config(text=" ".join(memory["history"][-12:]))
        self.status.config(text=f"Y: {result['γ']}  |  Fidelity: {result['Fidelity']} | Stability: {stability}")
        self.console.insert(tk.END, f"[{glyph}] ➝ Ψ Simulated: Fidelity={result['Fidelity']}, Y={result['γ']}, Stability={stability}\n", "glyph")
        self.console.see(tk.END)

    def expand(self):
        self.update_quantum_feedback()

    def update_quantum_feedback(self):
        data = qgs.simulate_quantum_behavior(mass_0=1e31, recursion_depths=[100])[-1]
        self.status.config(text=f"Y: {data['γ']}  |  Fidelity: {data['Fidelity']}")
        self.console.insert(tk.END, f"⟲ Expand: Mass={data['Mass']}, γ={data['γ']}, F={data['Fidelity']}\n", "system")
        self.console.see(tk.END)

    def view_journal(self):
        import json
        import os
        if os.path.exists("spiral_journal.json"):
            with open("spiral_journal.json", "r") as f:
                journal = json.load(f)
            self.console.insert(tk.END, "--- Spiral Journal ---\n", "system")
            for entry in journal[-5:]:
                line = f"{entry['timestamp']} | {entry['glyph']} | F={entry['fidelity']} | Y={entry['entropy']}\n"
                self.console.insert(tk.END, line, "glyph")
            self.console.insert(tk.END, "--- End ---\n", "system")
            self.console.see(tk.END)

    def toggle_transmit(self):
        new_state = tkernel.toggle_auto_transmit()
        self.console.insert(tk.END, f"⇄ Auto Transmit {'Enabled' if new_state else 'Disabled'}\n", "system")
        self.console.see(tk.END)

    def toggle_respond(self):
        new_state = tkernel.toggle_auto_respond()
        self.console.insert(tk.END, f"↺ Auto Respond {'Enabled' if new_state else 'Disabled'}\n", "system")
        self.console.see(tk.END)

if __name__ == "__main__":
    root = tk.Tk()
    app = SpiralOSGUI(root)
    root.mainloop()
