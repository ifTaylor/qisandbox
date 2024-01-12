import math
import matplotlib.pyplot as plt
from qiskit import QuantumCircuit
from qiskit.circuit.library import GroverOperator, MCMT, ZGate
from qiskit.visualization import plot_distribution

from qiskit_ibm_runtime import Sampler, Batch


class Grover():
    def __init__(
        self,
        backend,
        marked_states
    ):
        self.backend = backend
        self.marked_states = marked_states

    def grover_oracle(self):
        """Build a Grover oracle for multiple marked states

        Here we assume all input marked states have the same number of bits

        Parameters:
            marked_states (str or list): Marked states of oracle

        Returns:
            QuantumCircuit: Quantum circuit representing Grover oracle
        """
        if not isinstance(self.marked_states, list):
            self.marked_states = [self.marked_states]
        # Compute the number of qubits in circuit
        num_qubits = len(self.marked_states[0])

        circuit = QuantumCircuit(num_qubits)
        # Mark each target state in the input list
        for target in self.marked_states:
            # Flip target bit-string to match Qiskit bit-ordering
            rev_target = target[::-1]
            # Find the indices of all the '0' elements in bit-string
            zero_inds = [ind for ind in range(num_qubits) 
                         if rev_target.startswith("0", ind)]
            # Add a multi-controlled Z-gate with pre- and post-applied
            # X-gates (open-controls) where the target bit-string has
            # a '0' entry
            if zero_inds:
                circuit.x(zero_inds)
                circuit.compose(MCMT(ZGate(), num_qubits - 1, 1), inplace=True)
                circuit.x(zero_inds)

        return circuit

    def grover_operator(
            self,
            circuit
    ):
        grover_op = GroverOperator(circuit)
        self.optimal_num_iterations = math.floor(
            math.pi / 4 * math.sqrt(2**grover_op.num_qubits / len(self.marked_states))
        )

        return grover_op

    def grover_experiment_circuit(
        self,
        grover_operator
    ):
        circuit = QuantumCircuit(
            grover_operator.num_qubits
        )

        # Creates an even superposition of all bias states
        circuit.h(range(grover_operator.num_qubits))

        # Apply Grover operator
        circuit.compose(
            grover_operator.power(self.optimal_num_iterations),
            inplace=True
        )

        circuit.measure_all()

        return circuit

    def run_grover(self):
        oracle_circuit = self.grover_oracle()
        oracle_circuit.draw(output='mpl', style='iqp')

        grover_op = self.grover_operator(oracle_circuit)
        grover_op.decompose().draw(output='mpl', style='iqp')

        circuit = self.grover_experiment_circuit(grover_op)
        circuit.draw(output='mpl', style='iqp')

        with Batch(backend=self.backend):
            sampler = Sampler()
            job = sampler.run(
                circuit,
                shots=10000
            ).result().quasi_dists[0]

        plot_distribution(job.binary_probabilities())

        plt.show()
