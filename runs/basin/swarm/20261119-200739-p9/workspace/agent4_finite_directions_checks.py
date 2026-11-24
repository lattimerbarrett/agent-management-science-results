import numpy as np
from pathlib import Path
rng=np.random.default_rng(6519)
angles=np.array([0.,np.pi/3,2*np.pi/3])
vs=[np.array([np.cos(t),np.sin(t)]) for t in angles]
c=min(abs(np.sin(x-y)) for i,x in enumerate(angles) for j,y in enumerate(angles) if i!=j)
max_ratio=0.
for trial in range(300):
    typ=rng.integers(0,3,size=8)
    lam=np.exp(rng.uniform(0,5,size=8))
    prob=rng.dirichlet(np.ones(8))
    for p in [1.3,1.7,2.,2.5,3.,5.]:
        roots=[]; scalars=[]
        for k in range(8):
            v=vs[typ[k]]; P=np.outer(v,v); Q=np.eye(2)-P
            roots.append(lam[k]**(1/p)*P+lam[k]**(-1/p)*Q)
        K=np.array([[np.linalg.norm(X@np.linalg.inv(Y),2) for Y in roots] for X in roots])
        for j in range(3):
            w=np.where(typ==j,lam,1/lam)
            rr=(w[:,None]/w[None,:])**(1/p)/K
            # For distinct terminal directions, a rank-one compression supplies c.
            assert np.max(rr)<=1/c+1e-9
            max_ratio=max(max_ratio,np.max(rr))
            q=p/(p-1)
            CA=np.dot(prob,(K**q@prob)**(p-1))
            Cs=np.dot(prob,w)*np.dot(prob,w**(-1/(p-1)))**(p-1)
            assert Cs<=CA/c**p*(1+1e-8)
print('300 actual atomic weights x6 p values x3 scalarizations passed.')
print('Largest pointwise scalar/root-kernel ratio:',max_ratio,'allowed',1/c)
Path('workspace/agent4_finite_directions_checks.py').write_text(Path(__file__).read_text())
Path('workspace/agent4_finite_directions.md').write_text(r'''# Fixed separated terminal directions give only scalar exponents

Suppose W(x)=lambda(x)P_{j(x)}+lambda(x)^(-1)(I-P_{j(x)}),
where lambda>=1 and P_j=v_j v_j* are a fixed finite family of real
rank-one projections, spanning R^2, with pairwise angle sine>=c>0.
Constants below may depend on p, the number of directions, and c.
Define w_j(x)=lambda(x) if j(x)=j, and lambda(x)^(-1) otherwise.
Then pointwise, for every f,

 |W^(1/p) f|^p is comparable to sum_j w_j |v_j*f|^p.

Indeed at type k the first term controls lambda |v_k*f|^p, while
the other terms together control lambda^(-1) times the transverse
component, since the family spans with quantitative separation.
The remaining contributions are absorbed by the same two terms.

Moreover

 (w_j(x)/w_j(y))^(1/p) <= C_c ||W(x)^(1/p)W(y)^(-1/p)||.

If x,y are both type j this is immediate; if neither is type j,
use the root's two singular values or the Hilbert--Schmidt expansion
to control (lambda_y/lambda_x)^(1/p). If x has type j and y a
different type k, compress the product between the top eigendirection
at x and the bottom eigendirection at y: its norm is at least
(lambda_x lambda_y)^(1/p)|sin(angle(v_j,v_k))|.
The opposite type assignment gives scalar ratio<=1, whereas the
matrix product has determinant one and hence norm>=1.
Thus [w_j]Ap<=C_c^p [W]Ap, with the question's exact mixed definition.
Apply the scalar Hilbert bound to each scalar weighted projection,
sum the p-th powers, and use pointwise norm comparability. This yields

 ||H||Lp(W) <= C_{p,N,c} [W]Ap^max(1,1/(p-1)).

Consequently a sharp genuinely matrix lower example cannot use a
uniformly separated fixed finite family of terminal eigendirections.
It must have degenerating angular separation, an increasing number
of directions, or another parameter-dependent degeneracy.
This does not exclude finitely many Q-dependent directions, since
C_{p,N,c} may then itself grow with Q.
''')
