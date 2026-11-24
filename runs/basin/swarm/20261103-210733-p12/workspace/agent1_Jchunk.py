import sys,time,json
sys.path.insert(0,'workspace')
import agent1_J as h
from agent4_pairing import partitions
parts=list(partitions(24))
lo,hi=500,1000
out={};t0=time.time()
for idx in range(lo,hi):
 a=parts[idx];t=time.time();v=h.J(25,23,tuple(x+1 for x in a));out[str(idx)]=v
 json.dump(out,open('workspace/agent1_J500_1000.json','w'))
 print(idx,a,v,'time',round(time.time()-t,2),'total',round(time.time()-t0,2),h._J.cache_info(),flush=True)
