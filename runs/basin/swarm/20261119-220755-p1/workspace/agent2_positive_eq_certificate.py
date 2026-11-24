"""Rigorous interval certificate of a positive normal-form equilibrium (not yet a counterexample)."""
import sympy as sp
from sage.all import RealIntervalField, matrix, vector
R=RealIntervalField(300)
x=sp.symbols('x');nodes=[-3,-1,0,1,2,3]
N=sp.Rational(2,5);P=sp.prod(x-a for a in nodes);Q=(x+sp.Rational(4,5))*(x-sp.Rational(17,10));F=sp.Poly(sp.expand(P*Q+N),x)
def ri(q):
    q=sp.Rational(q);return R(int(q.p))/int(q.q)
def roots(poly):
    pairs=sp.Poly(poly,x).intervals(eps=sp.Rational(1,10**90))
    assert len(pairs)==8 and all(k==1 for I,k in pairs)
    return [R(ri(I[0]).lower(),ri(I[1]).upper()) for I,k in pairs]
a=roots(F.as_expr());b=roots(F.as_expr()+N)
def fromroots(rs):
    c=[R(1)]
    for z in rs:
        cc=[R(0)]*(len(c)+1)
        for j,v in enumerate(c):cc[j]-=z*v;cc[j+1]+=v
        c=cc
    return c
def val(c,z):
    ans=R(0)
    for v in c[::-1]:ans=ans*z+v
    return ans
f=fromroots([a[i] for i in [0,3,5,6]]);g=fromroots([a[i] for i in [1,2,4,7]])
mu=[b[1],b[6]];NN=ri(N);ds=[sp.prod(a-z for z in nodes if a!=z) for a in nodes]
V=matrix(R,[[R(a)**j for j in range(4)] for a in nodes]);Vm=matrix(R,[[z**j for j in range(4)] for z in mu]);fv=vector(R,[val(f,R(a)) for a in nodes]);gv=vector(R,[val(g,R(a)) for a in nodes]);fm=vector(R,[val(f,z) for z in mu]);gm=vector(R,[val(g,z) for z in mu])
# Algebraic identities hold rigorously by root definitions/partition; these bounds also check numerical construction.
assert all((fm[i]*gm[i]+NN).contains_zero() for i in range(2))
def calc(theta):
    theta=ri(theta) if isinstance(theta,(sp.Basic,int)) else theta;H=vector(R,[R(a)-theta for a in nodes]);p=vector(R,[NN*H[i]/(ri(ds[i])*fv[i]) for i in range(6)]);pp=vector(R,[H[i]*fv[i]/ri(ds[i]) for i in range(6)])
    assert all(z.lower()>0 for z in p) and all(z.lower()>0 for z in pp)
    M=V.transpose()*matrix.diagonal(p)*V;Mp=V.transpose()*matrix.diagonal(pp)*V
    force=4*M.inverse()*Vm.transpose()*matrix.diagonal(fm)
    dg=-Mp.inverse()*M*force
    dn=vector(R,[sum(p[i]*(gv[i]-fv[i])*(V*force)[i,j] for i in range(6)) for j in range(2)])
    growth=matrix(R,2,2,lambda i,j:2*((Vm*force)[i,j]/fm[i]+(Vm*dg)[i,j]/gm[i])-2*dn[j]/NN)
    Z=growth.inverse()*vector(R,[-2,-2]);w=force*Z;dgw=dg*Z;dnw=dn.dot_product(Z)
    deltaH=vector(R,[H[i]*(gv[i]*(V*w)[i]+fv[i]*(V*dgw)[i]-dnw)/NN for i in range(6)])
    # All entries equal exactly, since deltaH is constant (dual degree 1).
    inter=deltaH[0]
    for z in deltaH[1:]:
        inter=inter.intersection(z)
    assert all(z.lower()>0 for z in Z)
    return inter,Z,p
lo=sp.Rational(63993908,10**8);hi=sp.Rational(63993911,10**8)
L=calc(lo);U=calc(hi)
for _ in range(110):
    mid=(lo+hi)/2;MM=calc(mid)
    assert MM[0].lower()>0 or MM[0].upper()<0
    if (MM[0].lower()>0)==(L[0].lower()>0):lo=mid;L=MM
    else:hi=mid;U=MM
WHOLE=calc(R(ri(lo).lower(),ri(hi).upper()))
print("Uniform positive-Z intervals throughout bracket:",WHOLE[1])
assert (L[0].lower()>0 and U[0].upper()<0) or (L[0].upper()<0 and U[0].lower()>0)
print('Rigorous sign-changing equilibrium constraint:')
print('theta=',lo,'G=',L[0],'Z=',L[1]);print('theta=',hi,'G=',U[0],'Z=',U[1])
print('Hence by IVT a strictly positive equilibrium exists in this rational bracket.')
