from fractions import Fraction
from math import prod

# Exact two-form feasibility on 24 moment-curve points in R^9.
# Six measures each have four consecutive equally weighted atoms.
j = 6
colors = []
state = (0, 0)
for block in range(j):
    flips = [1, 0, 1] if block < 3 else [0, 1, 0]
    group = [state]
    for bit in flips:
        state = tuple((v ^ 1) if k == bit else v for k, v in enumerate(state))
        group.append(state)
    colors.extend(group)
roots = [[Fraction(2*i+3, 2) for i in range(23)
          if colors[i][b] != colors[i+1][b]] for b in range(2)]
print('Degrees of the two affine forms along the moment curve:', list(map(len, roots)))
for b in range(2):
    vals = [prod(Fraction(t)-r for r in roots[b]) for t in range(1, 25)]
    signs = [int(v > 0) for v in vals]
    assert all(signs[i] ^ signs[0] == colors[i][b] ^ colors[0][b] for i in range(24))
    assert all(v != 0 for v in vals)
for block in range(j):
    assert len(set(colors[4*block:4*block+4])) == 4
print('All six measures have exactly one atom in each open quadrant.')
print('All evaluations are nonzero: sufficiently small smoothings remain feasible.')

# A warning for finite-support tests: an atom on both hyperplanes can split.
# A radially symmetric smoothing of delta_0 in R^2 has quarter mass in each
# quadrant of the coordinate axes, although a single unsplit atom cannot.
print('Boundary check: delta_0 admits no strict four-way atomic coloring,')
print('but every radially symmetric smoothing is quartered by the coordinate axes.')
