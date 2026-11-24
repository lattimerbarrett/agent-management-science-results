import z3,itertools,time,json
start=time.time();A=[16,24,28,32,36,40];C=[8,12]+list(range(14,41,2));S=z3.Solver();S.set(timeout=60000)
m=[z3.Int('m%d'%i) for i in range(1,8)];n=[z3.Int('n%d'%i) for i in range(1,8)]
S.add(*[x>=0 for x in m+n]);OW=[];NW=[]
for u in range(1,8):
 ow=sum(m[x-1] for x in range(1,8) if (u&x).bit_count()%2);nw=sum(n[x-1] for x in range(1,8) if (u&x).bit_count()%2);OW.append(ow);NW.append(nw)
 S.add(z3.Or(*[ow==w for w in (A if u in [1,2,3] else C)]),z3.Or(*[nw==w for w in (A if u==4 else C)]))
S.add(OW[0]<=OW[1],OW[1]<=OW[2],*[OW[3]<=OW[x-1] for x in [5,6,7]])
for counts,W,ins in [(m,OW,[1,2,3]),(n,NW,[4])]:
 out=[u for u in range(1,8) if u not in ins]
 for u,v in itertools.product(ins,out):
  cap=sum(counts[x-1] for x in range(1,8) if (u&x).bit_count()%2 and (v&x).bit_count()%2)
  S.add(z3.Implies(z3.And(W[u-1]==16,W[v-1]==8),z3.Or(*[cap==i for i in [0,1,2,4,8]])))
  S.add(z3.Implies(z3.Or(z3.And(W[u-1]==16,W[v-1]==12),z3.And(W[u-1]==24,W[v-1]==8)),z3.Or(cap%2==0,cap<=3)))
  S.add(z3.Implies(z3.And(W[u-1]==16,W[v-1]==14),z3.Or(cap%2==0,cap<=7)))
  # v andu+v have SAMEtop4 symbol, while weights8/12/14have DIFFERENTleading-symbolannihilators.
  for a,b in itertools.permutations([8,12,14],2):S.add(z3.Not(z3.And(W[v-1]==a,W[(u^v)-1]==b)))
expr=sum(sum(z3.If(NW[x-1]==w,w*m[x-1],0) for w in (A if x==4 else C)) for x in range(1,8))
for target in [322,326,330,334]:
 S.push();S.add(sum(m)<=target//8,sum(n)<=target//8,expr==target);tt=time.time();r=S.check();print(target,r,'sec',time.time()-tt,flush=True)
 if r==z3.sat:
  mm=S.model();R={'old_counts':[mm.eval(x).as_long() for x in m],'new_counts':[mm.eval(x).as_long() for x in n],'old_weights':[mm.eval(x).as_long() for x in OW],'new_weights':[mm.eval(x).as_long() for x in NW]};print(R,flush=True);json.dump(R,open('workspace/agent4_mixed_rank3_profile_%d.json'%target,'w'))
 S.pop()
open('workspace/agent4_mixed_rank3_profile_model.py','w').write(open(__file__).read())
print('DONE',time.time()-start)
