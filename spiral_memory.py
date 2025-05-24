import json

MEMORY_FILE = "spiral_memory.json"

def load_memory():
    try:
        with open(MEMORY_FILE, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {"current_glyph": "∅", "history": ["∅"]}

def save_memory(memory):
    with open(MEMORY_FILE, "w") as f:
        json.dump(memory, f)

def advance_state(memory):
    glyphs = ["∅", "⧖", "⟲", "Ψ"]
    idx = glyphs.index(memory["current_glyph"])
    next_glyph = glyphs[(idx + 1) % len(glyphs)]
    memory["current_glyph"] = next_glyph
    memory["history"].append(next_glyph)
    save_memory(memory)
    return next_glyph
