import os
from qiskit import QuantumCircuit
from qiskit_ibm_runtime import QiskitRuntimeService, Sampler


class QisServiceBuilder:
    def __init__(
        self,
        simulated
    ):
        self.simulated = simulated

    def auth(self):
        """
        Initialize the Qiskit Runtime service.

        Returns:
            QiskitRuntimeService: The Qiskit Runtime service.
        """
        self.service = QiskitRuntimeService(
            channel="ibm_quantum",
            token=os.environ.get('IBM_QUANTUM_TOKEN')
        )

        return self.service

    def auth_lib(self):
        """
        Save credentials for easy access later on, before initializing the
        service.

        Returns:
            QiskitRuntimeService: The initialized Qiskit Runtime service.
        """
        self.service = QiskitRuntimeService.save_account(
            channel="ibm_quantum",
            token=os.environ.get('IBM_QUANTUM_TOKEN'),
            set_as_default=True
        )

        return self.service

    def get_status(self, service):
        """
        Simple circuit using Sampler to ensure that the environment is
        set up correctly.

        Returns:
            result: output of the circuit
        """
        # Create empty circuit
        circuit = QuantumCircuit(2)
        circuit.measure_all()

        service = self.auth()
        backend = service.backend("ibmq_qasm_simulator")
        job = Sampler(backend).run(circuit)
        print(f'job id: {job.job_id()}')
        result = job.result()
        print(result)

        return {
            'job_id': job.job_id(),
            'result': result
        }

    def start_backend(self):
        return (
            self.service.least_busy(
                simulator=self.simulated,
                operational=True
            )
            if not self.simulated
            else self.service.get_backend('ibmq_qasm_simulator')
        )


if __name__ == '__main__':
    service_builder = QisServiceBuilder()
    service = service_builder.auth()
    result = service_builder.get_status(service)

    print(result)
