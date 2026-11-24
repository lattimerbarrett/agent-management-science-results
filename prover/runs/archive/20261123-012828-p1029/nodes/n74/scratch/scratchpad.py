import sympy as s
# Exact finite-dimensional Gram test; no trace identity is used to infer a
# quasitrace identity.  The example isolates the pinching-order pitfall.
p1=s.Matrix([[1,0],[0,0]])
p2=s.Matrix([[1,1],[1,1]])/2
P=s.diag(p1,p2)
V=p1.row_join(p2)
G=V.T*V
S=V*V.T
assert G*P==G and P*G==G
assert G[:2,:2]==p1 and G[2:,2:]==p2
assert (G-P).det() == 0
print('Gram eigenvalues:',G.eigenvals())
print('Diagonal pinching eigenvalues:',P.eigenvals())
print('G - pinching(G) eigenvalues:',(G-P).eigenvals())
print('rank G =',G.rank(),'; rank pinching(G) =',P.rank())
print('Nonzero spectra agree with S:',S.eigenvals())
print('\nFor an infinite Bessel family with tau(p_i)>=delta and S_N<=C:')
print('dim(supp(G_N))<=1, while dim(diag(p_i))>=N*delta.')
print('tau_N(G_N)=tau(S_N)<=C, but tau_N(diag(G_N))>=N*delta.')
print('Therefore diagonal pinching need not preserve or decrease quasitrace.')
print('The trace bound N*delta<=C would implicitly assume that false property.')
