import sys,json,runpy
from pathlib import Path
sys.path.insert(0,'workspace')
e=runpy.run_path('workspace/agent3_transport_weak_search.py')
fs=e['fs'];faces=e['faces'];stars=e['stars'];req=e['req'];N=e['N'];canonical=e['canonical'];allstate=e['allstate'];Graph=e['Graph'];subsets=e['subsets']
reps={};trans={}
def valid(state,s):
 rem=state&stars[s]
 if not rem or rem==state:return None
 left=state^rem
 while rem:
  z=rem&-rem;i=z.bit_length()-1;rem^=z
  if req[s][i]&left!=req[s][i]:return None
 return left

def dfs(state):
 key=canonical(state)
 if key in reps:return
 assert state.bit_count()>1
 reps[key]=state
 for s in faces:
  left=valid(state,s)
  if left is not None:dfs(left)
dfs(allstate)

def labelmap(state):
 deadvertices={v for v in subsets((1<<(2*N))-1,1) if not(stars[v]&state)}
 G=Graph();G.add_vertices(range(3*N))
 for i in range(N):G.add_edges([(i,2*N+i),(N+i,2*N+i)])
 for s in faces:
  if s.bit_count()!=2 or s&sum(deadvertices):continue
  if not(stars[s]&state):G.add_edge(*[v.bit_length()-1 for v in subsets(s,1)])
 parts=[[i for i in range(N) if (1<<i) not in deadvertices],[i for i in range(N) if (1<<i) in deadvertices],[i for i in range(N,2*N) if (1<<i) not in deadvertices],[i for i in range(N,2*N) if (1<<i) in deadvertices],list(range(2*N,3*N))]
 return G.canonical_label(partition=[p for p in parts if p],certificate=True)[1]
keys=list(reps);index={k:i for i,k in enumerate(keys)};nodes=[]
for key,state in reps.items():
 row={'facets':[f for i,f in enumerate(fs) if state>>i&1],'transitions':[]}
 for s in faces:
  left=valid(state,s)
  if left is None:continue
  ck=canonical(left);target=reps[ck];cm=labelmap(left);rm=labelmap(target);inv={v:k for k,v in rm.items()}
  perm=[inv[cm[i]] for i in range(2*N)]
  def image(f):return sum(1<<perm[i] for i in range(2*N) if f>>i&1)
  assert {image(f) for i,f in enumerate(fs) if left>>i&1}=={f for i,f in enumerate(fs) if target>>i&1}
  row['transitions'].append({'face':s,'target':index[ck],'permutation':perm})
 nodes.append(row)
obj={'rank':8,'n':18,'initial':index[canonical(allstate)],'nodes':nodes}
Path('workspace/agent3_transport44_weak1_audit.json').write_text(json.dumps(obj))
# Entire independent audit uses explicit facet sets and explicit permutations,
# not graph-isomorphism/canonical-label routines.
for row in nodes:
 F=tuple(row['facets']);assert len(F)>1
 roots={}
 for s in set(s for f in F for q in (1,2) for s in subsets(f,q)):
  D=tuple(f for f in F if f&s!=s)
  if not D:continue
  covered={f^v for f in D for v in subsets(f,1)}
  if all(f^v in covered for f in F if f&s==s for v in subsets(s,1)):roots[s]=D
 assert set(roots)=={t['face'] for t in row['transitions']}
 for t in row['transitions']:
  D=roots[t['face']];p=t['permutation'];T=nodes[t['target']]['facets']
  assert len(T)<len(F)
  assert sorted(p)==list(range(18))
  assert {sum(1<<p[i] for i in range(18) if f>>i&1) for f in D}==set(T)
print('Independent audit passes',len(nodes),'states',sum(len(x['transitions']) for x in nodes),'transitions')
Path('workspace/agent3_transport44_weak1_audit.py').write_text(Path(__file__).read_text())
