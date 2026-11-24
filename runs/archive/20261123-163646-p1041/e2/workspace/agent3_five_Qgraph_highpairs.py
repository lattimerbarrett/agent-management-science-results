import itertools, collections, json, pathlib
V=range(1,6); pairs=list(itertools.combinations(V,2))
def allowed_high(E,H):
 E=set(E);H=set(H)
 for i in V:
  ns=[j if i==k else k for j,k in H if i in (j,k)]
  if any(tuple(sorted(p)) in E for p in itertools.combinations(ns,2)):return False
 return True
def typ(H):
 d=collections.Counter(x for e in H for x in e)
 return sorted(d.values(),reverse=True)
E={(1,2),(2,3),(4,5)}; ne=[p for p in pairs if p not in E]
out=[]
for z in range(1<<len(ne)):
 H=[e for i,e in enumerate(ne) if z>>i&1]
 if len(H)>=3 and allowed_high(E,H):out.append(H)
print('E3 admissible >=3 high sets',len(out))
for H in out: print(H,typ(H))
E4s={'P5':{(1,2),(2,3),(3,4),(4,5)},'C4':{(1,2),(2,3),(3,4),(1,4)},'tri_edge':{(1,2),(1,3),(2,3),(4,5)}}
r={}
for name,E in E4s.items():
 ne=[p for p in pairs if p not in E]; hs=[]
 for z in range(1<<len(ne)):
  H=[e for i,e in enumerate(ne) if z>>i&1]
  if len(H)>=4 and allowed_high(E,H):hs.append(H)
 r[name]=hs
 print(name,hs)
pathlib.Path('workspace/agent3_five_Qgraph_highpairs.json').write_text(json.dumps({'E3':out,'E4':r},indent=2))
pathlib.Path('workspace/agent3_five_Qgraph_highpairs.py').write_text(pathlib.Path('scratchpad.py').read_text())
