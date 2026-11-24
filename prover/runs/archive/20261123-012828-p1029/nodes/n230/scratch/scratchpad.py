# Check the logical use of the supplied verified result.
from itertools import product
# C: order bounds and constant positive quasitrace increments hold.
# L: the sequence has a least upper bound.
# The verified theorem says C => L; a witness requires C and not L.
models=[]
for C,L in product([False,True],repeat=2):
    verified=(not C) or L
    witness=C and not L
    if verified and witness:
        models.append((C,L))
print('Witnesses consistent with the verified supremum theorem:',models)
print('The theorem does not rule out C and L:', (not True) or True)
