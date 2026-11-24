import numpy as np
for r in [1,2,3,5,10]:
 p,q=5*r+2,2*r+1
 A=np.array([[int(i!=j and q<=((j-i)%p)<=p-q) for j in range(p)] for i in range(p)],dtype=np.int64)
 # C_5 as the circular clique K_{5/2}: differences 2 and 3.
 f=[5*i//p for i in range(p)]
 hom=all((f[j]-f[i])%5 in (2,3) for i in range(p) for j in range(p) if A[i,j])
 print(dict(r=r,n=p,degree=int(A.sum(axis=1).min()),closed_walks_3=int(np.trace(np.linalg.matrix_power(A,3))),closed_walks_5=int(np.trace(np.linalg.matrix_power(A,5))),maps_to_C5=hom))