import json,pathlib,sys,collections,time
sys.path.insert(0,'workspace');from agent3_graph_lifts import veronese,kernel
raw=json.loads(pathlib.Path('workspace/agent3_T288_mid_P8_bases.json').read_text())['bases'];vv=veronese(8,3);v3=veronese(9,3);v4=veronese(9,4);v5=veronese(9,5)
res=[];hist=collections.Counter();start=time.time()
for obj in raw:
 B=obj['base'];D={}
 for j,p in enumerate(B):
  z=vv[p];c=1<<j
  while z:
   h=z.bit_length()-1
   if h in D:z^=D[h][0];c^=D[h][1]
   else:D[h]=(z,c);break
 for p,q in obj['pairs']:
  z=vv[p]^vv[q];c=0
  while z:
   h=z.bit_length()-1
   assert h in D
   z^=D[h][0];c^=D[h][1]
  H={p,q}|{B[j] for j in range(68) if c>>j&1}
  F=sorted(H|{x^256 for x in set(B)^H});assert len(F)==72
  K3=kernel(F,v3);K4=kernel(F,v4);K5=kernel(F,v5)
  assert len(K3)==10 and len(K4)==1 and len(K5)==0
  AA={}
  for p0 in F:
   z0=p0^F[0]
   while z0:
    h0=z0.bit_length()-1
    if h0 in AA:z0^=AA[h0]
    else:AA[h0]=z0;break
  assert len(AA)==9
  hist[len(K3)]+=1
  res.append({'source_Q':obj['source_Q'],'pair':[p,q],'base':F,'baseK3dim':len(K3)})
print('results',len(res),'baseK3hist',hist,'secs',time.time()-start)
pathlib.Path('workspace/agent3_T288_mid_actual.json').write_text(json.dumps({'histogram':dict(hist),'results':res},indent=2))
pathlib.Path('workspace/agent3_T288_mid_actual.py').write_text(pathlib.Path(__file__).read_text())
