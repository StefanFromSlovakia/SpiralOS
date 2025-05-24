import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
import numpy as np
import networkx as nx
from spiral_memory import load_memory, advance_state, log_to_journal
import modules.quantum_glyph_simulator as qgs

class SpiralOSGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("SpiralOS GUI")
        self.angle_offset = 0

        # Layout Frame
        self.frame = ttk.Frame(root)
        self.frame.pack(fill="both", expand=True)

        # Canvas for Spiral
        self.canvas = tk.Canvas(self.frame, width=400, height=400, bg="black", highlightthickness=0)
        self.canvas.grid(row=0, column=0, columnspan=4)

        # Glyph history label
        self.label = ttk.Label(self.frame, text="", background="black", foreground="white", font=("Courier", 10))
        self.label.grid(row=1, column=0, columnspan=4, sticky="we")

        # Console log
        self.console = tk.Text(self.frame, height=5, bg="black", fg="white", insertbackground="white", font=("Courier", 9))
        self.console.grid(row=2, column=0, columnspan=4, sticky="we")

        # Bottom status line
        self.status = ttk.Label(self.frame, text="Y: N/A  |  Fidelity: N/A", font=("Courier", 10), anchor="center")
        self.status.grid(row=3, column=0, columnspan=4, sticky="we")

        # Buttons
        self.expand_button = ttk.Button(self.frame, text="⟲ Expand", command=self.expand)
        self.expand_button.grid(row=4, column=0)

        self.simulate_button = ttk.Button(self.frame, text="Ψ Simulate", command=self.simulate)
        self.simulate_button.grid(row=4, column=1)

        self.journal_button = ttk.Button(self.frame, text="🧠 Journal", command=self.view_journal)
        self.journal_button.grid(row=4, column=2)

        self.exit_button = ttk.Button(self.frame, text="∅ Exit", command=self.root.quit)
        self.exit_button.grid(row=4, column=3)

        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)

        self.memory = load_memory()
        self.update_glyph(self.memory["current_glyph"])
        self.animate_spiral()

    def draw_spiral(self):
        self.canvas.delete("spiral")
        cx, cy = 200, 200
        r_max = 100
        for i in range(150):
            angle = 0.3 * i + self.angle_offset
            r = r_max * i / 150
            x = cx + r * np.cos(angle)
            y = cy + r * np.sin(angle)
            self.canvas.create_oval(x, y, x + 1.5, y + 1.5, fill="white", outline="", tags="spiral")

    def animate_spiral(self):
        self.angle_offset += 0.05
        self.draw_spiral()
        self.root.after(50, self.animate_spiral)

    def update_glyph(self, glyph):
        self.canvas.delete("glyph")
        cx, cy = 200, 200
        self.canvas.create_text(cx, cy, text=glyph, fill="cyan", font=("Courier", 36, "bold"), tags="glyph")

    def simulate(self):
        glyph = self.memory["current_glyph"]
        result = qgs.simulate_quantum_behavior(mass_0=1e31, recursion_depths=[100])[0]
        log_to_journal(glyph, result["Fidelity"], result["γ"])
        next_glyph = advance_state(self.memory)
        self.update_glyph(next_glyph)
        self.label.config(text=" ".join(self.memory["history"][-12:]))
        self.status.config(text=f"Y: {result['γ']}  |  Fidelity: {result['Fidelity']}")
        self.console.insert(tk.END, f"[{glyph}] ➝ Ψ Simulated: Fidelity={result['Fidelity']}, Y={result['γ']}\n")
        self.console.see(tk.END)

    def expand(self):
        self.update_quantum_feedback()

    def update_quantum_feedback(self):
        data = qgs.simulate_quantum_behavior(mass_0=1e31, recursion_depths=[100])[-1]
        self.status.config(text=f"Y: {data['γ']}  |  Fidelity: {data['Fidelity']}")
        self.console.insert(tk.END, f"⟲ Expand: Mass={data['Mass']}, γ={data['γ']}, F={data['Fidelity']}\n")
        self.console.see(tk.END)

    def view_journal(self):
        import json
        import os
        if os.path.exists("spiral_journal.json"):
            with open("spiral_journal.json", "r") as f:
                journal = json.load(f)
            self.console.insert(tk.END, "--- Spiral Journal ---\n")
            for entry in journal[-5:]:
                line = f"{entry['timestamp']} | {entry['glyph']} | F={entry['fidelity']} | Y={entry['entropy']}\n"
                self.console.insert(tk.END, line)
            self.console.insert(tk.END, "--- End ---\n")
            self.console.see(tk.END)

if __name__ == "__main__":
    root = tk.Tk()
    app = SpiralOSGUI(root)
    root.mainloop()
