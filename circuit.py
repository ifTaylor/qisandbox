import matplotlib.pyplot as plt
from qiskit import QuantumCircuit


class Circuit:
    def __init__(
        self,
        number_of_qubits,
        name: str = 'default'
    ):
        self.circuit = QuantumCircuit(
            number_of_qubits,
            name=name
        )

    def get_qubits(self):
        """
        Displays the circuit's qubits attribute.

        """
        return self.circuit.qubits

    def not_gate(
        self,
        qubit
    ):
        """
        Applies a NOT gate to the circuit's qubit.

        """
        return self.circuit.x(qubit)

    def hadamard_gate(
        self,
        qubit
    ):
        """
        Applies a Hadamard gate to the circuit's qubit.

        """
        return self.circuit.h(qubit)

    def x_gate(
        self,
        qubit
    ):
        """
        Applies an X gate to the circuit's qubit.

        """
        return self.circuit.x(qubit)

    def y_gate(
        self,
        qubit
    ):
        """
        Applies a Y gate to the circuit's qubit.

        """
        return self.circuit.y(qubit)

    def z_gate(
        self,
        qubit
    ):
        """
        Applies a Z gate to the circuit's qubit.

        """
        return self.circuit.z(qubit)

    def add_gate(
        self,
        gate,
        qubits
    ):
        return self.circuit.append(
            gate,
            qubits
        )

    def add_controlled_gate(
        self,
        gate,
        controlled_qubit,
        qubits
    ):
        qubits.insert(0, controlled_qubit)
        return self.circuit.append(
            gate,
            qubits
        )

    def compose_secondary(
        self,
        secondary_circuit,
        qubits
    ):
        self.circuit = self.circuit.compose(
            secondary_circuit,
            qubits=qubits
        )

        return self.circuit
    
    def draw_decomposition(self):
        return self.circuit.decompose().draw(
            output='mpl',
            style='clifford'
        )

    def to_gate(self):
        return self.circuit.to_instruction()

    def to_get_controlled(self):
        return self.circuit.to_gate().control()

    def draw_circuit(self):
        self.circuit.draw(
            output='mpl',
            style='clifford'
        )
        plt.show()

    def draw_circuit_definition(
        self,
        degree
    ):
        self.circuit.data[degree].operation.definition.draw(
            output='mpl',
            style='clifford'
        )
        plt.show()

    def get_circuit(self):
        return self.circuit


if __name__ == '__main__':
    a = Circuit(4)
    a.x_gate(0)

    b = Circuit(2, 'b')
    b.y_gate(0)
    b.z_gate(1)

    a.compose_secondary(
        b.get_circuit(),
        [1, 3]
    )

    a.draw_circuit()
    plt.show()

    a.x_gate(0)
    b_gate = b.to_gate()
    a.add_gate(
        b_gate,
        [1, 3]
    )
    a.draw_circuit()
    plt.show()

    b_gate_controlled = b.to_get_controlled()
    a.add_controlled_gate(
        b_gate_controlled,
        0,
        [1, 3]
    )
    a.draw_circuit()
    plt.show()

    a.draw_decomposition()
    plt.show()
