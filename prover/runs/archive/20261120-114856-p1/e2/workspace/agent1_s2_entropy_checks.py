import sympy as S
x,e,h,E,E1,xi=S.symbols('x e h E E1 xi', nonzero=True)
a=S.symbols('a0:4')
nodes=list(map(S.Integer,[1,2,4,7]))
delta=sum(a[j]*x**j for j in range(4))
Ls=[S.prod((x-t)/(z-t) for t in nodes if t!=z) for z in nodes]
assert S.expand(sum(L*delta.subs(x,z) for L,z in zip(Ls,nodes))-delta)==0
outside=2*S.log(1-e*delta.subs(x,xi)/h)-S.log(1-e*E/h)-S.log(1-e*E1/h)
core=[2*S.log(1+e*delta.subs(x,z)/h)-S.log(1-e*E/h)-S.log(1-e*E1/h) for z in nodes]
expr=outside+sum(L.subs(x,xi)*inc for L,inc in zip(Ls,core))
assert S.simplify(S.diff(expr,e).subs(e,0)-2*(E+E1)/h)==0

nodes=list(map(S.Integer,[-2,-1,1,2]))
def jac(w):
    H=S.Matrix([[sum(wi*t**(i+j) for wi,t in zip(w,nodes)) for j in range(2)] for i in range(2)])
    coef=H.inv()*S.Matrix([-sum(wi*t**(i+2) for wi,t in zip(w,nodes)) for i in range(2)])
    p=x*x+coef[1]*x+coef[0];pv=[p.subs(x,t) for t in nodes];hh=sum(wi*z*z for wi,z in zip(w,pv));out=[wi*z*z/hh for wi,z in zip(w,pv)]
    J=S.zeros(3)
    for j in range(3):
        dpv=-H.inv()*S.Matrix([pv[j]*nodes[j]**i-pv[-1]*nodes[-1]**i for i in range(2)])
        dp=dpv[0]+dpv[1]*x;dh=pv[j]**2-pv[-1]**2
        for i in range(3):
            J[i,j]=S.cancel((S.Integer(i==j)*pv[i]**2+2*w[i]*pv[i]*dp.subs(x,nodes[i])-out[i]*dh)/hh)
    return out,p,hh,J
w=list(map(S.Rational,[S.Rational(1,8),S.Rational(1,6),S.Rational(1,2),S.Rational(5,24)]))
w1,p,h0,J=jac(w);w2,q,h1,J1=jac(w1)
assert p==x*x-2 and q==x*x-3 and h0==h1==2 and w2==w
N=J1*J-S.eye(3);V=S.Matrix([1,4,-4])
assert N.rank()==1 and N*N==S.zeros(3) and N*V==S.zeros(3,1)
assert S.Matrix.hstack(V,*N.columnspace()).rank()==1
print('Verified exact entropy first variation and common-range nilpotent four-node derivative.')
