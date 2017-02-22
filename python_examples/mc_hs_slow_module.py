#!/usr/bin/env python3
"""Energy and move routines for MC simulation, LJ potential.

Slow version using Python loop.
"""

def introduction():
    """Prints out introductory statements at start of run."""

    print('Hard sphere potential')
    print('Diameter, sigma = 1')
    print('Energy, kT = 1')
    print('Slow version built around Python loops')

def conclusion():
    """Prints out concluding statements at end of run."""

    print('Program ends')

def overlap ( box, r ):
    """Takes in box and coordinate array, and signals any overlap."""

    # Actual calculation is performed by function overlap_1

    n, d = r.shape
    assert d==3, 'Dimension error for r in overlap'

    for i in range(n-1):
        if overlap_1 ( r[i,:], box, r[i+1:,:] ):
            return True # Immediate return on detection of overlap

    return False

def overlap_1 ( ri, box, r ):
    """Takes in coordinates of an atom and signals any overlap.

    Values of box and partner coordinate array are supplied.
    """

    import numpy as np

    # In general, r will be a subset of the complete set of simulation coordinates
    # and none of its rows should be identical to ri

    # It is assumed that positions are in units where box = 1

    nj, d = r.shape
    assert d==3, 'Dimension error for r in overlap_1'
    assert ri.size==3, 'Dimension error for ri in overlap_1'

    inv_box_sq = 1.0 / box ** 2

    for rj in r:
        rij = ri - rj            # Separation vector
        rij = rij - np.rint(rij) # Periodic boundary conditions in box=1 units
        rij_sq = np.sum(rij**2)  # Squared separation

        if rij_sq < inv_box_sq: # Check within cutoff
            return True # Immediate return on detection of overlap

    return False

def n_overlap ( box, r ):
    """Takes in box and coordinate array, and counts overlaps."""

    # This routine is used in the calculation of pressure
    # Actual calculation is performed by function n_overlap_1

    n, d = r.shape
    assert d==3, 'Dimension error for r in n_overlap'

    n_ovr = 0 # Initialize

    for i in range(n-1):
        n_ovr = n_ovr + n_overlap_1 ( r[i,:], box, r[i+1:,:] )

    return n_ovr

def n_overlap_1 ( ri, box, r ):
    """Takes in coordinates of an atom and counts overlaps.

    Values of box and partner coordinate array are supplied.
    """

    import numpy as np

    # In general, r will be a subset of the complete set of simulation coordinates
    # and none of its rows should be identical to ri

    # It is assumed that positions are in units where box = 1

    nj, d = r.shape
    assert d==3, 'Dimension error for r in overlap_1'
    assert ri.size==3, 'Dimension error for ri in overlap_1'

    inv_box_sq = 1.0 / box ** 2

    n_ovr = 0 # Initialize

    for rj in r:
        rij = ri - rj            # Separation vector
        rij = rij - np.rint(rij) # Periodic boundary conditions in box=1 units
        rij_sq = np.sum(rij**2)  # Squared separation

        if rij_sq < inv_box_sq: # Check within cutoff
            n_ovr = n_ovr + 1

    return n_ovr
