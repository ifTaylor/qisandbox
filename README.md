# qisandbox

## What's been practiced.
- Select and set up an IBM Quantum channel:
https://docs.quantum.ibm.com/start/setup-channel#set-up-to-use-ibm-quantum-platform
- Hello world:
https://docs.quantum.ibm.com/start/hello-world

- Introduction:
https://docs.quantum.ibm.com/build
    - Construct circuits:
    https://docs.quantum.ibm.com/build/circuit-construction
    - Operator's module overview:
    https://docs.quantum.ibm.com/build/operators-overview

## Next Step(s):
- Introduction:
https://docs.quantum.ibm.com/build
    - Circuit library:
    https://docs.quantum.ibm.com/build/circuit-library
    - Pulse schedules:
    https://docs.quantum.ibm.com/build/pulse
    - Classical feedforward and control flow:
    https://docs.quantum.ibm.com/build/classical-feedforward-and-control-flow

- Tutorials:
https://learning.quantum.ibm.com/catalog/tutorials
    - Glover's algorithm:
    https://learning.quantum.ibm.com/tutorial/grovers-algorithm
    - CHSH inequality:
    https://learning.quantum.ibm.com/tutorial/chsh-inequality

## Reference
Courses:
https://learning.quantum.ibm.com/catalog/courses

## Vocab
- Cooper Pairs:\
    In a low temperature superconductor, electrons pair due to the net attractive interaction from the exchange of virtual photons(interaction bridge in Feynman diag.). This attraction overcomes the Coulomb repulsion between electrons. The pair end up having opposite spin states, thus creating the Cooper pair. A macro-quantum state, superconducting condensate, is created as more pairs saturate the material. The collective of Cooper pairs exhibit coherent behavior, or a clear state, allowing the phenomenon of supercurrent flow.

    The manipulation and control of Cooper pairs within Josephson junctions are used to represent and process quantum information. It is the superconductor's coherent state of macro subatomic behavior that carries the state of a qubit.

- Josephson Junctions:\
    Two superconducting materials, known as islands, containing aluminum or niobium are separated by a thin insulating barrier. Quantum tunneling is possible from one superconductor's Cooper pair, its wave-like nature, and its probabilistic position to have definite position within the second superconductor. 
    
    The probability of tunneling is influenced by the thickness of the barrier and matching the Cooper pair's energy level allowed by the barrier from applied magnetic flux or voltage. This energy match is known as the Josephson energy. Resonance conditions increase the probability of successful tunneling. Although not accurate I picture a water wave crashing on a wall, where the height of the wall is proportional to the barrier's thickness. The water splashing to the other side of the wall would be analogous to a particle's position tunneling. It's easier to splash over depending on wall's height and the waves energy from a resonate input(creating waves in a pool from osculating an inner tube up and down like we all have done).     
    
    A Josephson junction is described in terms of the phase difference across the two islands, or superconducting electrodes. The difference is defined by the number of Cooper pairs tunneling through. The relationship between the supercurrent flowing through the junction and the phase difference across islands is known as the Josephson relation.

    Junction Control:
    - Gate Voltage
    - Bias Voltage
    - Magnetic fields
    - Superconducting loops (SQUIDs, interference)
    - Microwave signals (resonance)
    - Temperature control

- Measurement: A readout resonator probes the qubit state with with microwave signals.
