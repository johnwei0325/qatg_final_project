# import benchmarks
# import sys
# sys.path.append('../examples')
# import sys
# sys.path.insert(0,"../examples")

from qatg import QATGFault
from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator
import numpy as np
import qiskit.circuit.library as qGate
from qiskit.circuit.library import UnitaryGate, SXGate
from qiskit import transpile
from collections import defaultdict

from qatg import QATG
import sys
import os.path as osp
sys.path.append(osp.dirname(osp.abspath(__file__)))
from examples import myFault1
from examples import myFault2
from examples import myFault3

def fault_simulation(fault_model, qc, shot):
    ### Fault simulation ###
    faulty_qc = qc.copy()   
    # faulty_qc = fault_model(faulty_qc)
    print(faulty_qc)
    for gate in faulty_qc.data:
        if isinstance(gate[0], fault_model.createOriginalGate().__class__):
            faulty_gate = fault_model.createFaultyGate(gate[0])
            faulty_qc.data[faulty_qc.data.index(gate)] = (faulty_gate, gate[1], gate[2])
    print(faulty_qc)
    simulator = AerSimulator()
    new_c = transpile(faulty_qc, simulator)
    # result = execute(faulty_qc, backend=simulator, shots=shots).result()
    result = simulator.run(new_c, shots=shot).result()
    result_counts = result.get_counts(faulty_qc)
    return result_counts

def simulation(qc, shot):
    simulator = AerSimulator()
    new_c = transpile(qc, simulator)
    # result = execute(faulty_qc, backend=simulator, shots=shots).result()
    result = simulator.run(new_c, shots=shot).result()
    result_counts = result.get_counts(qc)
    return result_counts

def cal_chi_square(observed, expected):
    # Total counts in observed and expected
    R_obs = sum(observed.values())
    R_exp = sum(expected.values())

    # Compute the expected counts for each category
    # Normalize expected values to match the total count of observed values
    normalized_expected = {key: (value / R_exp) * R_obs for key, value in expected.items()}

    # Ensure all categories in observed are in the normalized expected
    for key in observed:
        if key not in normalized_expected:
            normalized_expected[key] = 0

    # Compute chi-squared value
    for key in normalized_expected:
        if key not in observed:
            observed[key] = 0
    
    chi_squared = 0
    for key in observed:
        if normalized_expected[key] > 0:  # Only include terms where the expected count is greater than 0
            chi_squared += ((observed[key] - normalized_expected[key]) ** 2) / normalized_expected[key]
    chi_squared = np.sqrt(chi_squared)
    
    return chi_squared

if __name__ == '__main__':
    qc = QuantumCircuit.from_qasm_file("benchmarks/qc2.qasm")
    # print(qc)
    observed = fault_simulation(myFault1(np.pi), qc, 100000)
    expected = simulation(qc, 100000)
    print("observed: ", observed)
    print("expected: ", expected)
    generator = QATG(circuitSize = 1, basisSingleQubitGateSet = [qGate.UGate], circuitInitializedStates = {1: [1, 0]}, minRequiredStateFidelity = 0.1)
    configurationList = generator.createTestConfiguration([myFault2(np.pi)])
    boundary = 0
    repetition = 0
    for configuration in configurationList:
        repetition, boundary = configuration.calRepetition()
        print(configuration)
        configuration.circuit.draw('mpl')
        chi_squared = cal_chi_square(observed, expected)
        print(f"Chi-squared value: {chi_squared}")

        if chi_squared > boundary:
            print("PASS!!!")
        else :
            print("FAILED!!!")
    # input()
   
