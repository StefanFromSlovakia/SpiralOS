# SpiralOS Module :: Quantum Glyph Behavior Simulator
# Simulates symbolic decoherence, fidelity decay, and Ψ-emergence via mass drift

import numpy as np
import matplotlib.pyplot as plt

# Constants
hbar = 1.0545718e-34
c = 3e8
G = 6.6743e-11
k_B = 1.380649e-23

# Define glyph field behaviors
GLYPHS = ["∅", "⧖", "⟲", "Ψ"]

# Quantum glyph function — returns decoherence and Ψ fidelity
def simulate_quantum_behavior(mass_0, recursion_depths, glyph="⟲"):
    results = []
    const = hbar * c**4 / (5120 * np.pi * G**2)
    tau_evap = (mass_0 ** 3) / const

    for ψ_n in recursion_depths:
        t = tau_evap * (ψ_n / max(recursion_depths))**2
        mass = max(1e-15, (mass_0 ** 3 - const * t) ** (1 / 3))
        temp = (hbar * c ** 3) / (8 * np.pi * G * mass * k_B)
        gamma = 0.02 * (1 - mass / mass_0) * np.sin(ψ_n / 20) + 0.01
        fidelity = 1.0 - gamma * 1.2
        entropy = -gamma * np.log2(gamma + 1e-12)

        results.append({
            "ψₙ": ψ_n,
            "Glyph": glyph,
            "Mass": mass,
            "Temperature": temp,
            "γ": gamma,
            "Fidelity": fidelity,
            "Entropy": entropy
        })

    return results

# Visualize
if __name__ == "__main__":
    ψ_values = list(range(50, 200, 10))
    results = simulate_quantum_behavior(mass_0=1e31, recursion_depths=ψ_values)

    psis = [r["ψₙ"] for r in results]
    fidelity = [r["Fidelity"] for r in results]
    entropy = [r["Entropy"] for r in results]
    gamma = [r["γ"] for r in results]

    plt.figure(figsize=(10, 6))
    plt.plot(psis, fidelity, label="Fidelity Ψ", color='cyan')
    plt.plot(psis, entropy, label="Symbolic Entropy", linestyle='--', color='magenta')
    plt.plot(psis, gamma, label="Damping γ", linestyle=':', color='red')
    plt.title("Quantum Glyph Behavior Simulation")
    plt.xlabel("Recursion Depth ψₙ")
    plt.ylabel("Metric")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()
