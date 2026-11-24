import json,sys,itertools,time
sys.path.insert(0,'workspace');from agent3_check import appendable
fs=tuple(json.load(open('workspace/agent2_saturation_corridor3_11.json')));V=0
for f in fs:
 assert f.bit_count()==4
 V|=f
vs=[v for v in range(V.bit_length())if V>>v&1]
ts={f^(1<<v)for f in fs for v in vs if f>>v&1};es={sum(1<<v for v in e)for f in fs for e in itertools.combinations([v for v in vs if f>>v&1],2)}
print('n facets tris edges',len(vs),len(fs),len(ts),len(es),flush=True)
apps=[];ct3=[];ct4=[]
for c in itertools.combinations(vs,4):
 f=sum(1<<v for v in c)
 if f in fs:continue
 ct=sum((f^(1<<v))in ts for v in c)
 if ct>=3:ct3.append((c,ct))
 if appendable(fs,f):apps.append(c)
print('>=3 missingtets',len(ct3),ct3[:20],flush=True)
print('APPENDABLE',len(apps),apps[:20],flush=True)
# test listed order shelling from first facet
bad=[]
for i,f in enumerate(fs[1:],1):
 if not appendable(fs[:i],f):bad.append((i,f))
print('badorder',len(bad),bad[:10],flush=True)
open('workspace/agent4_corridor_verify.py','w').write(open(__file__).read())
