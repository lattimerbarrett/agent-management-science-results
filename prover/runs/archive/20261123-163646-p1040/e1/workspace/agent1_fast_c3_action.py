"""Fast exact12log coordinates and linearAut action through class3."""
import json,sys
from functools import lru_cache
from itertools import combinations
from agent1_degree3 import *
from agent1_degree3_closure import coords2,L2,linear_sub
from agent1_peiffer_c3 import ew,ec,ei,ID,ONE,subst,tmul

pairs=list(combinations(range(m),2))
def scale(p,k):return {w:k*x for w,x in p.items() if k*x}
def div(p,k):
 assert all(x%k==0 for x in p.values())
 return {w:x//k for w,x in p.items() if x}
def logs12(p):
 a={w:x for w,x in p.items() if len(w)==1}
 b={w:x for w,x in p.items() if len(w)==2}
 c={w:x for w,x in p.items() if len(w)==3}
 diag={(i,i):x for (i,),x in a.items()}
 b12=add(add(scale(b,12),scale(diag,6)),scale(mul(a,a,3),6),-1)
 c12=scale(c,12)
 for (i,j),x in b.items():
  c12=add(c12,{(i,i,j):6*x});c12=add(c12,{(i,j,j):6*x})
 for (i,),x in a.items():c12=add(c12,{(i,i,i):2*x})
 c12=add(c12,scale(add(mul(a,b,3),mul(b,a,3)),6),-1)
 c12=add(c12,scale(add(mul(a,diag,3),mul(diag,a,3)),3),-1)
 c12=add(c12,scale(mul(mul(a,a,3),a,3),4))
 return [12*a.get((i,),0) for i in range(m)]+coords2(b12)+coords(c12)

def polys(v):
 a={(i,):v[i] for i in range(m) if v[i]};b={};c={}
 for x,p in zip(v[m:m+36],L2):b=add(b,p,x)
 for x,p in zip(v[m+36:],LP):c=add(c,p,x)
 return a,b,c

def bch12(X,Y):
 a,b,c=X;d,e,f=Y
 z1=add(a,d);z2=add(add(b,e),div(br(a,d),24))
 z3=add(add(c,f),div(add(br(a,e),br(b,d)),24))
 z3=add(z3,div(add(br(a,br(a,d)),br(d,br(d,a))),1728))
 return z1,z2,z3

def amatrix(E):
 vv=[logs12(add(p,ONE)) for p in E]
 A=[{(j,):v[j]//12 for j in range(m) if v[j]} for v in vv]
 Q=[]
 for v in vv:Q.append(div(polys(v)[1],6))
 cols=[v for v in vv]
 for i,j in pairs:
  b=scale(br(A[i],A[j]),12)
  c=scale(add(br(Q[i],A[j]),br(A[i],Q[j])),6)
  cols.append([0]*m+coords2(b)+coords(c))
 for p in LP:cols.append([0]*(m+36)+[12*x for x in coords(linear_sub(p,A))])
 rows=[]
 for i in range(285):rows.append([(j,cols[j][i]) for j in range(285) if cols[j][i]])
 return rows

def applymat(M,v):
 out=[]
 for row in M:
  x=sum(a*v[j] for j,a in row);assert x%12==0;out.append(x//12)
 return tuple(out)

def main(identity_file='workspace/agent1_HAP_SL3Z_random_free_identities.json',out_file='workspace/agent1_hap_fast_c3_vectors.json'):
 sys.setrecursionlimit(50000)
 acts=json.load(open('workspace/agent2_nielsen_actions_n3.json'))['actions']
 AA=[ew(acts[x]['words']) for x in ['T','P','I','C']];AI=[ei(a) for a in AA]
 data=json.load(open('workspace/agent3_hap_relator_words_ALL.json'))
 def aw(w,G,GI):
  e=ID
  for s in w:e=ec(e,G[s-1] if s>0 else GI[-s-1])
  return e
 GG=[aw(d['word'],AA,AI) for d in data['lifts']];GI=[ei(a) for a in GG]
 matrices={i+1:amatrix(g) for i,g in enumerate(GG)}
 matrices.update({-i-1:amatrix(g) for i,g in enumerate(GI)})
 print('built6linear285dimAutmatrices',flush=True)
 R=[tuple(logs12(expand(tuple(w)))) for w in data['magnus_relator_lifts']]
 @lru_cache(None)
 def act(q,f):
  if not q:return R[f]
  return applymat(matrices[q[0]],act(q[1:],f))
 rows=[]
 for ident in json.load(open(identity_file)):
  X=({}, {}, {});fw=()
  for q,f,s in ident['terms']:
   q=tuple(q);r=tuple(data['relators'][f]);fw=red(fw+q+(r if s>0 else inv(r))+inv(q))
   v=act(q,f)
   if s<0:v=tuple(-x for x in v)
   X=bch12(X,polys(v))
  assert not fw
  assert not X[0]
  z=coords2(div(X[1],12))+coords(div(X[2],6))
  rows.append(z)
  json.dump(rows,open(out_file,'w'))
  print('translated verifiedcell',ident['cell'],'nterms',len(ident['terms']),'nonzeroentries',sum(x!=0 for x in z),'actioncache',act.cache_info(),flush=True)
 return rows
if __name__=='__main__':main()
