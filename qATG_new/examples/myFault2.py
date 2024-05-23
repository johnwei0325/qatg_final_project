import numpy as np
import numpy as np
import qiskit.circuit.library as qGate
from qiskit.circuit.library import UnitaryGate

from qatg import QATG
from qatg import QATGFault

class myFault2(QATGFault):
	def __init__(self, param):
		super(myFault2, self).__init__(qGate.RXGate, 0, f"gateType: RZ, qubits: 0, param: {param}")
		self.param = param
	def createOriginalGate(self):
		return qGate.RZGate(self.param)
	def createFaultyGate(self, faultfreeGate):
		matrix = qGate.RZGate(self.param).to_matrix()
		# UF = qGate.UGate(0.05*np.pi, 0.05*np.pi, 0.05*np.pi)
		UF = qGate.RYGate(0.1*self.param)
		# matrix = np.matmul(np.kron(np.eye(2), UF), matrix)
		matrix = np.matmul(matrix, UF)
		return UnitaryGate(matrix) # bias fault
	

# generator = QATG(circuitSize = 1, basisSingleQubitGateSet = [qGate.UGate], circuitInitializedStates = {1: [1, 0]}, minRequiredStateFidelity = 0.1)
# configurationList = generator.createTestConfiguration([myFault2(np.pi)])

# for configuration in configurationList:
#     print(configuration)
#     configuration.circuit.draw('mpl')
# input()
