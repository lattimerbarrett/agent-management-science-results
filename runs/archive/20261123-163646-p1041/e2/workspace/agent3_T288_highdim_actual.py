import json,pathlib,sys,collections,time
sys.path.insert(0,'workspace')
from agent3_graph_lifts import veronese,kernel
from agent3_lift_closure import closure
raw=json.loads(pathlib.Path('workspace/agent3_T288_highdim_P8_bases.json').read_text())
vs2=veronese(8,2);vs5=veronese(12,5);vs4=veronese(12,4)
out=[];hist=collections.Counter();start=time.time()
for obj in raw:
 B=obj['base'];E,_=closure(B,vs2)
 for p,comb in E:
  h={p}|{B[j] for j in range(34) if comb>>j&1}
  F=sorted(h|{x^256 for x in set(B)^h});assert len(F)==36
  S=sorted(x+(u<<9) for x in F for u in range(8))
  K5=kernel(S,vs5);K4=kernel(S,vs4)
  A={}
  for x in S:
   z=x^S[0]
   while z:
    i=z.bit_length()-1
    if i in A:z^=A[i]
    else:A[i]=z;break
  cl4,_=closure(S,vs4);odd=sum((a&b).bit_count()%2 for a in K4 for b in K5)
  hist[(len(A),len(K5),len(K4),len(cl4),bool(odd))]+=1
  out.append({'source_type':obj['type'],'source_Q':obj['Q'],'point':p,'base':F,'affine_rank':len(A),'K5dim':len(K5),'K4dim':len(K4),'cl4_extra_count':len(cl4),'K4_K5_odd_pair_count':odd})
print('hist',hist,'seconds',time.time()-start)
pathlib.Path('workspace/agent3_T288_highdim_actual.json').write_text(json.dumps({'results':out,'histogram':{str(k):v for k,v in hist.items()}},indent=2))
pathlib.Path('workspace/agent3_T288_highdim_actual.py').write_text(pathlib.Path(__file__).read_text())
