import sys,json,collections,itertools,pathlib,functools,operator,time
sys.path.insert(0,'workspace');from agent1_topform_gluing import anf,kernel
from agent3_lift_closure import veronese
D=json.load(open('workspace/agent1_T80_topform_structure.json'));S=D['support'];pts=D['points'];gens=json.load(open('workspace/agent1_T80_critical_triple_auts.json'))['generators'];m=11;E=veronese(m,5);target=functools.reduce(operator.xor,(E[p] for p in S),0)
basis=[];B={}
for p in pts:
 v=p
 for k,b in sorted(B.items(),reverse=True):
  if v>>k&1:v^=b
 if v:B[v.bit_length()-1]=v;basis.append(p)
assert len(basis)==10
H=[0]
for b in basis:H +=[x^b for x in H]
u0=next(u for u in range(1,1<<m) if u not in H);full=basis+[u0];coords={}
for c in range(1<<m):coords[functools.reduce(operator.xor,(b for j,b in enumerate(full) if c>>j&1),0)]=c
idx={p:i for i,p in enumerate(pts)};translates={sum(1<<(p^b) for p in S) for b in range(1<<m)};counts=collections.Counter();out=[];seen=set();t=time.time()
for gi,g in enumerate(gens):
 images=[pts[g[idx[b]]] for b in basis]+[u0];A=[0]*(1<<m)
 for p in range(1,1<<m):
  c=coords[p];A[p]=functools.reduce(operator.xor,(b for j,b in enumerate(images) if c>>j&1),0)
 if any(A[p]!=pts[g[i]] for i,p in enumerate(pts)):counts['nonlinear_gen']+=1;continue
 S0=[A[p] for p in S if not coords[p]>>10&1];S1=[A[p] for p in S if coords[p]>>10&1];target1=target^functools.reduce(operator.xor,(E[p] for p in S0),0);valid=0;novel=0
 for h in H:
  H1=[p^h for p in S1]
  if functools.reduce(operator.xor,(E[p] for p in H1),0)!=target1:continue
  valid+=1;HS=sorted(S0+H1);hmask=sum(1<<p for p in HS)
  if hmask in translates:counts['only_translate']+=1;continue
  novel+=1
  if hmask in seen:continue
  seen.add(hmask);G=sorted(S+[p|(1<<m) for p in HS]);assert max(x.bit_count() for x in anf(G,m+1))<=6
  K=kernel([veronese(m+1,5)[p] for p in G]);out.append({'m':m+1,'support':G,'gen':gi,'h':h,'K5':len(K)})
 counts['valid_extensions']+=valid;counts['new_supports']+=novel;print('GEN',gi,'valid',valid,'novel',novel,flush=True)
json.dump({'counts':dict(counts),'seeds':out},open('workspace/agent1_topform_fullstabilizer160.json','w'));pathlib.Path('workspace/agent1_topform_fullstabilizer160.py').write_text(pathlib.Path(__file__).read_text());print('DONE',dict(counts),'seeds',len(out),'K5',collections.Counter(g['K5'] for g in out),'time',time.time()-t)
