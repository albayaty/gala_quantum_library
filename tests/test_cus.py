from grover_controlled_diffuser import *
import pytest

def test_cus():
	qubits = [3, 4, 5, 6, 7]
	
	for qubit in qubits:
		assert num_CUs_gates(qubit) == (qubit*4) + 1
