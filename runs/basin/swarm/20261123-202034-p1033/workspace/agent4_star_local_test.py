import itertools,random,z3,json,time
random.seed(437);start=time.time();out=[]
for trial in range(40):
 n=11;r=3;Es=random.sample(list(itertools.combinations(range(n),r)),70)
 Ms=[sum(1<<x for x in E) for E in Es]
 cover=None;t=0
 for t in range(1,n+1):
  for C in itertools.combinations(range(n),t):
   cm=sum(1<<x for x in C)
   if all(cm&m for m in Ms):cover=C;break
  if cover:break
 if t<6:continue
 colors=[next(j for j,c in enumerate(cover) if c in E) for E in Es]
 s=z3.Solver();s.set(timeout=5000)
 vs=[[z3.Bool('v%d_%d'%(a,c)) for c in range(t)] for a in range(len(Es))]
 for a in range(len(Es)):
  s.add(z3.PbLe([(v,1) for v in vs[a]],1));s.add(z3.Not(vs[a][colors[a]]))
 for a,m in enumerate(Ms):
  for b in range(a):
   if not m&Ms[b]:s.add(z3.Or(vs[a][colors[b]],vs[b][colors[a]]))
 status=str(s.check());item={'trial':trial,'rank':r,'tau':t,'m':len(Es),'status':status};out.append(item);print(item,flush=True)
 if status=='sat':
  item['edges']=Es;item['cover']=cover;item['colors']=colors;md=s.model();item['targets']=[[c for c in range(t) if z3.is_true(md.eval(vs[a][c]))] for a in range(len(Es))];break
with open('workspace/agent4_star_local_test.json','w') as f:json.dump(out,f)
with open('workspace/agent4_star_local_test.py','w') as f:f.write(open(__file__).read())
print('elapsed',time.time()-start)
