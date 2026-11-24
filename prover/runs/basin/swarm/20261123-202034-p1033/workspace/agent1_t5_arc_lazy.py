import itertools,z3,time,json
from pathlib import Path
st=time.time();t=5;n=15;k=5
cores=[sum(1<<a for a in range(3*i,3*i+3)) for i in range(t)]
Es=[];colors=[];by=[[] for _ in range(t)]
for i,c in enumerate(cores):
 for P in itertools.combinations([a for a in range(n) if not(c>>a&1)],2):
  by[i].append(len(Es));Es.append(c|sum(1<<a for a in P));colors.append(i)
x=[z3.Bool('x%d'%j) for j in range(len(Es))];y=[z3.Bool('y%d'%j) for j in range(len(Es))]
s=z3.Solver();s.set(timeout=5000);q=z3.Solver();q.set(timeout=5000)
for cl in by:s.add(z3.Or([x[j] for j in cl]));q.add(z3.PbEq([(y[j],1) for j in cl],1))
for a,E in enumerate(Es):
 for b in range(a):
  if colors[a]==colors[b]:continue
  inter=E&Es[b]
  if not inter:s.add(z3.Or(z3.Not(x[a]),z3.Not(x[b])))
  good=inter and (inter&~cores[colors[a]]==0 or inter&~cores[colors[b]]==0)
  if not good:q.add(z3.Or(z3.Not(y[a]),z3.Not(y[b])))
for C in itertools.combinations(range(n),t-1):
 mask=sum(1<<a for a in C);s.add(z3.Or([x[j] for j,E in enumerate(Es) if not E&mask]))
it=0;out={'n':n,'t':t,'cores':cores,'candidates':len(Es),'built_seconds':time.time()-st}
while time.time()-st<150:
 rs=s.check()
 if rs!=z3.sat:out.update(result=str(rs),iterations=it);break
 mod=s.model();avail=[j for j in range(len(Es)) if z3.is_true(mod[x[j]])]
 rq=q.check(*[z3.Not(y[j]) for j in range(len(Es)) if j not in avail])
 if rq==z3.unsat:
  out.update(result='COUNTER',iterations=it,edges=[{'color':colors[j],'vertices':[a for a in range(n) if Es[j]>>a&1]} for j in avail]);break
 if rq!=z3.sat:out.update(result='secondary '+str(rq),iterations=it);break
 qm=q.model();sel=[j for j in range(len(Es)) if z3.is_true(qm[y[j]])];assert len(sel)==t
 s.add(z3.Or([z3.Not(x[j]) for j in sel]));it+=1
 if it%100==0:print(it,len(avail),time.time()-st,flush=True)
else:out.update(result='TOTAL TIMEOUT',iterations=it)
out['seconds']=time.time()-st
Path('workspace/agent1_t5_arc_lazy.py').write_text(Path(__file__).read_text());Path('workspace/agent1_t5_arc_lazy.json').write_text(json.dumps(out,indent=2));print(json.dumps(out,indent=2))