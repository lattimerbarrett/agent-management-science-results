import sympy as sp
for N in range(2,25):
    T=sp.zeros(N)
    for k in range(1,N):
        T[k,k-1]=sp.sqrt(1-sp.Rational(k,N))
    P=sp.zeros(N);P[0,0]=1
    D=T.T*T-T*T.T
    assert D==P-sp.eye(N)/N
    assert D[0,0]==1-sp.Rational(1,N)
    # Correct diagonal formula: first 1-1/N; all remaining -1/N.
    assert max(abs(x) for x in D-P)==sp.Rational(1,N)
    for m in range(1,min(N,8)+1):
        copies=[]
        for j in range(m):
            v=sp.zeros(N);v[j,0]=1
            assert v.T*v==P
            copies.append(v*v.T)
        S=sum(copies,sp.zeros(N))
        assert S*S==S
print('23 exact weighted-shift commutator checks and orthogonal-copy certificates passed.')
