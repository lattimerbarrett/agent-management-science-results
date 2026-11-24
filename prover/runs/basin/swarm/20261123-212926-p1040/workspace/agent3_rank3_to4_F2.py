from pathlib import Path
import sys,pickle,json,math
from fractions import Fraction
sys.path.insert(0,'workspace')
from agent3_derivations import generators
from agent3_exact_image_code import bracket_Q

gs0=generators(3,1000003);gs0=[{k:(-1 if v==1000002 else v) for k,v in g.items()} for g in gs0]
gs=[gs0[i] for i in [0,1,3,4,6,7,2,5,8]]
halls=[(j,i,k) for i in range(8) for j in range(i+1,9) for k in range(i,9)]
B={};relations=[]
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
 gcd=math.gcd(*rr.values());rr={x:c//gcd for x,c in rr.items()};relations.append(rr)
assert len(relations)==197
D3=json.load(open('workspace/agent4_gap_ia3_data.json'));D4=json.load(open('workspace/agent4_gap_ia4_data.json'))
print('names4',D4['names'][:5],flush=True)
import re
def parse(g):
 if isinstance(g,str):return ('C' if g[0]=='C' else 'M',)+tuple(map(int,re.findall(r'\d+',g)))
 return tuple(g)
idx={parse(g):i for i,g in enumerate(D4['names'])};embedding={i:idx[parse(g)] for i,g in enumerate(D3['names'])};N=24
F=pickle.load(open('workspace/agent2_rank4_cubic_F2_source.pkl','rb'))
print('basis type',type(F),'sample',str(next(iter(F.items())))[:300],flush=True)
def c3vector(rr):
 out=set()
 for h,coef in rr.items():
  if coef%2==0:continue
  a,b,c=[embedding[t] for t in halls[h]]
  for u in [(a,b,c),(b,a,c),(c,a,b),(c,b,a)]:
   key=u[0]*N*N+u[1]*N+u[2]
   if key in out:out.remove(key)
   else:out.add(key)
 return out
# Keys in this basis are purecubic source tensor coords, no mixed offset.
hits=[];residue_rows=[]
for i,rr in enumerate(relations):
 v=c3vector(rr)
 for k,row in sorted(F.items()):
  if k in v:
   if isinstance(row,dict):row={j for j,c in row.items() if c%2}
   v^=row
 if v:
  hits.append((i,len(v),rr));residue_rows.append(v.copy())
R={}
for v in residue_rows:
 v=v.copy()
 while v:
  k=min(v)
  if k in R:v^=R[k]
  else:R[k]=v;break
print('rank3 embedded relations with nonzero residue:',len(hits),'of197','residue spanrank',len(R),flush=True)
print('first hits',hits[:3],flush=True)
def weight(gen):
 typ,i,*ls=gen;i-=1;w=[0]*3
 if typ=='C':w[ls[0]-1]+=1
 else:
  w[i]-=1
  for j in ls:w[j-1]+=1
 return w
weights=[weight(g) for g in D3['names']]
from agent3_rank3_propagation import lie
A={(0,)};bb={(1,)};cc={(2,)}
images=[A,set(),set(),set(),set(),A,A^bb,set(),A^cc]
for hidx,size,rr in hits[:8]:
 ws=set();poly=set()
 for col,coef in rr.items():
  w=tuple(sum(weights[t][z] for t in halls[col]) for z in range(3));ws.add(w)
  if coef%2:poly^=lie(lie(images[halls[col][0]],images[halls[col][1]]),images[halls[col][2]])
 print('candidate relationindex',hidx,'weights',ws,'Foxnonzero',bool(poly),'Foxterms',len(poly),flush=True)
Path('workspace/agent3_rank3_kernel_all.json').write_text(json.dumps({'halls':halls,'relations':relations}))
Path('workspace/agent3_rank3_to4_F2_hits.json').write_text(json.dumps({'hits':hits}))
Path('workspace/agent3_rank3_to4_F2.py').write_text(Path('scratchpad.py').read_text())
