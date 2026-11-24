from z3 import *
import itertools,time,pickle,functools
start=time.time();vs=[Bool('f%d'%x) for x in range(256)];weights=[3**((x&63).bit_count()) for x in range(256)]
def xx(ls):return functools.reduce(lambda a,b:Xor(a,b),ls,BoolVal(False))
S=Solver();S.set(timeout=30000)
# u six low bits; s bit6,t bit7. Actualweighteddegree2u+s+t.
a=vs.copy()
for i in range(8):
 for m in range(256):
  if m>>i&1:
   t=Bool('a%d_%d'%(i,m));S.add(t==Xor(a[m],a[m^(1<<i)]));a[m]=t
for m in range(256):
 if 2*(m&63).bit_count()+((m>>6)&3).bit_count()>7:S.add(Not(a[m]))
for typ in [1,0]:
 S.push()
 for u in range(64):S.add(xx([vs[u+(j<<6)] for j in range(4)])==BoolVal(typ==1 and u&3==0))
 for target in [322,326,330,334]:
  S.push();S.add(PbEq(list(zip(vs,weights)),target));tt=time.time();r=S.check();print('typ',typ,'target',target,r,'sec',time.time()-tt,flush=True)
  if r==sat:
   model=S.model();word=[int(is_true(model.eval(v,model_completion=True))) for v in vs];assert sum(x*w for x,w in zip(word,weights))==target;pickle.dump((typ,target,word),open('workspace/agent4_C3six_hit_%d.pkl'%target,'wb'))
  S.pop()
 S.pop()
open('workspace/agent4_C3six_exact.py','w').write(open(__file__).read())
print('DONE',time.time()-start)
