import sympy as s
# A finite-dimensional check of the row-Gram construction, not a proof
# of quasitracial exhaustion.
b0=s.eye(2)/3; b1=s.eye(2)/3
R=(s.eye(2)/s.sqrt(3)).row_join(s.eye(2)/s.sqrt(3))
G=R.T*R
print('RR* equals b0+b1:', s.simplify(R*R.T-b0-b1)==s.zeros(2))
print('Diagonal Gram blocks are the increments:', G[:2,:2]==b0 and G[2:,2:]==b1)
print('rank of row Gram:',G.rank())
print('rank of diagonal pinching:',s.diag(b0,b1).rank())
print('spectra of sum:',(b0+b1).eigenvals())
print('This checks row identities only; it provides no bound for a nonadditive quasitrace on the pinching.')