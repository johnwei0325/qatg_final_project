import numpy as np
import qiskit.circuit.library as qGate
from qiskit.circuit.library import UnitaryGate, SXGate

from qatg import QATG
from qatg import QATGFault

class myFault1(QATGFault):
	def __init__(self, param):
		super(myFault1, self).__init__(qGate.RXGate, 0, f"gateType: SX, qubits: 0, param: {param}")
		self.param = param
	def createOriginalGate(self):
		return SXGate()
	def createFaultyGate(self, faultfreeGate):
		matrix = SXGate().to_matrix()
		# UF = qGate.UGate(0.05*np.pi, 0.05*np.pi, 0.05*np.pi)
		UF = qGate.RZGate(np.pi/20).to_matrix()
		# matrix = np.matmul(np.kron(np.eye(2), UF), matrix)
		matrix = np.matmul(UF,matrix)
		return UnitaryGate(matrix) # bias fault
	

# generator = QATG(circuitSize = 1, basisSingleQubitGateSet = [qGate.UGate], circuitInitializedStates = {1: [1, 0]}, minRequiredStateFidelity = 0.1)
# configurationList = generator.createTestConfiguration([myFault1(np.pi)])
# print("fuck")
# for configuration in configurationList:
#     print(configuration)
#     configuration.circuit.draw('mpl')
# input()