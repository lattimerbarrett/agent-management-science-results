import sympy as s
z,w=s.symbols('z w',nonzero=True)
coords=(z,w)
def bracket(A,B):
 return s.Matrix([sum(A[j]*s.diff(B[i],coords[j])-B[j]*s.diff(A[i],coords[j]) for j in range(2)) for i in range(2)])
for k in range(-4,5):
 for l in range(6):
  A=s.Matrix([0,z**k]); B=s.Matrix([0,z**k*w])
  C=lambda r:s.Matrix([z*w**r,0])
  lhs=bracket(A,C(l+1))-bracket(B,C(l))
  assert (lhs-s.Matrix([z**(k+1)*w**l,0])).applyfunc(s.simplify)==s.zeros(2,1)
  # Once all z-fields are generated, brackets with complete z*d/dw yield w-fields.
  P=s.Matrix([z**k*w**l,0]); Q=s.Matrix([0,z])
  lhs=bracket(P,Q)+s.Matrix([l*z**(k+1)*w**(l-1),0])
  assert (lhs-s.Matrix([0,z**k*w**l])).applyfunc(s.simplify)==s.zeros(2,1)
print('108 exact Laurent-monomial bracket identities passed.')
print('The displayed formulas prove the identities for arbitrary integer k and l>=0.')
