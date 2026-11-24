import z3,time,json
start=time.time();c=[z3.Int('n'+str(a)) for a in range(1,16)];w={u:sum(c[a-1] for a in range(1,16) if (u&a).bit_count()%2) for u in range(1,16)};allowed=[16,24,28,30,32,34,36,38,40]
s=z3.Solver();s.set(timeout=90000);s.add(*[x>=0 for x in c],sum(c)<=41)
for v in w.values():s.add(z3.Or(*[v==a for a in allowed]))
s.add(z3.Or(w[1]==30,w[1]==34,w[1]==38))
for u in range(1,16):
 for v in range(1,u):s.add(z3.Implies(z3.And(w[u]==16,w[v]==16),w[u^v]%4==0))
r=s.check();print('RESULT',r,'time',time.time()-start,flush=True)
if r==z3.sat:
 m=s.model();print('COUNTS',[m.eval(x) for x in c]);print('WEIGHTS',{u:m.eval(x) for u,x in w.items()})
import shutil;shutil.copyfile(__file__,'workspace/agent3_oldD4_doublyeven_profile_check.py')
