import tkinter as tk
from tkinter import ttk
import numpy as np
import json
import os
from spiral_memory import load_memory, advance_state, log_to_journal
import modules.quantum_glyph_simulator as qgs

class SpiralOSGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("SpiralOS GUI")
        self.angle_offset = 0.0

        # Layout Frame
        self.frame = tk.Frame(root, bg="black")
        self.frame.pack(fill="both", expand=True)

        # Spiral Canvas
        self.canvas = tk.Canvas(self.frame, width=400, height=400, bg="black", highlightthickness=0)
        self.canvas.pack()

        # Glyph trail / history
        self.label = tk.Label(self.frame, text="", fg="white", bg="black", font=("Courier", 10))
        self.label.pack(fill="x", pady=(0, 4))

        # Console log
        self.console = tk.Text(self.frame, height=5, bg="black", fg="white", insertbackground="white", font=("Courier", 9))
        self.console.pack(fill="x")

        # Status bar
        self.status = tk.Label(self.frame, text="Y: N/A   |   Fidelity: N/A", fg="white", bg="black", font=("Courier", 10))
        self.status.pack(fill="x", pady=(4, 4))

        # Buttons
        self.button_frame = tk.Frame(self.frame, bg="black")
        self.button_frame.pack(fill="x", pady=(0, 5))

        tk.Button(self.button_frame, text="⟲ Expand", command=self.expand).pack(side="left", padx=5)
        tk.Button(self.button_frame, text="Ψ Simulate", command=self.simulate).pack(side="left", padx=5)
        tk.Button(self.button_frame, text="🧠 Journal", command=self.view_journal).pack(side="left", padx=5)
        tk.Button(self.button_frame, text="∅ Exit", command=self.root.quit).pack(side="right", padx=5)

        # Start
        self.memory = load_memory()
        self.update_glyph(self.memory["current_glyph"])
        self.animate_spiral()

    def draw_spiral(self):
        self.canvas.delete("spiral")
        cx, cy = 200, 200
        r_max = 100
        for i in range(100):
            angle = 0.3 * i + self.angle_offset
            r = r_max * i / 100
            x = cx + r * np.cos(angle)
            y = cy + r * np.sin(angle)
            self.canvas.create_oval(x, y, x + 1.5, y + 1.5, fill="white", outline="", tags="spiral")

    def animate_spiral(self):
        self.angle_offset += 0.1
        self.draw_spiral()
        self.root.after(40, self.animate_spiral)

    def update_glyph(self, glyph):
        self.canvas.delete("glyph")
        cx, cy = 200, 200
        self.canvas.create_text(cx, cy, text=glyph, fill="cyan", font=("Courier", 38, "bold"), tags="glyph")

    def simulate(self):
        glyph = self.memory["current_glyph"]
        result = qgs.simulate_quantum_behavior(mass_0=1e31, recursion_depths=[100])[0]
        log_to_journal(glyph, result["Fidelity"], result["γ"])
        next_glyph = advance_state(self.memory)
        self.update_glyph(next_glyph)
        self.label.config(text=" ".join(self.memory["history"][-12:]))
        self.status.config(text=f"Y: {result['γ']:.3f}   |   Fidelity: {result['Fidelity']:.3f}")
        self.console.insert(tk.END, f"[{glyph}] ➝ Ψ Simulated: Fidelity={result['Fidelity']:.3f}, Y={result['γ']:.3f}\n")
        self.console.see(tk.END)

    def expand(self):
        data = qgs.simulate_quantum_behavior(mass_0=1e31, recursion_depths=[100])[-1]
        self.status.config(text=f"Y: {data['γ']:.3f}   |   Fidelity: {data['Fidelity']:.3f}")
        self.console.insert(tk.END, f"⟲ Expand: Mass={data['Mass']:.3f}, γ={data['γ']:.3f}, F={data['Fidelity']:.3f}\n")
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

if __name__ == "__main__":
    root = tk.Tk()
    app = SpiralOSGUI(root)
    root.mainloop()
