# SpiralOS GUI Interface — Tkinter Glyph Visualizer (Full Quantum-Symbolic Interface)

import tkinter as tk
from tkinter import messagebox, simpledialog
import math
from spiral_memory import load_memory, advance_state
from modules import quantum_glyph_simulator as qgs

class SpiralGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("SpiralOS GUI")
        self.memory = load_memory()

        self.canvas = tk.Canvas(root, width=400, height=300, bg="black")
        self.canvas.pack(pady=10)
        self.spiral_points = self.generate_spiral_points()
        self.spiral_dots = []
        self.draw_spiral_background()

        self.glyph_text = self.canvas.create_text(200, 150, text=self.memory['current_glyph'], font=("Courier", 64), fill="cyan")

        self.history_text = tk.Text(root, height=4, width=40)
        self.history_text.pack()
        self.refresh_history()

        btn_frame = tk.Frame(root)
        btn_frame.pack(pady=10)

        tk.Button(btn_frame, text="⟲ Expand", command=self.expand).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="Ψ Simulate", command=self.simulate).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="🧠 Journal", command=self.record_journal).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="∅ Exit", command=self.root.quit).pack(side=tk.LEFT, padx=5)

        self.feedback_label = tk.Label(root, text="γ: N/A  |  Fidelity: N/A", fg="white", bg="black", font=("Courier", 10))
        self.feedback_label.pack(pady=5)

        self.animate_rotation()

    def generate_spiral_points(self):
        points = []
        center_x, center_y = 200, 150
        radius = 2
        angle = 0.0
        while radius < 140:
            x = center_x + radius * math.cos(angle)
            y = center_y + radius * math.sin(angle)
            points.append((x, y))
            angle += 0.2
            radius += 0.3
        return points

    def draw_spiral_background(self):
        for x, y in self.spiral_points:
            dot = self.canvas.create_oval(x, y, x + 1, y + 1, fill="gray", outline="")
            self.spiral_dots.append(dot)

    def rotate_spiral(self):
        center_x, center_y = 200, 150
        rotated = []
        for i, (x, y) in enumerate(self.spiral_points):
            angle = math.radians(2)
            dx, dy = x - center_x, y - center_y
            rx = dx * math.cos(angle) - dy * math.sin(angle)
            ry = dx * math.sin(angle) + dy * math.cos(angle)
            new_x, new_y = center_x + rx, center_y + ry
            rotated.append((new_x, new_y))
            self.canvas.coords(self.spiral_dots[i], new_x, new_y, new_x + 1, new_y + 1)
        self.spiral_points = rotated

    def animate_rotation(self):
        self.rotate_spiral()
        self.root.after(50, self.animate_rotation)

    def glyph_to_color(self, glyph):
        return {
            "∅": "gray",
            "⧖": "orange",
            "⟲": "cyan",
            "Ψ": "magenta"
        }.get(glyph, "white")

    def expand(self):
        next_glyph = advance_state(self.memory)
        self.canvas.itemconfig(self.glyph_text, text=next_glyph)
        self.canvas.itemconfig(self.glyph_text, fill=self.glyph_to_color(next_glyph))
        self.refresh_history()
        self.animate_flash()
        self.update_quantum_feedback()

    def simulate(self):
        messagebox.showinfo("Simulate", "Launching Quantum Glyph Simulation...")
        qgs.main()

    def refresh_history(self):
        self.history_text.delete(1.0, tk.END)
        self.history_text.insert(tk.END, " → ".join(self.memory["history"]))

    def animate_flash(self):
        def flash(count):
            color = self.glyph_to_color(self.memory["current_glyph"]) if count % 2 == 0 else "black"
            self.canvas.itemconfig(self.glyph_text, fill=color)
            if count < 6:
                self.root.after(100, flash, count + 1)
            else:
                self.canvas.itemconfig(self.glyph_text, fill=color)
        flash(0)

    def update_quantum_feedback(self):
        from modules.quantum_glyph_simulator import simulate_quantum_behavior
        data = simulate_quantum_behavior(mass_0=1e31, recursion_depths=[100])[-1]
        γ = round(data["γ"], 5)
        fidelity = round(data["Fidelity"], 5)
        self.feedback_label.config(text=f"γ: {γ}  |  Fidelity: {fidelity}")

    def record_journal(self):
        entry = simpledialog.askstring("SpiralOS Journal", "What symbolic insight or dream would you like to record?")
        if entry:
            with open("spiral_journal.txt", "a") as f:
                f.write(f"\n[{self.memory['current_glyph']}] {entry}\n")
            messagebox.showinfo("Saved", "Your reflection has been added to spiral_journal.txt")

if __name__ == "__main__":
    root = tk.Tk()
    gui = SpiralGUI(root)
    root.mainloop()
