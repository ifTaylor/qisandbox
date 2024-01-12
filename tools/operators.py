import numpy as np
import matplotlib.pyplot as plt
from qiskit import QuantumCircuit, ClassicalRegister, QuantumRegister
from qiskit import BasicAer
from qiskit.quantum_info.operators import Operator, Pauli
from qiskit.quantum_info import process_fidelity
 
from qiskit.extensions import RXGate, XGate, CXGate

"""
Creating Operators

"""
# Two qubit Pauli operator initialized as a matrix
matrix = [[0, 0, 0, 1], [0, 0, 1, 0], [0, 1, 0, 0], [1, 0, 0, 0]]
XX = Operator(matrix)
print(XX)

"""
Operator Properties

"""
# N-qubit and M-qubit operators
op = Operator(np.random.rand(2**1, 2**2))
print(f'Input rand dimensions: {op.input_dims()}')
print(f'Output rand dimensions: {op.output_dims()}')

op = Operator(np.random.rand(6, 6))
print('Input 6x6 dimensions:', op.input_dims())
print('Output 6x6 dimensions:', op.output_dims())


# Force input dimension to be (4,) rather than (2, 2)
op = Operator(np.random.rand(2 ** 1, 2 ** 2), input_dims=[4])
print('Input force 4 dimension:', op.input_dims())
print('Output dimensions:', op.output_dims())

# Specify system is a qubit and qutrit
op = Operator(np.random.rand(6, 6),
              input_dims=[2, 3], output_dims=[2, 3])
print('Input qutrit dimensions:', op.input_dims())
print('Output qutrit dimensions:', op.output_dims())

# Subsystem dimensions
print('Dimension of input system 0:', op.input_dims([0]))
print('Dimension of input system 1:', op.input_dims([1]))

"""
Converting classes to operators

"""

# Two qubit Pauli operator initialized from library
pauli_XX = Pauli('XX')
XX = Operator(pauli_XX)
print(XX)

# Operator from gate
# (This CNot operator output shows right bit shift.)
cnot_op = Operator(CXGate())
print(cnot_op)

# Operator from parameterized gate.
rotx_param_op = Operator(RXGate(np.pi / 2))
print(rotx_param_op)

# Operator from QuantumCircuit
circuit = QuantumCircuit(10)
circuit.h(0)
for j in range(1, 10):
    circuit.cx(j - 1, j)
circuit.draw(output='mpl', style='clifford')
hadamard_cnot_op = Operator(circuit)
print(hadamard_cnot_op)

"""
Using operators in circuits

"""

# Two qubit Pauli, unitary operator added to circuit
XX = Operator(Pauli('XX'))

circuit = QuantumCircuit(2, 2)
circuit.append(XX, [0, 1])
circuit.measure([0, 1], [0, 1])
circuit.draw(output='mpl', style='clifford')


# Syntax simplified
circuit = QuantumCircuit(2, 2)
circuit.append(Pauli('XX'), [0, 1])
circuit.measure([0, 1], [0, 1])
circuit.draw(output='mpl', style='clifford')


"""
Combining operators

"""

# Tensor product
# Cross product of two, two qubit Pauli operators
A = Operator(Pauli('X'))
print(F'Operator A: {A}')
B = Operator(Pauli('Z'))
print(F'Operator B: {B}')
# A cross B
AxB = A.tensor(B)
print(f'A cross B prod: {AxB}')

# Tensor expansion
# B cross A (same output for both)
BxA_expand = A.expand(B)
print(f'AB expand: {BxA_expand}')
BxA_prod = B.tensor(A)
print(f'B cross A prod: {BxA_prod}')

# Composition
# Matrix multiplication
AB = A.compose(B)
print(f'A * B: {AB}')

# Reverse composition
# Multiply B before A (non symmetric in q world)
BA_rev = A.compose(B, front=True)
print(f'B * A: {BA_rev}')

# Subsystem composition
op = Operator(np.eye(2 ** 3))
XZ = Operator(Pauli('XZ'))
opXZ = op.compose(XZ, qargs=[0, 2])
print(f'opXZ: {opXZ}')

YX = Operator(Pauli('YX'))
opYX = op.compose(YX, qargs=[0, 2], front=True)
print(f'opYX: {opYX}')

# Linear combinations
# Subject to arithmetic and scalar multiplication by complex numbers
XX = Operator(Pauli('XX'))
YY = Operator(Pauli('YY'))
ZZ = Operator(Pauli('ZZ'))

op = 0.5 * (XX + YY - 3 * ZZ)
print(f'op: {op}')

# Check if unitary
print(f'Check for unitary: {op.is_unitary()}')

"""
Comparison of Operators

"""


def equal(op1, op2):
    return op1 == op2


# Equality method to check if two operators are approximately equal
print(equal(Operator(Pauli('X')), Operator(XGate())))
print(equal(Operator(Pauli('X')), np.exp(1j * 0.5) * Operator(XGate())))

# Process fidelity
op_a = Operator(XGate())
op_b = np.exp(1j * 0.5) * Operator(XGate())

# Compute process fidelity
# Theoretic quantity for how close two quantum channels are.
F = process_fidelity(op_a, op_b)
print('Process fidelity =', F)


plt.show()
