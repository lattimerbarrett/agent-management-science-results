import sympy as S
n,k=S.symbols('n k', nonzero=True)
for ell in range(9):
    cO=S.prod(n/k+j for j in range(ell))/S.factorial(ell)
    cA=S.prod(n/k-1+j for j in range(ell))/S.factorial(ell)
    assert S.cancel((n+ell*k-k)*cA-(n-k)*cO)==0
cases=0
for g in range(2,101):
    r=(g+2)//3; K=g-r; d=2*g-2
    assert K<d and K>=2*r-2 and 3*K>=d and 4*K>d
    gaps=list(range(1,2*g,2))
    q=[2*g-1-2*j for j in range(r)]
    assert set(h for h in gaps if h>2*K)==set(q)
    assert min(q)>K
    assert (3*K==d)==(g%3==1)
    for m in range(r):
        b=S.symbols('b:'+str(m+1))
        H=S.Matrix(r,K//2+1,lambda j,a:b[j+a] if j+a<=m else 0)
        # Reverse the first m+1 columns: triangular with diagonal b_m.
        J=H[:m+1,:m+1][:,::-1]
        assert all(J[i,i]==b[m] for i in range(m+1))
        assert all(J[i,j]==0 for i in range(m+1) for j in range(i))
        assert all(H[j,a]==0 for j in range(r) for a in range(K//2+1) if j>m or a>m)
        for a in range(m+1,K//2+1):
            for j in range(m+1):
                pole=2*g-1-2*j+2*a
                Q=a-j-1
                assert Q>=0 and pole==2*g+1+2*Q
                assert 4*g+2-pole>0
        cases+=1
print('Symbolic divergence identities: 9')
print('All-coefficient symbolic cases:',cases)
