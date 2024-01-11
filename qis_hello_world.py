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
    def __init__(
        self,
        simulated,
        show_circuit
    ):
        self.simulated = simulated
        self.show_circuit = show_circuit

    def bell_state(self):
        """
        Step 1: Map the problem to a quantum-native format.
            Circuits represent quantum instructions and operators
            represent the observables we want to measure.

        This code creates a circuit that produces a Bell state,
        which is a specific two-qubit, entangled state.

        """
        print('Building circuit.')
        # Create a circuit with two qubits
        qc = QuantumCircuit(2)

        # Attribute a Hadamard gate to qubit 0
        qc.h(0)

        # Perform a CNOT gate on qubit 1, controlled by qubit 0
        qc.cx(0, 1)

        # Draw the circuit using matplotlib
        if self.show_circuit:
            qc.draw(output='mpl', style='clifford')
            plt.show() if self.show_circuit else None

        return qc

    def pauli(self):
        """
        Create two-qubit Pauli operators.

        This method creates the following two-qubit Pauli operators:

        - ZZ: Represents the Pauli Z operator acting on qubit 1 and qubit 2 simultaneously.
        - ZI: Represents the Pauli Z operator acting only on qubit 1.
        - IZ: Represents the Pauli Z operator acting only on qubit 2.
        - XX: Represents the Pauli X operator acting on both qubit 1 and qubit 2 simultaneously.
        - XI: Represents the Pauli X operator acting only on qubit 1.
        - IX: Represents the Pauli X operator acting only on qubit 2.

        If the state is entangled, the correlation between the two qubits is 1.

        :return: Dictionary containing Pauli operators.
        """
        self.pauli_observables = {
            'ZZ': Pauli('ZZ'),
            'ZI': Pauli('ZI'),
            'IZ': Pauli('IZ'),
            'XX': Pauli('XX'),
            'XI': Pauli('XI'),
            'IX': Pauli('IX')
        }

    """
    Step 2: Optimize the circuits and operators.

    No optimization a required, as the functions are fundamental.

    """

    def get_output_sample(
            self,
            service,
            circuit,
    ):
        """
        Step 3: Execute using a quantum primitive function.

        This code returns a sample of results. Quantum computers can
        product random results. Estimator is the primitive function used
        here.

        """
        print(f'Building backend, simulated: {self.simulated}')
        if not self.simulated:
            backend = service.least_busy(
                simulator=False,
                operational=True
            )
        else:
            backend = service.get_backend('ibmq_qasm_simulator')

        options = Options()
        options.resilience_level = 1
        options.optimization_level = 3

        estimator = Estimator(
            backend,
            options=options
        )

        print(f'Estimator circuits: {estimator}')

        job = estimator.run(
            circuits=[circuit]*6,
            observables=[
                self.pauli_observables['ZZ'],
                self.pauli_observables['ZI'],
                self.pauli_observables['IZ'],
                self.pauli_observables['XX'],
                self.pauli_observables['XI'],
                self.pauli_observables['IX']
            ],
            shots=5000
        )

        print(f'Job id: {job.job_id()}')

        return job

    def visualize(self, job):
        observables = list(self.pauli_observables.keys())
        print(f'Starting result, with settings: {observables}')
        values = job.result().values

        # Error bars
        error = []
        for case in job.result().metadata:
            error.append(2*np.sqrt(case['variance']/case['shots']))

        plt.plot(observables, values)
        plt.errorbar(observables, values, yerr=error, fmt='o')
        plt.xlabel('Observables')
        plt.ylabel('Values')
        plt.show()


if __name__ == '__main__':
    hello = HelloQuantum(
        simulated=True,
        show_circuit=False
    )

    # Step 1: Map the problem to a quantum-native format.
    circuit = hello.bell_state()
    hello.pauli()

    # Step 3: Execute using a quantum primitive function.
    print('Starting IBM service...')
    service_builder = QisServiceBuilder()
    service = service_builder.auth()
    print(f'Service(s): {service.instances()}')

    estimate_sample = hello.get_output_sample(
        service,
        circuit
    )

    # Step 4: Analyze the results.
    hello.visualize(estimate_sample)
