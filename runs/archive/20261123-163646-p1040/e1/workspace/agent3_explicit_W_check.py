"""Independently verify explicit four-term degree4 candidate by INTEGER
Magnus scalar substitutions through wordlength5; no graded Lie calculation.
"""
import sys,json
import numpy as np
from itertools import product
from collections import defaultdict
from scipy.sparse import coo_matrix,load_npz
sys.path.insert(0,'workspace')
from agent3_magnus import magnus,inverse,reduce_word
D=json.load(open('workspace/agent2_nielsen_actions_n3.json'))
gens={i+1:tuple(map(tuple,g)) for i,g in enumerate(D['generators'])}
gens.update({-i-1:tuple(map(tuple,g)) for i,g in enumerate(D['inverses'])})
def comm(a,b):return reduce_word(a+b+inverse(a)+inverse(b))
C=json.load(open('workspace/agent4_explicit_degree4_kernel_candidate.json'))
word=()
for _,sgn,(a,b,c,g) in C['term_indices']:
 t=comm(comm(comm((a+1,),(b+1,)),(c+1,)),(-g-1,))
 word+=t if sgn>0 else inverse(t)
word=reduce_word(word)
print('explicit candidate reducedF9length',len(word))
words=[w for l in range(1,6) for w in product(range(3),repeat=l)];ix={w:i for i,w in enumerate(words)}
def mul(A,B):
 P=defaultdict(int)
 for u,c in A.items():
  for v,d in B.items():
   if len(u)+len(v)<=5:P[u+v]+=c*d
 return {w:c for w,c in P.items() if c}
S={}
for a,g in gens.items():
 G=[]
 for w in g:
  P=magnus(w,5);P.pop((),None);G.append({tuple(x-1 for x in v):c for v,c in P.items()})
 cache={():{():1}};rr=[];cc=[];vv=[]
 for w in words:
  cache[w]=mul(cache[w[:-1]],G[w[-1]])
  for u,c in cache[w].items():rr.append(ix[u]);cc.append(ix[w]);vv.append(c)
 S[a]=coo_matrix((np.array(vv,dtype=np.int64),(rr,cc)),shape=(len(words),len(words))).tocsr()
V=np.zeros((len(words),3),dtype=np.int64)
for i in range(3):V[ix[i,],i]=1
start=V.copy();peak=0
for a in reversed(word):
 V=S[a]@V;peak=max(peak,int(np.max(np.abs(V))))
assert np.array_equal(V,start)
assert peak<2**40
print('INTEGER scalarMagnuscheckPASS: W∈A5; maximumintermediatecoefficient',peak)
json.dump({'word':word,'length':len(word),'integer_Magnus_through5_identity':True,'peak_coefficient':peak},open('workspace/agent3_explicit_W_check.json','w'))
