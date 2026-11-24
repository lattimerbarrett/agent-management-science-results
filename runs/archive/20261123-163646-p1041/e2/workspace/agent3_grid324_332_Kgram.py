import sys,json,pathlib,collections,numpy as np,time
sys.path.insert(0,'workspace')
from agent1_checked_grid import truth_table
from agent3_graph_lifts import veronese,kernel
vs=veronese(14,5)
out={};bad=[];start=time.time()
for w in [324,328,332]:
 hist=collections.Counter();num=0;nonself=0
 for a in range(129):
  for b in range(129):
   q=w-128*(a+b)+2*a*b
   if q%128:continue
   t=q//128
   try:arr=truth_table(a,b,t)
   except AssertionError:continue
   if arr.sum()!=w:continue
   S=np.flatnonzero(arr).tolist();K=kernel(S,vs)
   AA={}
   for p in S:
    z=p^S[0]
    while z:
     h=z.bit_length()-1
     if h in AA:z^=AA[h]
     else:AA[h]=z;break
   odd=[(i,j) for i,x in enumerate(K) for j,y in enumerate(K[:i+1]) if (x&y).bit_count()%2]
   num+=1;hist[(len(K),len(AA),bool(odd))]+=1
   if odd:nonself+=1;bad.append({'weight':w,'params':[a,b,t],'Kdim':len(K),'support':S})
 out[w]={'configs':num,'histogram':{str(k):v for k,v in hist.items()},'nonselforthogonal':nonself}
 print(w,out[w],flush=True)
pathlib.Path('workspace/agent3_grid324_332_Kgram.json').write_text(json.dumps({'summary':out,'badseeds':bad,'elapsed':time.time()-start},indent=2))
pathlib.Path('workspace/agent3_grid324_332_Kgram.py').write_text(pathlib.Path(__file__).read_text())
