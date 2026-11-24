import z3,itertools,sys,time,json
from pathlib import Path
sys.path.insert(0,'workspace')
from agent4_checker import dec

def mask(c):return sum(1<<v for v in c)
def rank2(cols):
 piv={}
 for c in cols:
  while c:
   i=c.bit_length()-1
   if i in piv:c^=piv[i]
   else:piv[i]=c;break
 return len(piv)
def cm(F,n):
 faces={q:set() for q in range(5)}
 for f in F:
  vs=[i for i in range(n) if f>>i&1]
  for q in range(5):faces[q].update(mask(c) for c in itertools.combinations(vs,q))
 def lk(s):
  ans={q:set() for q in range(5)}
  for q in range(s.bit_count(),5):
   for f in faces[q]:
    if f&s==s:ans[q-s.bit_count()].add(f^s)
  return ans
 for size in range(3):
  for s in faces[size]:
   L=lk(s);dim=3-size
   ranks={0:1}
   for q in range(1,dim+2):
    low={f:i for i,f in enumerate(sorted(L[q-1]))}
    columns=[]
    for f in L[q]:columns.append(sum(1<<low[f^(1<<v)] for v in range(n) if f>>v&1))
    ranks[q]=rank2(columns)
   for q in range(1,dim+1):
    if len(L[q])-ranks[q]-ranks[q+1]:return False
 return True

def solve(n,limit):
 T={mask(c):z3.Bool('t'+str(mask(c))) for c in itertools.combinations(range(n),3)}
 Fs={mask(c):z3.Bool('f'+str(mask(c))) for c in itertools.combinations(range(n),4)}
 S=z3.Solver();S.set(timeout=120000)
 for f,x in Fs.items():
  ts=[T[f^(1<<v)] for v in range(n) if f>>v&1]
  S.add(x==z3.And(ts));S.add(z3.PbEq([(t,1) for t in ts],3)==False)
 for size in [2,3]:
  for c in itertools.combinations(range(n),size):
   a=mask(c);cond=z3.Or([x for f,x in Fs.items() if f&a==a])
   S.add(cond if size==2 else z3.Implies(T[a],cond))
 nt=z3.Sum([z3.If(x,1,0) for x in T.values()]);nf=z3.Sum([z3.If(x,1,0) for x in Fs.values()])
 S.add(nt>=(n-2)**2,nf>=nt-n*(n-1)//2+n-1,z3.Or([z3.Not(x) for x in Fs.values()]))
 S.add(Fs[15],Fs[23])
 for v in range(n):
  tv=z3.Sum([z3.If(x,1,0) for f,x in T.items() if f>>v&1]);fv=z3.Sum([z3.If(x,1,0) for f,x in Fs.items() if f>>v&1])
  S.add(tv>=2*n-5,fv>=tv-n+2)
 for c in itertools.combinations(range(n),2):
  a=mask(c);te=z3.Sum([z3.If(x,1,0) for f,x in T.items() if f&a==a]);fe=z3.Sum([z3.If(x,1,0) for f,x in Fs.items() if f&a==a]);S.add(fe>=te-1)
 start=time.time();cnt=0
 while time.time()-start<limit:
  res=S.check()
  if res!=z3.sat:print('result',res,'n',n,'models',cnt,flush=True);break
  m=S.model();F=tuple(sorted(f for f,x in Fs.items() if z3.is_true(m.eval(x))))
  cnt+=1
  if cm(F,n):
   print('CM candidate',cnt,len(F),F,flush=True)
   Path('workspace/agent1_terminal_cm_%d.json'%n).write_text(json.dumps(F))
   yes=dec(F,3);print('SHELLABLE?',yes,flush=True)
   if yes:break
  S.add(z3.Or([x!=m.eval(x) for x in T.values()]))
  if cnt%100==0:print('tested',cnt,'sec',time.time()-start,flush=True)
if __name__=='__main__':
 Path('workspace/agent1_triangle_sat.py').write_text(Path(__file__).read_text())
 solve(9,240)
