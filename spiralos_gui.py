# SpiralOS GUI Interface — Tkinter Glyph Visualizer

import tkinter as tk
from tkinter import messagebox
from spiral_memory import load_memory, advance_state
from modules import quantum_glyph_simulator as qgs

class SpiralGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("SpiralOS GUI")
        self.memory = load_memory()

        self.label = tk.Label(root, text=f"Current Glyph: {self.memory['current_glyph']}", font=("Helvetica", 18))
        self.label.pack(pady=20)

        self.history_text = tk.Text(root, height=5, width=40)
        self.history_text.pack()
        self.refresh_history()

        btn_frame = tk.Frame(root)
        btn_frame.pack(pady=10)

        tk.Button(btn_frame, text="⟲ Expand", command=self.expand).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="Ψ Simulate", command=self.simulate).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="∅ Exit", command=self.root.quit).pack(side=tk.LEFT, padx=5)

    def expand(self):
        next_glyph = advance_state(self.memory)
        self.label.config(text=f"Current Glyph: {next_glyph}")
        self.refresh_history()

    def simulate(self):
        messagebox.showinfo("Simulate", "Launching Quantum Glyph Simulation...")
        qgs.main()

    def refresh_history(self):
        self.history_text.delete(1.0, tk.END)
        self.history_text.insert(tk.END, " → ".join(self.memory["history"]))

if __name__ == "__main__":
    root = tk.Tk()
    gui = SpiralGUI(root)
    root.mainloop()
