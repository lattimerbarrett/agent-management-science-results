import sys,pickle,time
from collections import defaultdict
sys.path.insert(0,'workspace')
from agent3_exact_pointed import smooth,tail,S48
P,labs,rows,fl=pickle.load(open('workspace/agent2_coupled_matrix.pkl','rb'))
parts=S48['parts']
def mons(d,n):
 if n==2:return [(p,a,d-k-a) for k in range(d+1) for p in parts(k) for a in range(d-k+1)]
 return [(p,d-k) for k in range(d+1) for p in parts(k)]
cols=mons(13,2);h12=mons(12,1);h13=mons(13,1)
idx={m:i for i,m in enumerate(cols)};i12={m:len(cols)+i for i,m in enumerate(h12)};i13={m:len(cols)+len(h12)+i for i,m in enumerate(h13)}
def mod(c):return c.numerator*pow(c.denominator%P,P-2,P)%P
start=time.time()
for n,(lab,row) in enumerate(zip(labs,rows)):
 out=defaultdict(int)
 if lab[0]=='rel':
  r,ab,sig,mul=lab[1]
  for (mu,exps),c in smooth(r,tuple(sig),tuple(ab)).items():
   key=(tuple(sorted(mu+mul[0])),)+tuple(a+b for a,b in zip(exps,mul[1:]))
   out[idx[key]]+=mod(c)
  if mul[1:]==(0,0):
   for (mu,a),c in tail(r,tuple(sig),*ab).items():out[i12[(tuple(sorted(mu+mul[0])),a)]]+=mod(c)
 elif lab[0]=='single':
  d=lab[1];r,ab,sig,mul=lab[2];ix=i12 if d==12 else i13
  for (mu,(a,)),c in smooth(r,tuple(sig),tuple(ab)).items():out[ix[(tuple(sorted(mu+mul[0])),a+mul[1])]]+=mod(c)
 elif lab[0]=='beta':
  mu,a,b=lab[1]
  for x,y in [(a,b)]+([] if a==b else[(b,a)]):
   out[idx[(mu,x+1,y)]]-=1;out[idx[(mu,x,y+1)]]-=1
 elif lab[0]=='gamma':
  mu,a=lab[1];out[i12[(mu,a+1)]]-=1;out[i13[(mu,a+2)]]+=1
 else:raise ValueError(lab)
 expected={j:c%P for j,c in out.items() if c%P}
 actual={j:c%P for j,c in enumerate(row) if c%P}
 assert expected==actual,(n,lab)
print('Independently verified all',len(rows),'coupled constraint rows from exact QQ generator in',time.time()-start,'seconds')
from agent3_dual_check import I
from fractions import Fraction
import json
j=json.load(open('workspace/agent3_radical.json'))
delta=[(tuple(mu),mod(Fraction(c))) for mu,c in zip(j['monomials'],j['coefficients'])]
for lab,actual in zip(labs,fl):
 value=0
 if lab[0]=='beta':
  mu,a,b=lab[1]
  value=12*(2 if a!=b else 1)*sum(c*I(tuple(sorted(mu+m)),a,b) for m,c in delta)
 elif lab[0]=='gamma':
  mu,a=lab[1]
  for m,c in delta:
   value+=c*I(tuple(sorted(mu+m)),a)
   if 1 in m:
    rem=list(m);rem.remove(1)
    value-=c*m.count(1)*I(tuple(sorted(mu+tuple(rem))),a+1)
 assert value%P==actual%P,lab
print('Independently checked all',len(fl),'functional-column coefficients:12A+B; total seconds',time.time()-start)
from pathlib import Path
if Path(__file__).resolve()!=Path('workspace/agent4_coupled_check.py').resolve():
 source=Path(__file__).read_text()
 Path('workspace/agent4_coupled_check.py').write_text(source)
