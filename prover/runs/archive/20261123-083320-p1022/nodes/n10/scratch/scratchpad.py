import sympy as s
# A nondegenerate bivector on a six-dimensional vector space.
N=6
J=s.zeros(N)
for i in range(0,N,2):
    J[i,i+1]=1
    J[i+1,i]=-1
# Infinitesimal GL(V) orbit of the projective class of J.
pairs=[(i,j) for i in range(N) for j in range(i+1,N)]
cols=[]
for a in range(N):
    for b in range(N):
        X=s.zeros(N); X[a,b]=1
        Y=X*J+J*X.T
        cols.append(s.Matrix([Y[i,j] for i,j in pairs]))
M=s.Matrix.hstack(*cols)
v=s.Matrix([J[i,j] for i,j in pairs])
print('rank of bivector:',J.rank())
print('rank of bundle: binomial(5,2)-1 =',s.binomial(5,2)-1)
print('line splitting: O(1)^4 + O^5')
print('dimension of orbit in projective bivectors:',M.row_join(v).rank()-1)
print('dimension of projective stabilizer:',35-(M.row_join(v).rank()-1))
