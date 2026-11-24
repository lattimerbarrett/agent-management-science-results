import networkx as nx,itertools,json,time
from pathlib import Path

def pairings(v):
 if not v:yield [];return
 a=v[0]
 for j in range(1,len(v)):
  b=v[j]
  if abs(a-b) in [1,N-1]:continue
  for p in pairings(v[1:j]+v[j+1:]):yield [(a,b)]+p

def canon(ch):
 return min(tuple(sorted(tuple(sorted(((s*a+t)%N,(s*b+t)%N))) for a,b in ch)) for s in [-1,1] for t in range(N))

def matchings(edges):
 adj=[[] for _ in range(N)]
 for j,(a,b) in enumerate(edges):adj[a].append((b,j));adj[b].append((a,j))
 def rec(left,mask):
  if not left:yield mask;return
  bit=left&-left;a=bit.bit_length()-1;new=left^bit
  yield from rec(new,mask)
  for b,j in adj[a]:
   if new>>b&1:yield from rec(new^(1<<b),mask|(1<<j))
 yield from rec((1<<N)-1,0)

def stats(edges):
 cyc={l:None for l in range(3,7)};mp=999;pw=None
 for mask in matchings(edges):
  R=nx.Graph();R.add_nodes_from(range(N));R.add_edges_from(e for j,e in enumerate(edges) if not mask>>j&1)
  pats=[];cs=[];stars=[];bad=False
  for vs in nx.connected_components(R):
   C=R.subgraph(vs);degs=[d for v,d in C.degree()];m=C.number_of_edges()
   if m==0:continue
   if max(degs)<=2:
    if all(d==2 for d in degs):cs.append(m)
    else:pats.append(m)
   elif sorted(degs)==[1,1,1,3]:stars.append(3)
   else:bad=True;break
  if bad:continue
  if not cs and not stars and max(pats,default=0)<mp:mp=max(pats,default=0);pw=mask
  for l in cyc:
   if cyc[l] is None and max(pats,default=0)<=l and all(c==l for c in cs) and (not stars or l==3):cyc[l]=mask
 return mp,pw,cyc
N=12;seen=set();out=[];st=time.time();found=None
for verts in itertools.combinations(range(N),6):
 for ch in pairings(list(verts)):
  ca=canon(ch)
  if ca in seen:continue
  seen.add(ca);edges=sorted(set(tuple(sorted(e)) for e in nx.cycle_graph(N).edges())|set(ch))
  mp,pw,cyc=stats(edges)
  out.append({'chords':ch,'minpath':mp,'cycles':[l for l,m in cyc.items() if m is not None]})
  if mp==7 and all(m is not None for m in cyc.values()):found={'edges':edges,'pathmask':pw,'cyclemasks':cyc};break
 if found:break
print('N',N,'isom_dihedral',len(seen),'found',found,'time',time.time()-st)
from collections import Counter
print(Counter((s['minpath'],tuple(s['cycles'])) for s in out))
Path('workspace/agent2_linegraph_path6_search_N12.json').write_text(json.dumps({'N':N,'found':found,'rows':out},indent=2))
Path('workspace/agent2_linegraph_path6_search.py').write_text(Path(__file__).read_text())
