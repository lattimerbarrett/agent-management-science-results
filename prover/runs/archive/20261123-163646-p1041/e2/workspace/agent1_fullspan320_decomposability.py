import sys,json,pathlib,collections,time
sys.path.insert(0,'workspace')
from agent3_lift_closure import veronese

def kernel(S,vs):
 B={};K=[]
 for i,p in enumerate(S):
  v=vs[p];c=1<<i
  while v:
   k=v.bit_length()-1
   if k in B:v^=B[k][0];c^=B[k][1]
   else:B[k]=(v,c);break
  if not v:K.append(c)
 return K
D=json.load(open('workspace/agent1_fullspan_predecessors.json'));V=veronese(14,6);out=[]
for i,d in enumerate(D):
 K=kernel(d['support'],V);weights=collections.Counter()
 for k in K:weights[k.bit_count()]+=1
 out.append({'seed':i,'K6dim':len(K),'basis_weights':dict(weights)})
print(collections.Counter(x['K6dim'] for x in out));json.dump(out,open('workspace/agent1_fullspan320_decomposability.json','w'));pathlib.Path('workspace/agent1_fullspan320_decomposability.py').write_text(pathlib.Path(__file__).read_text())
