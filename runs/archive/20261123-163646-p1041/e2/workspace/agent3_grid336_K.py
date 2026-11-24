import sys,json,pathlib,collections,numpy as np
sys.path.insert(0,'workspace');from agent1_checked_grid import truth_table;from agent3_graph_lifts import veronese,kernel
vv=veronese(14,5);hist=collections.Counter();res=[]
for a in range(129):
 for b in range(129):
  q=336-128*(a+b)+2*a*b
  if q%128:continue
  t=q//128
  try:f=truth_table(a,b,t)
  except AssertionError:continue
  if f.sum()!=336:continue
  S=np.flatnonzero(f).tolist();K=kernel(S,vv);D={}
  for p in S:
   z=p^S[0]
   while z:
    h=z.bit_length()-1
    if h in D:z^=D[h]
    else:D[h]=z;break
  hist[(len(D),len(K))]+=1
  if len(K)>=17:res.append({'params':[a,b,t],'support':S,'Kdim':len(K),'affrank':len(D)})
print('HIST',hist,'eligible',len(res))
pathlib.Path('workspace/agent3_grid336_K.json').write_text(json.dumps({'histogram':{str(k):v for k,v in hist.items()},'seeds':res},indent=2))
pathlib.Path('workspace/agent3_grid336_K.py').write_text(pathlib.Path(__file__).read_text())
