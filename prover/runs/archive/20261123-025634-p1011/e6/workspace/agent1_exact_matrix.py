import sympy as S
from pathlib import Path
from time import time
k=S.symbols('k',integer=True,nonnegative=True)
n=18
q=1
alpha=S.Rational(2*q+15,2)
start=max(0,2-q)
l=k+q
Dinv=S.prod(l+2*j for j in range(9))/S.prod(l+2*j-1 for j in range(10))
lam=(l-1)*(l+17)
def sum_pair(s,t):
    aa=int(2*alpha)
    c=S.simplify(2**(aa+1-s-t)*S.gamma(alpha-s+1)*S.gamma(alpha-t+1)/(S.pi*S.gamma(s)*S.gamma(t)))
    R=S.cancel(c*(2*k+aa+1)*S.rf(k+1,aa)*lam**2*Dinv/(S.rf(k+s,aa+2-2*s)*S.rf(k+t,aa+2-2*t)))
    R=R.subs(k,k+start)
    parts=S.apart(R,k)
    val=0; simple=0
    for term in S.Add.make_args(parts):
        num,den=term.as_numer_denom()
        poly=S.Poly(den,k)
        fac=S.factor_list(poly.as_expr())[1]
        assert len(fac)==1,(term,fac)
        (linear,power),=fac
        pp=S.Poly(linear,k)
        aa=pp.nth(0)/pp.nth(1)
        cc=S.simplify(term*(k+aa)**power)
        assert not cc.has(k)
        if power==1:
            simple+=cc
            val-=cc*S.harmonic(aa-1)
        else:
            val+=cc*(S.zeta(power)-S.harmonic(aa-1,power))
    assert simple==0,simple
    return S.simplify(val)
maxs=3 if q<=1 else 4
T=S.zeros(maxs)
for s in range(1,maxs+1):
 for t in range(s,maxs+1):
    tm=time();T[s-1,t-1]=T[t-1,s-1]=sum_pair(s,t)
    print(s,t,T[s-1,t-1],float(T[s-1,t-1]),'time',time()-tm,flush=True)
if q==0:
    inds=[2,3,4]
elif q==1:
    inds=[1,2,3]
else:
    inds=[0,1,2,3]
B=S.Matrix([[S.binomial(i,s-q+1)*2**(s-q+1)*(-1)**(i-(s-q+1)) if 0<=s-q+1<=i else 0 for s in range(1,maxs+1)] for i in inds])
Q=S.simplify(B*T*B.T)
K=S.Matrix([[(q+inds[i]+inds[j]-1)*Q[i,j] for j in range(len(inds))] for i in range(len(inds))])
print('Q divided by pi:',Q)
print('K minors:',[K[:i,:i].det() for i in range(1,len(inds)+1)])
Path(f'workspace/agent1_exactQ18q{q}.txt').write_text(str(Q))
Path('workspace/agent1_exact_matrix.py').write_text(Path('scratchpad.py').read_text())
