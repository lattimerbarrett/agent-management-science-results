from pathlib import Path
import sys,pickle,json,math
from fractions import Fraction
from functools import reduce
sys.path.insert(0,'workspace')
from agent3_derivations import generators
from agent3_exact_image_code import bracket_Q
from agent2_source_defect import load,reduce as residue,defect

gs0=generators(3,1000003)
gs0=[{k:(-1 if v==1000002 else v) for k,v in g.items()} for g in gs0]
gs=[gs0[i] for i in [0,1,3,4,6,7,2,5,8]]
halls=[(j,i,k) for i in range(8) for j in range(i+1,9) for k in range(i,9)]
assert len(halls)==240
B={};oracle=load();hits=[]
def inv(w):return [-x for x in w[::-1]]
def comm(a,b):return a+b+inv(a)+inv(b)
def plus(a,b,t):
 c=a.copy()
 for k,v in b.items():
  z=c.get(k,0)+t*v
  if z:c[k]=z
  elif k in c:del c[k]
 return c
for col,(j,i,k) in enumerate(halls):
 v=bracket_Q(bracket_Q(gs[j],gs[i],3),gs[k],3);r={col:Fraction(1)}
 while v:
  key=min(v)
  if key in B:
   b,s=B[key];t=v[key];v=plus(v,b,-t);r=plus(r,s,-t)
  else:
   t=v[key];B[key]=({x:Fraction(c,t) for x,c in v.items()},{x:c/t for x,c in r.items()});break
 if v:continue
 lcm=math.lcm(*(c.denominator for c in r.values()));rr={x:int(c*lcm) for x,c in r.items()}
 gcd=math.gcd(*rr.values());rr={x:c//gcd for x,c in rr.items()}
 tensor={}
 for h,c in rr.items():
  a,b,d=halls[h]
  for u,s in [((a,b,d),1),((b,a,d),-1),((d,a,b),-1),((d,b,a),1)]:
   key=81+81*u[0]+9*u[1]+u[2];tensor[key]=tensor.get(key,0)+c*s
 rem={p:residue(bb,tensor,p) for p,bb in oracle.items()}
 if any(rem.values()):
  word=[]
  for h,c in rr.items():
   a,b,d=halls[h];w=comm(comm([a+1],[b+1]),[d+1])
   if c<0:w=inv(w)
   word+=w*abs(c)
  # Cancel exact formal inverse neighbors for compactness.
  out=[]
  for x in word:
   if out and out[-1]==-x:out.pop()
   else:out.append(x)
  assert defect(out)==rem
  hit={'word':out,'hall_relation':[(halls[h],c) for h,c in rr.items()],'source_defect_primes':[p for p,r in rem.items() if r],'residue_sizes':{p:len(r) for p,r in rem.items()}}
  hits.append(hit)
  print('HIT',len(hits),'wordlength',len(out),'primes',hit['source_defect_primes'],'hallterms',len(rr),flush=True)
  if len(hits)>=8:break
Path('workspace/agent3_cubic_candidates.json').write_text(json.dumps({'convention':'C-first/LEFT-M sourcegeneratororder ofagent2; RtoLwordproduct; eachword in gamma3 haszeroJohnsondegree3, but no actualsource nontriviality asserted.','candidates':hits}))
Path('workspace/agent3_cubic_candidates.py').write_text(Path('scratchpad.py').read_text())
