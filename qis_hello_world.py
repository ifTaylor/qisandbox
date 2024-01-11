import matplotlib.pyplot as plt
from qiskit import QuantumCircuit
from qiskit.quantum_info import Pauli
from qiskit_ibm_runtime import Estimator, Options
from runtime_service import QisServiceBuilder
import numpy as np

"""
The four steps to writing a quantum program:
    1. Map the problem to a quantum-native format.
    2. Optimize the circuits and operators.
    3. Execute using a quantum primitive function.
    4. Analyze the results.

"""


class HelloQuantum:
    def __init__(self):
        pass

    def bell_state(self):
        """
        Step 1: Map the problem to a quantum-native format.
            Circuits represent quantum instructions and operators
            represent the observables we want to measure.

        This code creates a circuit that produces a Bell state,
        which is a specific two-qubit, entangled state.

        """
        # Create a circuit with two qubits
        qc = QuantumCircuit(2)

        # Attribute a Hadamard gate to qubit 0
        qc.h(0)

        # Perform a CNOT gate on qubit 1, controlled by qubit 0
        qc.cx(0, 1)

        # Draw the circuit using matplotlib
        qc.draw(output='mpl', style='clifford')
        plt.show()

        return qc

    def pauli(self):
        """
        Step 1: cont...

        This code creates teh two-qubit Pauli operator Z on qubit 0 and
        Z on qubit 1. If the state is entangled, the correlation between
        the two qubits is 1.

        """
        ZZ = Pauli('ZZ')
        ZI = Pauli('ZI')
        IZ = Pauli('IZ')
        XX = Pauli('XX')
        XI = Pauli('XI')
        IX = Pauli('IX')

        return {
            'ZZ': ZZ,
            'ZI': ZI,
            'IZ': IZ,
            'XX': XX,
            'XI': XI,
            'IX': IX
        }

    """
    Step 2: Optimize the circuits and operators.

    No optimization a required, as the functions are fundamental.

    """

    def get_output_sample(
            self,
            service,
            circuit,
            pauli
    ):
        """
        Step 3: Execute using a quantum primitive function.

        This code returns a sample of results. Quantum computers can
        product random results. Estimator is the primitive function used
        here.

        """
        backend = service.least_busy(
            simulator=False,
            operational=True
        )

        options = Options()
        options.resilience_level = 1
        options.optimization_level = 3

        estimator = Estimator(
            backend,
            options=options
        )

        job = estimator.run(
            circuits=[circuit]*6,
            observables=[
                pauli['ZZ'],
                pauli['ZI'],
                pauli['IZ'],
                pauli['XX'],
                pauli['XI'],
                pauli['IX']
            ],
            shots=5000
        )

        return job

    def visualize(self, job):
        data = ['IZ', 'IX', 'ZI', 'XI', 'ZZ', 'XX']
        values = job.result().values

        # Error bars
        error = []
        for case in job.result().metadata:
            error.append(2*np.sqrt(case['variance']/case['shots']))

        plt.plot(data, values)
        plt.errorbar(data, values, yerr=error, fmt='o')
        plt.xlabel('Observables')
        plt.ylabel('Values')
        plt.show()


if __name__ == '__main__':
    hello = HelloQuantum()

    # Step 1: Map the problem to a quantum-native format.
    circuit = hello.bell_state()
    pauli = hello.pauli()

    # Step 3: Execute using a quantum primitive function.
    service_builder = QisServiceBuilder()
    service = service_builder.auth()

    estimate_sample = hello.get_output_sample(
        service,
        circuit,
        pauli
    )

    # Step 4: Analyze the results.
    hello.visualize(estimate_sample)
