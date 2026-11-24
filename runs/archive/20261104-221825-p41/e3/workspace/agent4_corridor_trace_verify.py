import json,sys,itertools,time
sys.path.insert(0,'workspace');from agent3_check import appendable;from agent4_fastcert import fastcert
p=json.load(open('workspace/agent2_saturation_corridor3_11_trace.json'))
base=tuple(sorted(sum(1<<v for v in f)for f in p['base']));fs=list(base);print('basecertstart',len(base),flush=True);t=time.time();bc=fastcert(base,0);print('baseVD',bool(bc),time.time()-t,flush=True)
if bc:json.dump(bc,open('workspace/agent4_corridor_base_vdcert.json','w'))
for i,f in enumerate(p['order']):
 f=sum(1<<v for v in f)
 assert f not in fs and appendable(fs,f),(i,f)
 fs.append(f)
final=set(json.load(open('workspace/agent2_saturation_corridor3_11.json')))
assert set(fs)==final
print('VERIFIED ALL',len(p['order']),'APPENDED',len(fs),flush=True)
# Homology mod2
verts=range(20);edges=list(itertools.combinations(verts,2));ei={sum(1<<v for v in e):i for i,e in enumerate(edges)};tris={f^(1<<v)for f in fs for v in verts if f>>v&1};ti={t:i for i,t in enumerate(tris)}
def rank(vectors):
 basis={}
 for row in vectors:
  while row:
   j=row.bit_length()-1
   if j in basis:row^=basis[j]
   else:basis[j]=row;break
 return len(basis)
r2=rank([sum(1<<ei[t^(1<<v)]for v in verts if t>>v&1)for t in tris]);r3=rank([sum(1<<ti[f^(1<<v)]for v in verts if f>>v&1)for f in fs])
print('Betti mod2',1,len(edges)-19-r2,len(tris)-r2-r3,len(fs)-r3,flush=True)
open('workspace/agent4_corridor_trace_verify.py','w').write(open(__file__).read())
