import sympy as S

def op(nodes,w,s):
    V=S.Matrix([[x**j for j in range(s)] for x in nodes]); M=V.T*S.diag(*w)*V
    coeff=-M.inv()*V.T*S.Matrix([wi*x**s for x,wi in zip(nodes,w)])
    q=[x**s+sum(coeff[j]*x**j for j in range(s)) for x in nodes]
    H2=S.factor(sum(wi*qi**2 for wi,qi in zip(w,q)))
    return q,H2

for s in range(1,7):
    n=s+2;nodes=list(map(S.Integer,range(1,n+1)));w=[S.Rational(i*i+1,sum(j*j+1 for j in range(1,n+1))) for i in range(1,n+1)]
    c=[1/S.prod(x-y for y in nodes if y!=x) for x in nodes]
    q,H2=op(nodes,w,s)
    z=[S.factor(wi*qi**2/H2) for wi,qi in zip(w,q)]
    Q,Hnext2=op(nodes,z,s)
    t=sum(ci*ci*x/wi for ci,x,wi in zip(c,nodes,w))/sum(ci*ci/wi for ci,wi in zip(c,w))
    tnext=sum(ci*ci*x/zi for ci,x,zi in zip(c,nodes,z))/sum(ci*ci/zi for ci,zi in zip(c,z))
    f=[x-t for x in nodes];fn=[x-tnext for x in nodes]
    for i in range(n):
        assert S.simplify(w[i]*q[i]-H2*c[i]*f[i])==0
        assert S.simplify(q[i]*Q[i]*f[i]-Hnext2*fn[i])==0
    print('s=',s,'barycentric duality and signed two-step multiplier identity verified.')

# Exact scalar same-gap root ordering for two opposing directions.
nu=[S.Rational(1,4)]*4;nodes=list(map(S.Integer,[-3,-1,1,3]));t=S.Integer(0)
for c in [S.Rational(-1,2),S.Rational(1,2)]:
    weights=[wi*(x-t)**2/(x-c)**2 for x,wi in zip(nodes,nu)]
    h=sum(x*wi for x,wi in zip(nodes,weights))/sum(weights)
    assert (h-c)*(c-t)>0
print('Scalar same-gap root ordering checked in both directions.')
