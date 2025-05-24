import tkinter as tk
import simpleaudio as sa
import threading
import math
from audio import SafeAudioPlayer

# Initialize audio player
audio = SafeAudioPlayer()

class SpiralApp:
    def __init__(self, root):
        self.root = root
        self.root.title("SpiralOS GUI")
        self.canvas = tk.Canvas(root, width=600, height=600, bg='black')
        self.canvas.pack()

        self.angle = 0
        self.spiral_id = None

        self.play_button = tk.Button(root, text="Play Spiral", command=self.start_spiral)
        self.play_button.pack(side=tk.LEFT, padx=10, pady=10)

        self.stop_button = tk.Button(root, text="Stop Spiral", command=self.stop_spiral)
        self.stop_button.pack(side=tk.LEFT, padx=10, pady=10)

        self.silent_var = tk.IntVar()
        self.silent_check = tk.Checkbutton(root, text="Silent Mode", variable=self.silent_var, command=self.toggle_silent_mode)
        self.silent_check.pack(side=tk.LEFT, padx=10, pady=10)

    def toggle_silent_mode(self):
        if self.silent_var.get():
            audio.enable_silent_mode()
        else:
            audio.disable_silent_mode()

    def draw_spiral(self):
        self.canvas.delete("all")
        center_x, center_y = 300, 300
        points = []
        for i in range(100):
            angle = self.angle + i * 0.1
            radius = 5 * i
            x = center_x + radius * math.cos(angle)
            y = center_y + radius * math.sin(angle)
            points.append((x, y))
        for i in range(len(points) - 1):
            self.canvas.create_line(points[i], points[i+1], fill='cyan', width=2)
        self.angle += 0.1
        self.spiral_id = self.root.after(50, self.draw_spiral)

    def start_spiral(self):
        self.stop_spiral()
        self.draw_spiral()
        try:
            wave_obj = sa.WaveObject.from_wave_file("sounds/spiral.wav")
            audio.play(wave_obj)
        except Exception as e:
            print(f"[GUI] Failed to play sound: {e}")

    def stop_spiral(self):
        if self.spiral_id:
            self.root.after_cancel(self.spiral_id)
            self.spiral_id = None
        audio.stop()

if __name__ == '__main__':
    root = tk.Tk()
    app = SpiralApp(root)
    root.mainloop()
