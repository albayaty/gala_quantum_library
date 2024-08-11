# ----------------------------------------------------------------------
# The n-bit Fredkin gates of GALA-n:
# controlled-SWAP (CSWAP)
# ----------------------------------------------------------------------

def GALA_Fredkin(n, as_block=False, statistics=False):
    """
    This function constructs the n-bit Fredkin gate of GALA-n quantum library,
    where n >= 3 qubits.
    
    Parameters
	----------
    n: the total number of qubits (n-2 controls and 2 targets),
    as_block: construct a gate as a quantum circuit or a block, its default value is False, and
    statistics: print the final counts of H, RZ, and CX gates, as a final quantum cost.
    
    Returns
	-------
	The n-bit Fredkin gate of GALA-n as a quantum circuit or a block.
    Note that the target qubits are the last two indexed qubits in the n qubits.
    
    For more information, please read our GALA-n paper, 
    available at https://doi.org/10.48550/arXiv.2311.06760
    """
    
    # The indices of n-2 controls and 2 targets of a gate:
    controls = list(range(n-2))
    target1 = n-2
    target2 = n-1
    
    # The n-bit Fredkin gate of GALA-n:    
    GALA_gate = QuantumCircuit(n)
    
    GALA_gate.cx( target2, target1 )
    
    GALA_gate.compose( GALA_Boolean(n, gate="AND", as_block=True), inplace=True )
    
    GALA_gate.cx( target2, target1 )
    
    if statistics:
        print(f"\n⟩⟩⟩ Statistics (quantum cost) of {n}-bit Fredkin gate (GALA-{n}):")
        print(f"\t H gates = 2")
        print(f"\tRZ gates = {2**(n-1)}")
        print(f"\tCX gates = {(2**(n-1))+1}\n")
    
    if as_block:
        return GALA_gate.to_gate(label="Fredkin gate\n\n(GALA-"+str(n)+")")
    else:
        return GALA_gate
