# Record the exact obstruction without assuming that its kernel is all torsion.
import sympy as sp
# A homomorphism to a torsion-free group can have a non-torsion kernel.
M = sp.Matrix([[1, 0]])
print('Example map Z^2 -> Z:', M)
print('Kernel basis:', M.nullspace())
print('Thus torsion implies a kernel, but the converse needs a separate theorem.')