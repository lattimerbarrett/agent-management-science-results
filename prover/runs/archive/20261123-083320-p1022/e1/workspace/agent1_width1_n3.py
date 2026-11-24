import sympy as s
import json
from pathlib import Path
x,y,H,P,z,t=s.symbols('x y H P z t')
c2,c3=s.symbols('c2 c3')
D=4

def trunc(expr):
    expr=s.Poly(s.expand(expr),x,y)
    return s.Add(*(coef*x**i*y**j for (i,j),coef in expr.terms() if i+j<=D))

def hom(expr,k):
    return s.Add(*(coef*x**i*y**j for (i,j),coef in s.Poly(s.expand(expr),x,y).terms() if i+j==k))

def complete(k): return sum(x**i*y**(k-i) for i in range(k+1))

def reduce_gr(expr):
    sym,rem,mapping=s.symmetrize(s.expand(expr),[x,y],formal=True)
    assert rem==0,rem
    sym=s.expand(sym.subs({mapping[0][0]:H,mapping[1][0]:P}))
    G=s.groebner([H**3-2*H*P,H**4-3*H**2*P+P**2],H,P,domain=s.QQ.frac_field(c2,c3))
    return s.factor(G.reduce(sym)[1])

def chern(ch, rank):
    # exp(sum (-1)^(k-1) (k-1)! ch_k t^k)
    logc=sum((-1)**(k-1)*s.factorial(k-1)*hom(ch,k)*t**k for k in range(1,D+1))
    poly=s.series(s.exp(logc),t,0,D+1).removeO().expand()
    return [reduce_gr(poly.coeff(t,k)) for k in range(1,D+1)]

Den=sum(complete(k)/s.factorial(k+1) for k in range(D+1))
U=Den-1
Inv=trunc(sum((-U)**i for i in range(D+1)))
results=[]
for r in [3,4,5]:
 for a in range(1,r):
    b=r-a
    che=[r,a,(a*a-2*c2)/2,(a**3-3*a*c2+3*c3)/6]
    V=trunc(sum(che[j]*complete(j-1) for j in range(1,4))*Inv)
    Ex=sum(che[j]*x**j for j in range(4))
    # symmetrize W by average; antisymmetric part zero in flag ring.
    W0=trunc(Ex-trunc(sum(x**i/s.factorial(i) for i in range(D+1))*V))
    W=trunc((W0+W0.xreplace({x:y,y:x}))/2)
    cv=chern(V,a)
    cw=chern(W,b)
    equations=[]
    for j,C in enumerate(cv,1):
      if j>a:
       equations.extend(s.Poly(C,H,P).coeffs())
    for j,C in enumerate(cw,1):
      if j>b:
       equations.extend(s.Poly(C,H,P).coeffs())
    equations=[s.factor(e) for e in equations if e!=0]
    G=s.groebner(equations,c2,c3)
    solutions=s.solve(equations,[c2,c3],dict=True)
    print('r,a,b',r,a,b,'ideal',G,'solutions',solutions)
    results.append({'r':r,'a':a,'b':b,'equations':[str(e) for e in equations],'solutions':str(solutions)})
Path('workspace/agent1_width1_n3_results.json').write_text(json.dumps(results,indent=2))
Path('workspace/agent1_width1_n3.py').write_text(Path(__file__).read_text())
