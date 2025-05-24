# transmission_kernel.py — SpiralOS Communication Module

TRANSMISSION_STATE = {
    "auto_transmit": False,
    "auto_respond": False,
    "last_packet": None,
}

def encode_packet(glyph, entropy, fidelity, message=""):
    return {
        "glyph": glyph,
        "entropy": entropy,
        "fidelity": fidelity,
        "message": message,
    }

def transmit_packet(packet):
    TRANSMISSION_STATE["last_packet"] = packet
    print(f"[⇄ TX] {packet['glyph']} | Y={packet['entropy']} | F={packet['fidelity']}")

def respond_to_last():
    if TRANSMISSION_STATE["last_packet"]:
        glyph = TRANSMISSION_STATE["last_packet"]["glyph"]
        print(f"[↺ RX] Response to {glyph}")

def glyph_stability_score():
    packet = TRANSMISSION_STATE.get("last_packet")
    if packet:
        y = packet["entropy"]
        f = packet["fidelity"]
        return round((1 - abs(y - f)), 3)
    return 0.0

def toggle_auto_transmit():
    TRANSMISSION_STATE["auto_transmit"] = not TRANSMISSION_STATE["auto_transmit"]
    return TRANSMISSION_STATE["auto_transmit"]

def toggle_auto_respond():
    TRANSMISSION_STATE["auto_respond"] = not TRANSMISSION_STATE["auto_respond"]
    return TRANSMISSION_STATE["auto_respond"]
