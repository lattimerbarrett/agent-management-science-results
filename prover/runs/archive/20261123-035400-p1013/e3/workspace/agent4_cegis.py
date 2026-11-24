import networkx as nx,json,z3,itertools,time,os
from pathlib import Path
H=nx.node_link_graph(json.load(open('workspace/agent2_glue_b_vs_clique.json')))
a=b=8
nr=a+b;N=nr+2;A=set(range(2,a+2));B=set(range(a+2,N));pairs=list(itertools.combinations(range(2,N),2));idx={e:i for i,e in enumerate(pairs)};edge=[z3.Bool('e'+str(i)) for i in range(len(pairs))]
O=z3.Optimize();O.set(timeout=30000)
def E(x,y):return edge[idx[tuple(sorted((x,y)))]]
da=[z3.Sum([z3.If(E(x,y),1,0)for y in A if y!=x])for x in sorted(A)];db=[z3.Sum([z3.If(E(x,y),1,0)for y in B if y!=x])for x in sorted(B)]
O.add(*[d<=5 for d in da],*[d<=3 for d in db]);O.add(*[da[i]>=da[i+1]for i in range(a-1)],*[db[i]>=db[i+1]for i in range(b-1)])
# No two vertex-disjoint internal P3s in A.
for six in itertools.combinations(sorted(A),6):
 for tri in itertools.combinations(six,3):
  other=tuple(x for x in six if x not in tri)
  if tri>other:continue
  for c in tri:
   le=[x for x in tri if x!=c]
   for d in other:
    lr=[x for x in other if x!=d]
    O.add(z3.Or(z3.Not(E(c,le[0])),z3.Not(E(c,le[1])),z3.Not(E(d,lr[0])),z3.Not(E(d,lr[1]))))
score=z3.Sum([z3.If(e,1,0)for e in edge])-a*b-a//2
wscore=z3.Sum([z3.If(E(x,y),2 if x in B and y in B else 1,0)for x,y in pairs])
O.add(score>=9)
O.maximize(score);O.maximize(wscore)
I=z3.Solver();I.set(timeout=30000);vs=list(H);labs={v:z3.Int('l'+str(i))for i,v in enumerate(vs)}
I.add(*[z3.And(l>=0,l<N)for l in labs.values()])
for u,v in H.edges():
 x,y=labs[u],labs[v]
 fixed=z3.Or(z3.And(x==0,y==0),z3.And(x==0,z3.Or(y==1,*[y==j for j in B])),z3.And(y==0,z3.Or(x==1,*[x==j for j in B])),z3.And(x==1,z3.Or(*[y==j for j in A])),z3.And(y==1,z3.Or(*[x==j for j in A])))
 I.add(z3.Or(fixed,*[z3.And(E(c,d),z3.Or(z3.And(x==c,y==d),z3.And(x==d,y==c)))for c,d in pairs]))
for v in H:
 I.add(z3.Implies(labs[v]==0,z3.PbLe([(labs[w]==0,1)for w in H[v]],1)))
for j in range(2,N):I.add(z3.PbLe([(l==j,1)for l in labs.values()],1))
path=Path('workspace/agent4_cegis_checkpoint.json')
cuts=json.loads(path.read_text())if path.exists()else[]
for cut in cuts:O.add(z3.Or(*[z3.Not(edge[j])for j in cut]))
start=time.time()
for it in range(len(cuts),len(cuts)+2000):
 if O.check()!=z3.sat:print('OUTER',O.reason_unknown(),flush=True);break
 m=O.model();bits=[z3.is_true(m.eval(e))for e in edge]
 stat=I.check(*[e if bit else z3.Not(e)for e,bit in zip(edge,bits)])
 if stat==z3.unsat:
  out={'a':a,'b':b,'score':m.eval(score).as_long(),'edges':[e for e,bit in zip(pairs,bits)if bit]}
  Path('workspace/agent4_cegis_found.json').write_text(json.dumps(out));print('FOUND',out,flush=True);break
 if stat!=z3.sat:print('INNER_UNKNOWN',flush=True);break
 im=I.model();mapping={v:im.eval(l).as_long()for v,l in labs.items()};used=set()
 for u,v in H.edges():
  x,y=mapping[u],mapping[v]
  if x>=2 and y>=2:used.add(idx[tuple(sorted((x,y)))])
 assert used
 cut=sorted(used);cuts.append(cut);O.add(z3.Or(*[z3.Not(edge[j])for j in cut]))
 if it%10==0:
  path.write_text(json.dumps(cuts));print(it,'score',m.eval(score),'cut',len(cut),'sec',round(time.time()-start,2),flush=True)
path.write_text(json.dumps(cuts))
