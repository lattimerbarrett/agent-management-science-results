import sympy as s
import json,time
from pathlib import Path
H,P=s.symbols('H P')

def analyze(n,r,a):
 start=time.time(); D=2*n-2; b=r-a
 cs=s.symbols('c2:'+str(n+1)); cc=[s.Integer(1),s.Integer(a)]+list(cs)
 dom=s.QQ.frac_field(*cs)
 hs=[s.Integer(1),H]
 for j in range(2,D+3):hs.append(s.expand(H*hs[-1]-P*hs[-2]))
 G=s.groebner([hs[n],hs[n+1]],H,P,domain=dom)
 def red(ex):return s.expand(G.reduce(s.expand(ex))[1])
 # Newton: i! ch_i = power sum p_i.
 powers=[s.Integer(r)]
 for k in range(1,n+1):
  powers.append(s.expand(sum((-1)**(i-1)*cc[i]*powers[k-i] for i in range(1,k))+(-1)**(k-1)*k*cc[k]))
 che=[s.Integer(r)]+[powers[k]/s.factorial(k) for k in range(1,n+1)]
 ds=[hs[k]/s.factorial(k+1) for k in range(D+1)]
 v=[];w=[]
 for i in range(D+1):
  fv=che[i+1]*hs[i] if i+1<=n else 0
  v.append(red(fv-sum(ds[j]*v[i-j] for j in range(1,i+1))))
  numerator=0
  for j in range(n+1):
   k=i+1-j
   if k<0 or k==j:continue
   factor=(P**j*hs[k-j-1]) if k>j else (-P**k*hs[j-k-1])
   numerator+=che[j]*factor/s.factorial(k)
  w.append(red(numerator-sum(ds[j]*w[i-j] for j in range(1,i+1))))
 assert v[0]==a and w[0]==b
 def chern(vs):
  out=[s.Integer(1)]
  for k in range(1,D+1):
   out.append(red(sum((-1)**(j-1)*s.factorial(j)*vs[j]*out[k-j] for j in range(1,k+1))/k))
  return out
 cv=chern(v);cw=chern(w)
 eq=[]
 for C in cv[a+1:]+cw[b+1:]:
  eq.extend(s.Poly(C,H,P).coeffs())
 eq=list(dict.fromkeys(s.factor(ex) for ex in eq if ex!=0))
 print('Building',n,r,a,'eq',len(eq),'seconds',time.time()-start,flush=True)
 GB0=s.groebner(eq,*reversed(cs),order='grevlex',method='f5b')
 GB=GB0.fglm('lex') if GB0.is_zero_dimensional else GB0
 print('GB',n,r,a,str(GB),'seconds',time.time()-start,flush=True)
 sol=s.solve(list(GB),cs,dict=True)
 print('SOLUTIONS',sol,flush=True)
 return {'n':n,'r':r,'a':a,'equations':[str(e) for e in eq],'groebner':[str(e) for e in GB],'solutions':str(sol)}

Path('workspace/agent1_width1_general.py').write_text(Path(__file__).read_text())
results=[]
for r,a in [(9,4)]:
 results.append(analyze(5,r,a))
 Path('workspace/agent1_width1_n5_results.json').write_text(json.dumps(results,indent=2))
