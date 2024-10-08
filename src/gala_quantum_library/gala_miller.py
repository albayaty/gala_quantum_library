from qiskit import QuantumCircuit
from gala_quantum_library import *

# ----------------------------------------------------------------------
# The n-bit Miller gates of GALA-n:
# quantum distance gates
# ----------------------------------------------------------------------

def GALA_Miller(n, as_block=False, statistics=False):
    """
    This function constructs the n-bit Miller gate of GALA-n quantum library, where n >= 3 qubits.
    
    Parameters
    ----------
    n: the total number of qubits (n-1 controls and 1 target),
    as_block: construct a gate as a quantum circuit or a block, its default value is False, and
    statistics: print the final counts of H, RZ, and CX gates, as a final quantum cost.
    
    Returns
    -------
    The n-bit Miller gate of GALA-n as a quantum circuit or a block.
    Note that this gate has n output qubits.
    
    For more information, please read our GALA-n paper, 
    available at https://doi.org/10.48550/arXiv.2311.06760
    """
    
    # Consistency checking:
    if (n < 3):
	    print(f"\n⟩⟩⟩ ERROR: GALA_Miller() should have more than {n} qubits!")
	    print(f"⟩⟩⟩  INFO: GALA_Miller() has n qubits (n-1 controls + 1 target), where n >= 3.\n")
	    return
    
    # The indices of n-1 controls and 1 target of a gate:
    controls = list(range(n-1))
    target = n-1
    
    # The n-bit Miller gate of GALA-n:
    GALA_gate = QuantumCircuit(n)
    
    GALA_gate.cx( target, controls )
    
    GALA_gate.compose( GALA_Boolean(n, gate="AND", as_block=True), inplace=True )
    
    controls.reverse()
    
    GALA_gate.cx( target, controls )
    
    if statistics:
	    print(f"\n⟩⟩⟩ Statistics (quantum cost) of {n}-bit Miller gate (GALA-{n}):")
	    print(f"\t H gates = 2")
	    print(f"\tRZ gates = {2**(n-1)}")
	    print(f"\tCX gates = {(2**(n-1))-1+((n-1)*2)}\n")
    
    if as_block:
	    return GALA_gate.to_gate(label="Miller gate\n\n(GALA-"+str(n)+")")
    else:
	    return GALA_gate


# ----------------------------------------------------------------------
# Counting the number of gates of GALA_Miller():
# ----------------------------------------------------------------------

def num_gates_GALA_Miller(n):
    """
    This function counts the number of gates of GALA_Miller().
    
    Parameters
    ----------
    n: the number of qubits (n-1 controls and 1 target), where n >= 3.
    
    Returns
    -------
    The number of gates of GALA_Miller().
    """
    
    # Consistency checking:
    if (n < 3):
	    print(f"\n⟩⟩⟩ ERROR: GALA_Miller() should have more than {n} qubits!")
	    print(f"⟩⟩⟩  INFO: GALA_Miller() has n qubits (n-1 controls + 1 target), where n >= 3.\n")
	    return
    
    H = 2
    RZ = 2**(n-1)
    CX = (2**(n-1))-1+((n-1)*2)
    
    gates = H + RZ + CX
    
    return gates
