from qiskit import QuantumCircuit
import numpy as np

# ----------------------------------------------------------------------
# The n-bit Boolean gates of GALA-n:
# AND, NAND, OR, NOR, Implication (IMP), and Inhibition (INH)
# ----------------------------------------------------------------------

def GALA_Boolean(n, gate="AND", as_block=False, statistics=False):
    """
    This function constructs the n-bit Boolean gates of GALA-n quantum library, where n >= 3 qubits.
    
    Parameters
    ----------
    n: the total number of qubits (n-1 controls and 1 target),
    gate: the name of an n-bit Boolean gate:
    "AND" as the default gate, "NAND", "OR", "NOR",
    "IMP" as the implication, and "INH" as the inhibition,
    as_block: construct a gate as a quantum circuit or a block, its default value is False, and
    statistics: print the final counts of H, RZ, and CX gates, as a final quantum cost.
    
    Returns
    -------
    The n-bit Boolean gate of GALA-n as a quantum circuit or a block.
    Note that the target qubit is the last indexed qubits in the n qubits.
    
    For more information, please check "Algorithm 1" in our GALA-n
    paper, available at https://doi.org/10.48550/arXiv.2311.06760
    """
    
    # Consistency checking:
    gates = ["AND", "NAND", "OR", "NOR", "IMP", "INH"]
    if gate not in gates:
	    print(f"\n⟩⟩⟩ ERROR: The '{gate}' gate is not supported by GALA_Boolean()!")
	    print(f"⟩⟩⟩  INFO: GALA_Boolean() only supports the gates: {gates}.\n")
	    return
    
    # The indices of n-1 controls and 1 target of a gate:
    controls = list(range(n-1))
    target = n-1
    
    # The core rotational angles of RZ gates:
    theta = np.pi / 2**(n-1)
    
    # The n-bit Boolean gate of GALA-n:    
    GALA_gate = QuantumCircuit(n)
    
    # Add SP1 to the target qubit:
    GALA_gate.h( target )
    
    # Add AX1 to the target qubit:
    #GALA_gate.id( target )
    
    # Construct Core3 (theta), i.e., the core of 3-bit Boolean gate of GALA-n:    
    core = QuantumCircuit(n)
    
    if (gate == "OR") or (gate == "NOR"):
	    core.rz( theta, target )
    else:
	    # For all remaining 3-bit Boolean gates of GALA-n:
	    core.rz( -theta, target )
    
    core.cx( controls[-1], target )
    
    if (gate == "IMP") or (gate == "INH"):
	    core.rz( -theta, target )
    else:
	    # For all remaining 3-bit Boolean gates of GALA-n:
	    core.rz( theta, target )
    
    core.cx( controls[-2], target )
    
    if (gate == "AND") or (gate == "NAND"):
	    core.rz( -theta, target )
    else:
	    # For all remaining 3-bit Boolean gates of GALA-n:
	    core.rz( theta, target )
    
    core.cx( controls[-1], target )
    
    # For all 3-bit Boolean gates of GALA-n:
    core.rz( theta, target )
    # End of Core3 (theta) construction
    
    # Calculate the remaining control qubits:
    r = n - 3
    
    # Construct Core-n (theta), i.e., the core of n-bit Boolean gate of GALA-n:    
    while (r > 0):
	    snapshot = core.copy()
	    core.cx( controls[r-n], target )
	    core.compose( snapshot, inplace=True )
	    r = r - 1
    
    GALA_gate.compose(core, inplace=True)
    
    # Add AX2 to the target qubit:
    if (gate == "NAND") or (gate == "IMP"):
	    GALA_gate.rz( -np.pi, target )
    elif (gate == "OR"):
	    GALA_gate.rz( np.pi, target )
    
    # Add SP2 to the target qubit:
    GALA_gate.h( target )
    
    if statistics:
	    print(f"\n⟩⟩⟩ Statistics (quantum cost) of {n}-bit {gate} gate (GALA-{n}):")
	    print(f"\t H gates = 2")
	    if (gate == "NAND") or (gate == "OR") or (gate == "IMP"):
		    print(f"\tRZ gates = {(2**(n-1))+1}")
	    else:
		    print(f"\tRZ gates = {2**(n-1)}")
	    print(f"\tCX gates = {(2**(n-1))-1}\n")
    
    if as_block:
	    return GALA_gate.to_gate(label=gate+" gate\n\n(GALA-"+str(n)+")")
    else:
	    return GALA_gate
