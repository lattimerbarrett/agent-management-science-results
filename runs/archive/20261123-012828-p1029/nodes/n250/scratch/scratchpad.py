import sympy as s
# Bookkeeping for residual/overlapping-corner recursion, supplied by the
# verified defect-amplification lemma, not a construction of its maps.
r0,r1,r2,r3,d,delta=s.symbols('r0 r1 r2 r3 d delta', real=True)
bs=[r0-r1,r1-r2,r2-r3]
assert s.simplify(sum(bs)-(r0-r3))==0
print('Residual recursion: sum of first three increments =',s.expand(sum(bs)))
print('If 0<=r_(n+1)<=r_n<=1, every partial sum stays <=1.')
print('If each step uses an overlapping corner of fixed dimension d,')
print('the ambient increment lower bound is',d*delta,'at every step, not d**n*delta.')
print('This bookkeeping does not by itself determine whether the increasing sequence has a supremum in the original algebra.')
