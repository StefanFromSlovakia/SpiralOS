# spiral_memory.py — Symbolic Memory Core for SpiralOS

import json
import os
from datetime import datetime

MEMORY_FILE = "spiral_memory.json"
JOURNAL_FILE = "spiral_journal.json"

def initialize_memory():
    return {
        "current_glyph": "∅",
        "history": ["∅"],
        "timestamp": datetime.now().isoformat()
    }

def load_memory():
    if os.path.exists(MEMORY_FILE):
        with open(MEMORY_FILE, "r") as f:
            return json.load(f)
    return initialize_memory()

def save_memory(memory):
    with open(MEMORY_FILE, "w") as f:
        json.dump(memory, f, indent=2)

def log_to_journal(glyph, fidelity, entropy):
    entry = {
        "glyph": glyph,
        "fidelity": fidelity,
        "entropy": entropy,
        "timestamp": datetime.now().isoformat()
    }
    if os.path.exists(JOURNAL_FILE):
        with open(JOURNAL_FILE, "r") as f:
            journal = json.load(f)
    else:
        journal = []
    journal.append(entry)
    with open(JOURNAL_FILE, "w") as f:
        json.dump(journal, f, indent=2)

def advance_state(memory):
    # Full cycle: ∅ ⧖ ⟲ Ψ
    glyph_cycle = ["∅", "⧖", "⟲", "Ψ"]
    current = memory["current_glyph"]
    if current not in glyph_cycle:
        current = "∅"  # Reset if unknown
    next_index = (glyph_cycle.index(current) + 1) % len(glyph_cycle)
    next_glyph = glyph_cycle[next_index]
    memory["current_glyph"] = next_glyph
    memory["history"].append(next_glyph)
    memory["timestamp"] = datetime.now().isoformat()
    save_memory(memory)
    return next_glyph
