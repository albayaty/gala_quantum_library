from gala_quantum_library import *
import pytest

def test_gala():
	qubits = [3, 4, 5]
	
	for n in qubits:
		assert num_gates_GALA_Boolean(n) == 2 + 2**(n-1) + (2**(n-1))-1		
		assert num_gates_GALA_Fredkin(n) == 2 + 2**(n-1) + (2**(n-1))+1
		assert num_gates_GALA_Miller(n) == 2 + 2**(n-1) + (2**(n-1))-1+((n-1)*2)
		assert num_gates_GALA_CSX(n) == 4 + (2**(n-1))+2 + (2**(n-1))-1
