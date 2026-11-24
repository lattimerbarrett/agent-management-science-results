import json,pickle,z3,time
m=15;n=1<<m

def bx(v):
 if not v:return z3.BoolVal(False)
 while len(v)>1:v=[z3.Xor(v[i],v[i+1]) if i+1<len(v) else v[i] for i in range(0,len(v),2)]
 return v[0]
results=[]
for g in json.load(open('workspace/agent1_GL4_maximals.json')):
 start=time.time();parent=list(range(n))
 def root(x):
  while parent[x]!=x:parent[x]=parent[parent[x]];x=parent[x]
  return x
 for p in g['gens']:
  mp=[0]*n
  for mask in range(1,n):
   l=mask&-mask;mp[mask]=mp[mask^l]|(1<<p[l.bit_length()-1])
  for i,j in enumerate(mp):
   a=root(i);b=root(j)
   if a!=b:parent[max(a,b)]=min(a,b)
 roots=[root(i) for i in range(n)];reps=sorted(set(roots));idx={r:i for i,r in enumerate(reps)};orb=[idx[r] for r in roots];sizes=[0]*len(reps)
 for o in orb:sizes[o]+=1
 allowed=[j for j,s in enumerate(sizes) if s<=334];ind={j:i for i,j in enumerate(allowed)};B={}
 for mask in reps:
  if mask.bit_count()<=8:continue
  eq=0;sub=mask
  while True:
   if orb[sub] in ind:eq^=1<<ind[orb[sub]]
   if sub==0:break
   sub=(sub-1)&mask
  while eq:
   k=eq.bit_length()-1
   if k in B:eq^=B[k]
   else:B[k]=eq;break
 null=[]
 for free in range(len(allowed)):
  if free in B:continue
  v=1<<free
  for pivot in sorted(B):
   if (B[pivot]&v).bit_count()%2:v^=1<<pivot
  null.append(v)
 print('group',g['order'],'orbits',len(reps),'allowed',len(allowed),'dim',len(null),flush=True)
 s=z3.Tactic('sat').solver();s.set(timeout=60000,anf=True,**{'anf.exlin':True,'anf.delay':0});v=[z3.Bool(f'v{i}') for i in range(len(null))];o=[bx([v[k] for k,b in enumerate(null) if b>>j&1]) for j in range(len(allowed))]
 s.add(z3.Or(*[z3.PbEq([(q,sizes[j]) for q,j in zip(o,allowed)],w) for w in [322,326,330,334]]));r=s.check();print('RESULT',r,'time',time.time()-start,flush=True);results.append({'order':g['order'],'orbits':len(reps),'dim':len(null),'result':str(r)})
 if r==z3.sat:
  model=s.model();word=0
  for b,q in zip(null,v):
   if z3.is_true(model.eval(q,model_completion=True)):word^=b
  S=[p for p,o in enumerate(orb) if o in ind and word>>ind[o]&1];json.dump({'support':S,'weight':len(S),'group_order':g['order']},open('workspace/agent1_maximal_found.json','w'));print('FOUND',len(S));break
json.dump(results,open('workspace/agent1_maximal_results.json','w'))
