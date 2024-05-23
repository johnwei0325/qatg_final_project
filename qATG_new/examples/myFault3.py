import numpy as np
import qiskit.circuit.library as qGate
from qiskit.circuit.library import UnitaryGate
from qiskit import QuantumCircuit
from qatg import QATG
from qatg import QATGFault

class myFault3(QATGFault):
	def __init__(self):
		super(myFault3, self).__init__(qGate.CXGate, [0, 1], f"gateType: CX, qubits: 0-1")
	def createOriginalGate(self):
		return qGate.CXGate()
	def createFaultyGate(self, faultfreeGate):
		if not isinstance(faultfreeGate, qGate.CXGate):
			raise TypeError("what is this faultfreeGate")
		matrix = qGate.CXGate().to_matrix()
		UF1 = qGate.RXGate(0.1*np.pi)
		UF2 = qGate.RXGate(-0.1*np.pi)
		matrix = np.matmul(np.kron(np.eye(2), UF1), matrix)
		matrix = np.matmul(matrix, np.kron(UF2, np.eye(2)))
		# UnitaryGate(matrix).draw()
		return UnitaryGate(matrix)

# qc = QuantumCircuit(2)
# faulty_cx_gate = myCNOTFault().createFaultyGate(qGate.CXGate())
# qc.append(faulty_cx_gate, [0, 1])
# qc.draw('mpl')
# print(qc)
# generator = QATG(circuitSize = 2, basisSingleQubitGateSet = [qGate.UGate], circuitInitializedStates = {2: [1, 0, 0, 0]}, minRequiredStateFidelity = 0.1)
# configurationList = generator.createTestConfiguration([myFault3()])


# for configuration in configurationList:
#     print(configuration)
#     configuration.circuit.draw('mpl')
# input()
