# spiralos_gui.py — SpiralOS GUI with Transmission Integration + Sound Layer

import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
import numpy as np
import networkx as nx
import threading
import time
import pygame

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
        self.console = tk.Text(root, height=5, bg="black", fg="white", insertbackground="white")
        self.console.pack()
        self.status = ttk.Label(root, text="Y: N/A  |  Fidelity: N/A", font=("Courier", 10))
        self.status.pack()

        self.expand_button = ttk.Button(root, text="⟲ Expand", command=self.expand)
        self.expand_button.pack(side="left", padx=5, pady=5)

        self.simulate_button = ttk.Button(root, text="Ψ Simulate", command=self.simulate)
        self.simulate_button.pack(side="left", padx=5, pady=5)

        self.journal_button = ttk.Button(root, text="
