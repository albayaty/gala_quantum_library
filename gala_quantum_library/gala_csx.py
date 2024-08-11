from qiskit import QuantumCircuit
import numpy as np

# ----------------------------------------------------------------------
# The n-bit controlled square-root of Pauli-X (X) gates of GALA-n:
# controlled-√X (as controlled-V) and controlled-√X† (as controlled-V†)
# ----------------------------------------------------------------------

def GALA_CSX(n, gate="CSX", as_block=False, statistics=False):
    """
    This function constructs the n-bit controlled square-root of X gates
    of GALA-n quantum library, where n >= 2 qubits.
    
    Parameters
    ----------
    n: the total number of qubits (n-1 controls and 1 target),
    gate: the name of an n-bit controlled square-root of X gate, as:
    "CSX" for the n-bit controlled-√X (controlled-V) gate as a default, and
    "CSXdg" for the n-bit controlled-√X† (controlled-V†) gate,
    as_block: construct a gate as a quantum circuit or a block, its default value is False, and
    statistics: print the final counts of H, RZ, and CX gates, as a final quantum cost.
    
    Returns
    -------
    The n-bit controlled square-root of X gate of GALA-n as a quantum circuit or a block.
    Note that the target qubit is the last indexed qubits in the n qubits.
    
    For more information, please read our GALA-n paper, 
    available at https://doi.org/10.48550/arXiv.2311.06760
    """
    
    # Consistency checking:
    gates = ["CSX", "CSXdg"]
    if gate not in gates:
	    print(f"\n⟩⟩⟩ ERROR: The '{gate}' gate is not supported by GALA_CSX()!")
	    print(f"⟩⟩⟩  INFO: GALA_CSX() only supports the gates: {gates}.\n")
	    return
    
    # The indices of n-1 controls and 1 target of a gate:
    controls = list(range(n-1))
    target = n-1
    
    theta = np.pi / 4
    
    # The n-bit controlled square-root of X gate of GALA-n:    
    GALA_gate = QuantumCircuit(n)
    
    GALA_gate.h( target )
    
    if (gate == "CSX"):
	    GALA_gate.rz( -theta, target )
    elif (gate == "CSXdg"):
	    GALA_gate.rz( theta, target )
    
    if (n == 2):
	    GALA_gate.cx( controls[-1], target )
    else:
	    GALA_gate.compose( GALA_Boolean(n, gate="AND", as_block=True), inplace=True )
    
    if (gate == "CSX"):
	    GALA_gate.rz( theta, target )
    elif (gate == "CSXdg"):
	    GALA_gate.rz( -theta, target )
    
    GALA_gate.h( target )
    
    if statistics:
	    print(f"\n⟩⟩⟩ Statistics (quantum cost) of {n}-bit {gate} gate (GALA-{n}):")
	    if (n == 2):
		    print(f"\t H gates = 2")
		    print(f"\tRZ gates = 2")
		    print(f"\tCX gates = 1")
	    else:
		    print(f"\t H gates = 4")
		    print(f"\tRZ gates = {(2**(n-1))+2}")
		    print(f"\tCX gates = {(2**(n-1))-1}\n")
    
    if as_block:
	    return GALA_gate.to_gate(label=gate+" gate\n\n(GALA-"+str(n)+")")
    else:
	    return GALA_gate
