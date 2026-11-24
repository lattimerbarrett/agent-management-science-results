import sympy as s
from itertools import combinations

J = s.zeros(6)
for i in (0,2,4):
    J[i,i+1], J[i+1,i] = 1,-1
assert J.rank() == 6
assert s.binomial(5,2)-1 == 9 < 2*5

# Symbolic universal form of a bivector in U wedge V, dim U=2.
a = s.symbols('a')
B = s.Matrix(2,4,s.symbols('b:8'))
A = s.Matrix([[0,a],[-a,0]])
K = A.row_join(B).col_join((-B.T).row_join(s.zeros(4)))
K1 = A.row_join(B).col_join(s.zeros(4,6))
K2 = s.zeros(2,6).col_join((-B.T).row_join(s.zeros(4)))
assert K == K1+K2
assert K1.rank() == K2.rank() == 2
# Thus rank(K)<=4, incompatible with rank(J)=6, in any basis.

# Restriction splitting: Q|line has one positive and four zero summands.
q = [1,0,0,0,0]
f = sorted([q[i]+q[j] for i,j in combinations(range(5),2)], reverse=True)
assert f == [1]*4+[0]*6
f.remove(0) # quotient by section with nonzero constant component
assert f == [1]*4+[0]*5

# For coordinate U, the quotient V/U is represented by complementary indices.
def plane_dual_sections(U):
    W = [i for i in range(6) if i not in U]
    restriction = J.extract(W,W)
    # H0(F*|P(U)) has dimension choose(3,2)=3.
    return 3-int(restriction != s.zeros(3)), restriction.rank()

h0, rank0 = plane_dual_sections([0,2,4])
h1, rank1 = plane_dual_sections([0,1,2])
assert (h0,h1) == (3,2)
assert (rank0,rank1) == (0,2)
print({'rank_E':len(f), 'line_splitting':f,
       'plane_h0_Edual':(h0,h1), 'quotient_bivector_ranks':(rank0,rank1)})
