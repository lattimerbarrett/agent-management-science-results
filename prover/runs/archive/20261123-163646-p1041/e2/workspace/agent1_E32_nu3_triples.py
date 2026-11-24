import json,sys,itertools,collections,pathlib
sys.path.insert(0,'workspace')
from agent3_lift_closure import veronese

def basis(columns):
 B={}
 for j,v in enumerate(columns):
  c=1<<j
  while v:
   k=v.bit_length()-1
   if k in B:v^=B[k][0];c^=B[k][1]
   else:B[k]=(v,c);break
 return B

def red(v,B):
 c=0;rem=0
 while v:
  k=v.bit_length()-1
  if k not in B:rem^=1<<k;v^=1<<k;continue
  v^=B[k][0];c^=B[k][1]
 return rem,c
raw=json.load(open('workspace/agent4_boundary256_orbits.json'));out=[]
for obj in raw:
 if not obj['solvable']:continue
 S=sorted({(p&63)|((p>>3)&64) for p in obj['support']});vs=veronese(7,3);B=basis([vs[p] for p in S]);X=[p for p in range(128) if p not in S];R={p:red(vs[p],B)[0] for p in X};hits=[]
 for a,b,c in itertools.combinations(X,3):
  if R[a]^R[b]^R[c]==0:hits.append([a,b,c])
 singles=[p for p in X if R[p]==0]
 pairs=[[a,b] for a,b in itertools.combinations(X,2) if R[a]==R[b]]
 cuts=collections.Counter(sum((p&v).bit_count()%2 for p in S) for v in range(1,128))
 assert not singles and not pairs and not hits
 assert min(cuts)>=8 and max(cuts)<=24
 print(obj['type'],'triples',len(hits),'cut_hist',dict(cuts));out.append({'type':obj['type'],'singles':singles,'pairs':pairs,'triples':hits,'cut_hist':dict(cuts)})
json.dump(out,open('workspace/agent1_E32_nu3_triples.json','w'));pathlib.Path('workspace/agent1_E32_nu3_triples.py').write_text(pathlib.Path(__file__).read_text())
