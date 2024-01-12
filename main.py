from services.runtime_service import QisServiceBuilder
from algorithms.grovers import Grover

service_builder = QisServiceBuilder(simulated=True)
service = service_builder.auth()
backend = service_builder.start_backend()
print(f"""
    Service(s): {service.instances()}
    Backend: {backend.name}
""")

marked_states = [
    "000",
    "001",
    "010",
    "011", 
    "100",
    "101",
    "110",
    "111"
]

grover = Grover(
    backend=backend,
    marked_states=marked_states
)

grover.run_grover()
