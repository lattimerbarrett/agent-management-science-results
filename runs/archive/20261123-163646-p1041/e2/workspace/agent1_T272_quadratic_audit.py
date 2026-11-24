import sys,json,pathlib
sys.path.insert(0,'workspace')
from agent3_lift_closure import veronese,closure

def rank(vs):
 B={}
 for v in vs:
  while v:
   k=v.bit_length()-1
   if k in B:v^=B[k]
   else:B[k]=v;break
 return len(B)

S=[p for p in range(512) if (1^sum(((p>>(2*j))&1)*((p>>(2*j+1))&1) for j in range(4)))&1]
assert len(S)==272
K=272-rank(veronese(9,5)[p] for p in S);assert K==10
X,r=closure(S,veronese(9,2));assert not X
result={'weight':len(S),'K5':K,'affine_evaluation_rank':rank(1|(p<<1) for p in S),'cl2extras':len(X)}
json.dump(result,open('workspace/agent1_T272_quadratic_audit.json','w'));pathlib.Path('workspace/agent1_T272_quadratic_audit.py').write_text(pathlib.Path(__file__).read_text());print(result)
