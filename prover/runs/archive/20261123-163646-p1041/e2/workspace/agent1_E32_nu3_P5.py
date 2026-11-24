import sys,itertools,json,pathlib,time,collections
sys.path.insert(0,'workspace')
from agent3_lift_closure import veronese

def basis(S,vs):
 B={}
 for i,p in enumerate(S):
  v=vs[p];c=1<<i
  while v:
   k=v.bit_length()-1
   if k not in B:B[k]=(v,c);break
   v^=B[k][0];c^=B[k][1]
 return B

def red(v,B):
 c=0;r=0
 while v:
  k=v.bit_length()-1
  if k not in B:r^=1<<k;v^=1<<k;continue
  v^=B[k][0];c^=B[k][1]
 return r,c
raw=json.load(open('workspace/agent4_boundary256_orbits.json'));vs=veronese(7,3);out=[];start=time.time()
for obj in raw:
 if not obj['solvable']:continue
 S=sorted({(p&63)|((p>>3)&64) for p in obj['support']});B=basis(S,vs);X=[p for p in range(128) if p not in S];R={p:red(vs[p],B)[0] for p in X};pairs={}
 for a,b in itertools.combinations(X,2):pairs.setdefault(R[a]^R[b],[]).append((a,b))
 hits=set();triples=0
 for a,b,c in itertools.combinations(X,3):
  triples+=1;v=R[a]^R[b]^R[c]
  for d,e in pairs.get(v,[]):
   if len({a,b,c,d,e})==5:hits.add(tuple(sorted([a,b,c,d,e])))
 print(obj['type'],'P5',len(hits),'triples',triples,'time',time.time()-start,flush=True)
 out.append({'type':obj['type'],'baseS32':S,'P5':sorted(hits),'triples':triples,'pairs':sum(len(v) for v in pairs.values())})
json.dump(out,open('workspace/agent1_E32_nu3_P5.json','w'));pathlib.Path('workspace/agent1_E32_nu3_P5.py').write_text(pathlib.Path(__file__).read_text())
