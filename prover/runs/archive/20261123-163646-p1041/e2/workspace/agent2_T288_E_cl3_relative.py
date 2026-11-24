import json,sys,pathlib,collections,time
sys.path.insert(0,'workspace');from agent3_lift_closure import veronese

def kernel(S,vs):
 B={};out=[]
 for i,p in enumerate(S):
  v=vs[p];c=1<<i
  while v:
   k=v.bit_length()-1
   if k not in B:B[k]=(v,c);break
   v^=B[k][0];c^=B[k][1]
  if not v:out.append(c)
 return out

def insert(B,v):
 while v:
  k=v.bit_length()-1
  if k in B:v^=B[k]
  else:B[k]=v;return v
 return 0
D=json.load(open('workspace/agent2_T288_E_ALLgraph_cl3.json'));vs=veronese(11,5);hist=collections.Counter();hits=[];t=time.time()
for ix,r in enumerate(D['hits']):
 S=r['support'];E=r['extra'];assert len(S)==288 and len(E)==16
 K=kernel(S+E,vs);B={}
 for k in K:insert(B,k>>288)
 cs=[0]
 for b in B.values():cs += [c^b for c in cs]
 enumer=collections.Counter(c.bit_count() for c in cs);hist[tuple(sorted(enumer.items()))]+=1
 for c in cs:
  if c and c.bit_count()<=6:hits.append({'source':ix,'subset':[E[i] for i in range(16) if c>>i&1]})
print('hist',hist,'small',len(hits),'sec',time.time()-t)
json.dump({'hist':{str(k):v for k,v in hist.items()},'small':hits},open('workspace/agent2_T288_E_cl3_relative.json','w'));pathlib.Path('workspace/agent2_T288_E_cl3_relative.py').write_text(pathlib.Path(__file__).read_text())
# repair previously generated standalone reproducibility
p=pathlib.Path('workspace/agent2_T288_E_ALLgraph_cl3_full.py');s=p.read_text().replace('import json,sys,pathlib,collections,time','import json,sys,pathlib,collections,time,itertools');s=s.replace("pathlib.Path('workspace/agent2_T288_E_ALLgraph_cl3.py').write_text(pathlib.Path(__file__).read_text())", "None")
p.write_text(s)
