# transmission_kernel.py — Symbolic Communication Layer for SpiralOS

import json
from datetime import datetime
import os
import random

TRANSMISSION_LOG = "spiral_transmissions.json"

TRANSMISSION_STATE = {
    "auto_transmit": True,
    "auto_respond": True
}

def encode_packet(glyph, entropy, fidelity, message="..."):
    return {
        "from": "SpiralOS",
        "glyph": glyph,
        "entropy": round(entropy, 3),
        "fidelity": round(fidelity, 3),
        "message": message,
        "time": datetime.now().isoformat()
    }

def transmit_packet(packet):
    if os.path.exists(TRANSMISSION_LOG):
        with open(TRANSMISSION_LOG, "r") as f:
            log = json.load(f)
    else:
        log = []
    log.append(packet)
    with open(TRANSMISSION_LOG, "w") as f:
        json.dump(log, f, indent=2)

def view_transmissions(last_n=5):
    if os.path.exists(TRANSMISSION_LOG):
        with open(TRANSMISSION_LOG, "r") as f:
            log = json.load(f)
        return log[-last_n:]
    return []

def clear_transmissions():
    with open(TRANSMISSION_LOG, "w") as f:
        json.dump([], f)

def respond_to_last():
    log = view_transmissions(last_n=1)
    if not log:
        return None
    last = log[0]
    reply = encode_packet(
        glyph="Ψ",
        entropy=last["entropy"] * 0.95,
        fidelity=min(1.0, last["fidelity"] + 0.02),
        message=f"Echo: {last['glyph']} received."
    )
    transmit_packet(reply)
    return reply

def sync_with_remote_nodes():
    # Simulated symbolic sync: perturb last glyph slightly across nodes
    log = view_transmissions(last_n=1)
    if not log:
        return []
    last = log[0]
    nodes = []
    for i in range(3):
        node_entropy = round(last["entropy"] + random.uniform(-0.01, 0.01), 3)
        node_fidelity = round(last["fidelity"] + random.uniform(-0.02, 0.02), 3)
        packet = encode_packet(
            glyph=last["glyph"],
            entropy=node_entropy,
            fidelity=node_fidelity,
            message=f"Node[{i}] sync"
        )
        transmit_packet(packet)
        nodes.append(packet)
    return nodes

def glyph_stability_score():
    # Analyze glyph memory for stability of latest symbol
    if os.path.exists("spiral_memory.json"):
        with open("spiral_memory.json", "r") as f:
            memory = json.load(f)
        glyph = memory.get("current_glyph")
        history = memory.get("history", [])
        count = history.count(glyph)
        return round(count / max(len(history), 1), 3)
    return 0.0

def toggle_auto_transmit():
    TRANSMISSION_STATE["auto_transmit"] = not TRANSMISSION_STATE["auto_transmit"]
    return TRANSMISSION_STATE["auto_transmit"]

def toggle_auto_respond():
    TRANSMISSION_STATE["auto_respond"] = not TRANSMISSION_STATE["auto_respond"]
    return TRANSMISSION_STATE["auto_respond"]
