import sympy as s
import pickle
T,c=s.symbols("T c"); xs=s.symbols("x0:3");ys=s.symbols("y0:3");ts=s.symbols("t0:3")
ps=[T**i*(1-xs[i]*T)*(1-ys[i]*T)for i in range(3)]
ps += [(1-c*T)*s.prod(T+x for x in xs),(T+c)*s.prod(T+y for y in ys)]
D=s.Poly(s.Matrix([[s.Poly(p,T).nth(j)for j in range(5)]for p in ps]).det(method="domain-ge"),c,*xs,*ys)
P=s.Poly(0,c,*xs,*ts)
for pw,co in D.terms():
    P+=s.Poly(co*c**pw[0]*s.prod(xs[i]**pw[1+i]*(xs[i]+c*ts[i])**pw[4+i]*(1+ts[i])**(2-pw[4+i])for i in range(3)),c,*xs,*ts)
v=s.symbols("v0:4")
for j in range(4):
    order=list(xs[:j])+[c]+list(xs[j:])
    Q=s.Poly(P.as_expr().subs({z:sum(v[:i+1])for i,z in enumerate(order)},simultaneous=True),*v,*ts)
    assert all(a>0 for a in Q.coeffs())
    print(j,len(Q.coeffs()),min(Q.coeffs()))
