import json,pathlib,sys,collections,itertools,time
sys.path.insert(0,'workspace')
from agent3_graph_lifts import veronese
raw=json.loads(pathlib.Path('workspace/agent3_T272_q224_P24_allseeds.json').read_text())['seeds'];vv=veronese(8,3)
res=[];hist=collections.Counter();start=time.time()
for obj in raw:
 S=set(obj['support']);eps=[]
 for j in [6,7]:
  es=[e for e in [0,1] if all(x^(1<<j)^(e<<9) in S for x in S)]
  assert len(es)==1;eps.append(es[0])
 B=sorted({(p&63)|(((p>>8)&1)<<6)|((((p>>9)&1)^ (eps[0]*((p>>6)&1)) ^ (eps[1]*((p>>7)&1)))<<7) for p in S});assert len(B)==68
 D={}
 for p in B:
  z=vv[p]
  while z:
   h=z.bit_length()-1
   if h in D:z^=D[h]
   else:D[h]=z;break
 def red(z):
  for h in sorted(D,reverse=True):
   if z>>h&1:z^=D[h]
  return z
 buckets={}
 for p in range(256):
  if p in B:continue
  buckets.setdefault(red(vv[p]),[]).append(p)
 assert 0 not in buckets
 pairs=[(p,q) for group in buckets.values() for i,p in enumerate(group) for q in group[:i]]
 hist[len(pairs)]+=1;res.append({'source_Q':obj['Q'],'base':B,'pairs':pairs})
print('bases',len(res),'pairhist',hist,'secs',time.time()-start)
pathlib.Path('workspace/agent3_T288_mid_P8_bases.json').write_text(json.dumps({'histogram':dict(hist),'bases':res},indent=2))
pathlib.Path('workspace/agent3_T288_mid_P8_bases.py').write_text(pathlib.Path(__file__).read_text())
