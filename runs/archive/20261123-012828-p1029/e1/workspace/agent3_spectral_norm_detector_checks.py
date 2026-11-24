"""Exact finite-dimensional checks of the spectral-compression detector."""
import random
import sympy as S
rng=random.Random(276)
r=S.symbols('r', positive=True)
n=S.symbols('n', positive=True)
f=r*n**2/(n*r+1)**2
assert S.simplify(S.diff(f,n)-2*n*r/(n*r+1)**3)==0
assert S.simplify(1-r*f-(2*n*r+1)/(n*r+1)**2)==0
assert S.limit(f,n,S.oo)==1/r
assert S.limit(f,r,0,dir='+')==0
count=0
for dim in range(2,9):
    for trial in range(12):
        v=S.Matrix([rng.randint(-3,3) for _ in range(dim)])
        if v.dot(v)==0: v[0]=1
        U=S.eye(dim)-2*v*v.T/v.dot(v)
        assert U.T*U==S.eye(dim)
        eigen=[S.Rational(j+1,dim+1) for j in range(dim)]
        D=S.diag(*eigen)
        # Earliest nonzero diagonal of C is prescribed; C=G G^T/scale.
        first=rng.randrange(dim)
        G=S.zeros(dim,2)
        for j in range(first,dim):
            for k in range(2): G[j,k]=rng.randint(-2,2)
        G[first,0]=1
        C=G*G.T/S.Integer(100*dim)
        a=U*D*U.T
        c=U*C*U.T
        b=a+c
        assert c==U*G*(U*G).T/S.Integer(100*dim)
        cutoff=(eigen[first]+(eigen[first+1] if first+1<dim else eigen[first]+1))/2
        Q=S.diag(*[int(bool(x<cutoff)) for x in eigen])
        q=U*Q*U.T
        assert q*q==q and q.T==q
        assert a*q==q*a
        assert all((x<cutoff)==bool(Q[j,j]) for j,x in enumerate(eigen))
        # q a q has norm eigen[first], from its explicit diagonal form.
        assert q*a*q==U*(Q*D*Q)*U.T
        assert max([eigen[j] for j in range(dim) if Q[j,j]])==eigen[first]
        w=U[:,first]
        assert (w.T*w)[0]==1 and q*w==w
        gain=S.simplify((w.T*q*b*q*w)[0]-eigen[first])
        assert gain==C[first,first] and gain>0
        count+=1
print('PASS:',count,'exact rational matrix strictness certificates; 4 symbolic regularizer identities')
