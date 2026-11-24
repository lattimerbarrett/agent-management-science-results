import itertools,networkx as nx,pickle
from pathlib import Path
H=nx.Graph()
H.add_edges_from([(0,i) for i in range(1,5)]+[(1,2),(2,3),(3,4),(4,1)]+[(1,5),(5,6),(6,1),(3,7),(7,8),(8,3)])
for S in itertools.chain.from_iterable(itertools.combinations(list(H),k) for k in range(10)):
 if H.subgraph(S).number_of_edges():continue
 J=H.subgraph([v for v in H if v not in S])
 if sorted(sorted(dict(C.degree()).values()) for C in [J.subgraph(c) for c in nx.connected_components(J)])==[[1,1],[1,1],[1,1,2]]:
  print('P3+2K2 independent deletion:',S,flush=True)
p=q=3
pairs=list(itertools.combinations(range(1+p+q),2)); idx={e:i for i,e in enumerate(pairs)}
def bit(u,v):return 1<<idx[tuple(sorted((u,v)))]
A=list(range(1,p+1));B=list(range(p+1,p+q+1))
internal=sum(bit(u,v) for P in [A,B] for u,v in itertools.combinations(P,2))
full=(1<<len(pairs))-1; outside=full^internal
patterns=set()
for z in [None]+list(H):
 rest=[v for v in H if v!=z]
 for parts in range(1<<len(rest)):
  X=[v for i,v in enumerate(rest) if parts>>i&1];Y=[v for i,v in enumerate(rest) if not parts>>i&1]
  Xc=[v for v in X if any(w in X for w in H[v])];Yc=[v for v in Y if any(w in Y for w in H[v])]
  if len(Xc)>p or len(Yc)>q:continue
  for aa in itertools.permutations(A,len(Xc)):
   for bb in itertools.permutations(B,len(Yc)):
    m=dict(zip(Xc,aa));m.update(zip(Yc,bb))
    if z is not None:m[z]=0
    mask=0
    for u,v in H.edges():
     if u in m and v in m:mask|=bit(m[u],m[v])
    patterns.add(mask)
# Remove patterns that properly contain another certificate.
mins=[]
for pat in sorted(patterns,key=int.bit_count):
 if not any(x&pat==x for x in mins):mins.append(pat)
print('raw patterns',len(patterns),'minimal patterns',len(mins),flush=True)
ints=[i for i in range(len(pairs)) if internal>>i&1];outs=[i for i in range(len(pairs)) if outside>>i&1]
checked=0;found=[]
for maski in range(1<<len(ints)):
 added=sum(1<<ints[j] for j in range(len(ints)) if maski>>j&1)
 e=added.bit_count()
 if not e:continue
 if e==1:continue # Ordinary candidate; not a new equality gadget.
 relevant=[pat for pat in mins if pat&internal&added==pat&internal]
 for lost in range(e):
  for dd in itertools.combinations(outs,lost):
   missing=sum(1<<j for j in dd)
   mask=outside^missing|added
   checked+=1
   if not any(pat&mask==pat for pat in relevant):
    found.append((mask,e-lost))
    print('FOUND gain',e-lost,'internal',[pairs[i] for i in ints if added>>i&1],'missing',[pairs[i] for i in outs if missing>>i&1],flush=True)
    if len(found)>=10:break
  if len(found)>=10:break
 if len(found)>=10:break
print('checked',checked,'found',len(found))
# Test the claimed two-sided-edge certificate when finite cross edges are missing.
a,b=A[:2];c,d=B[:2]
for missing_edges in [[(a,c),(b,d)],[(a,c),(a,d),(b,c),(b,d)]]:
 mask=outside|bit(a,b)|bit(c,d)
 for u,v in missing_edges:mask&=~bit(u,v)
 print('two-sided edges; missing cross=',missing_edges,'H embeds=',any(pat&mask==pat for pat in mins),flush=True)
pickle.dump((pairs,mins,found),open('h9_gadget_search.pkl','wb'))