import sys,json,time
from pathlib import Path
Path('workspace/agent3_transport_weak_search.py').write_text(Path(__file__).read_text())
sys.path.insert(0,'workspace')
from sage.all import Graph
from agent3_checker import subsets
x=json.load(open('workspace/agent4_transport_4.json'));fs=tuple(x['facets']);N=9
faces=sorted(set(s for f in fs for q in (1,2) for s in subsets(f,q)),key=lambda s:(s.bit_count(),s))
stars={s:sum(1<<i for i,f in enumerate(fs) if f&s==s) for s in faces}
ridgeowners={}
for i,f in enumerate(fs):
 for v in subsets(f,1):ridgeowners.setdefault(f^v,[]).append(i)
req={}
for s in faces:
 req[s]={}
 for i,f in enumerate(fs):
  if f&s!=s:continue
  nbr=0
  for v in subsets(s,1):
   owners=ridgeowners[f^v];assert len(owners)==2
   j=next(j for j in owners if j!=i);nbr|=1<<j
  req[s][i]=nbr
allstate=(1<<len(fs))-1;dead=set();seenstates=0

def canonical(state):
 deadvertices={v for v in subsets((1<<(2*N))-1,1) if not(stars[v]&state)}
 G=Graph();G.add_vertices(range(3*N))
 for i in range(N):G.add_edges([(i,2*N+i),(N+i,2*N+i)])
 for s in faces:
  if s.bit_count()!=2 or s&sum(deadvertices):continue
  if not(stars[s]&state):
   uv=[v.bit_length()-1 for v in subsets(s,1)];G.add_edge(*uv)
 parts=[[i for i in range(N) if (1<<i) not in deadvertices],[i for i in range(N) if (1<<i) in deadvertices],[i for i in range(N,2*N) if (1<<i) not in deadvertices],[i for i in range(N,2*N) if (1<<i) in deadvertices],list(range(2*N,3*N))]
 return tuple(map(len,parts)),G.canonical_label(partition=[p for p in parts if p]).graph6_string()

def search(state):
 global seenstates
 if state.bit_count()==1:return ()
 key=canonical(state)
 if key in dead:return None
 seenstates+=1
 if seenstates%1000==0:print('states',seenstates,'dead',len(dead),'remaining',state.bit_count(),flush=True)
 childkeys=set()
 for s in faces:
  removed=state&stars[s]
  if not removed or removed==state:continue
  remaining=state^removed;rs=removed;pure=True
  while rs:
   z=rs&-rs;i=z.bit_length()-1;rs^=z
   if req[s][i]&remaining!=req[s][i]:pure=False;break
  if not pure:continue
  ck=canonical(remaining)
  if ck in childkeys:continue
  childkeys.add(ck)
  ans=search(remaining)
  if ans is not None:return(s,)+ans
 dead.add(key);return None
t=time.time();path=search(allstate);print('WEAK1',path is not None,'states',seenstates,'time',time.time()-t,flush=True)
json.dump({'weak1':path is not None,'path':path,'states':seenstates},open('workspace/agent3_transport44_weak1.json','w'))
