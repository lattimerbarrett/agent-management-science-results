import sympy as S
from pathlib import Path
from time import time
k=S.symbols('k',integer=True,nonnegative=True)
results=[]
def block(n,q):
 m=n//2; alpha=S.Rational(2*q+n-3,2); aa=int(2*alpha)
 maxd=n//2-1
 inds=list(range(2 if q==0 else 1 if q==1 else 0,(maxd-q)//2+1))
 if not inds:return None
 start=max(0,2-q); l=k+q
 Dinv=S.prod(l+2*j for j in range(m))/S.prod(l+2*j-1 for j in range(m+1))
 lam=(l-1)*(l+n-1)
 ss=list(range(max(1,q-1),q+max(inds)))
 def pair(s,t):
  c=S.simplify(2**(aa+1-s-t)*S.gamma(alpha-s+1)*S.gamma(alpha-t+1)/(S.pi*S.gamma(s)*S.gamma(t)))
  R=S.cancel(c*(2*k+aa+1)*S.rf(k+1,aa)*lam**2*Dinv/(S.rf(k+s,aa+2-2*s)*S.rf(k+t,aa+2-2*t)))
  parts=S.apart(R.subs(k,k+start),k)
  val=0;simple=0
  for term in S.Add.make_args(parts):
   num,den=term.as_numer_denom(); fac=S.factor_list(den)[1]
   assert len(fac)==1,(n,q,s,t,term)
   (linear,power),=fac; pp=S.Poly(linear,k); shift=pp.nth(0)/pp.nth(1)
   cc=S.cancel(term*(k+shift)**power)
   assert not cc.has(k)
   if power==1: simple+=cc; val-=cc*S.harmonic(shift-1)
   else: val+=cc*(S.zeta(power)-S.harmonic(shift-1,power))
  assert S.simplify(simple)==0
  return S.simplify(val)
 T=S.zeros(len(ss))
 for a,s in enumerate(ss):
  for b,t in enumerate(ss[a:],a):T[a,b]=T[b,a]=pair(s,t)
 B=S.Matrix([[S.binomial(i,s-q+1)*2**(s-q+1)*(-1)**(i-(s-q+1)) if 0<=s-q+1<=i else 0 for s in ss] for i in inds])
 Q=S.simplify(B*T*B.T)
 K=S.Matrix([[(q+inds[i]+inds[j]-1)*Q[i,j] for j in range(len(inds))] for i in range(len(inds))])
 minors=[S.factor(K[:i,:i].det()) for i in range(1,len(inds)+1)]
 assert all(x.is_positive is True for x in minors),(n,q,inds,minors)
 return (n,q,inds,str(K),list(map(str,minors)))
for n in range(4,18,2):
 for q in range(n//2):
  r=block(n,q)
  if r:
   results.append(r);print('PASS',n,q,r[2],r[4],flush=True)
Path('workspace/agent2_even_low_gram_results.txt').write_text(repr(results))
Path('workspace/agent2_even_low_gram_checks.py').write_text(Path(__file__).read_text())
print('Exact positive blocks checked:',len(results))
