# prototype.py
import random
import numpy as np

def simulate_eve(qubits, eve_probability=0.1):
    """
    Placeholder simulate_eve function.
    Replace this with your existing simulate_eve implementation if present.
    """
    disturbed = []
    for i in range(qubits):
        if random.random() < eve_probability:
            disturbed.append(i)
    return disturbed

# Qiskit BB84 Eve Fingerprint (requires: pip install qiskit qiskit-aer)
try:
    from qiskit import QuantumCircuit
    from qiskit_aer import AerSimulator
    import numpy as np

    def qiskit_bb84_fingerprint(nqubits=4, eve_prob=0.15, shots=2048, seed=None):
        """BB84 simulation: Eve intrusions create unique qubit disturbance fingerprints.

        Returns:
          dominant (str): bitstring with the most frequent measurement outcome
          counts (dict): full counts dictionary from the simulator
          qber (float): simplified QBER estimate (fraction of 1-bits in dominant pattern)
        """
        if seed is not None:
            np.random.seed(seed)
        qc = QuantumCircuit(nqubits, nqubits)
        for i in range(nqubits):
            qc.h(i)  # Prepare in Hadamard (random basis effect)
            if np.random.rand() < eve_prob:  # Eve measures/disturbs with given probability
                qc.x(i)  # Represent disturbance as a bit flip fingerprint
        qc.measure_all()
        sim = AerSimulator()
        result = sim.run(qc, shots=shots).result()
        counts = result.get_counts()
        # Choose the most frequent outcome as the "dominant intrusion pattern"
        dominant = max(counts, key=counts.get)
        # Simplified QBER: fraction of 1-bits in the dominant pattern
        qber = sum(int(b) for b in dominant) / nqubits
        return dominant, counts, qber

    # Demo usage — placed under __main__ so it doesn't run on import
    if __name__ == "__main__":
        print("
Quantum BB84 Eve Fingerprint:")
        fp, counts, qber = qiskit_bb84_fingerprint()
        print(f"Fingerprint: {fp} (QBER: {qber:.2f})")
except ImportError:
    # Informative message if qiskit or qiskit-aer is not installed
    print("Qiskit not installed: pip install qiskit qiskit-aer")
