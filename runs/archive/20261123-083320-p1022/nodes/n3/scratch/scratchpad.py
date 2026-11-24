import sympy as s
# Basis e1,f1,e2,f2,e3,f3; bivector e1^f1+e2^f2+e3^f3.
B=s.zeros(6)
for i in range(3):
    B[2*i,2*i+1]=1
    B[2*i+1,2*i]=-1
for name,U in [('Lagrangian',(0,2,4)),('non-Lagrangian',(0,1,2))]:
    keep=[i for i in range(6) if i not in U]
    projected=B.extract(keep,keep)
    nonzero=projected != s.zeros(3)
    print(name, 'projected bivector =',projected.tolist(),
          'h^0(E^* restricted to plane) =', 3-int(nonzero))
print('Line splitting: O(1)^4 + O^5, rank 9 < 2*5.')
