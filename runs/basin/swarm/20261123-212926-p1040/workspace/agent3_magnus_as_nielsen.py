from pathlib import Path
import json,itertools
x=json.loads(Path('workspace/agent4_gap_ia3_data.json').read_text())
def inv(w):return tuple(-i for i in w[::-1])
def red(w):
 a=[]
 for i in w:
  if a and a[-1]==-i:a.pop()
  else:a.append(i)
 return tuple(a)
def sub(w,a):return red(z for i in w for z in (a[i-1] if i>0 else inv(a[-i-1])))
def comp(a,b):return tuple(sub(w,a) for w in b)
id=((1,),(2,),(3,))
perms=list(itertools.permutations((1,2,3)))
ags=[((-1,),(2,),(3,))]+[tuple((i,) for i in p) for p in perms if p!=(1,2,3)]
ags += [((2,1),(2,),(3,)),((-2,1),(2,),(3,)),((1,-2),(2,),(3,)),((1,2),(2,),(3,))]
inverse={i:next(j for j,b in enumerate(ags) if comp(a,b)==id) for i,a in enumerate(ags)}
def reverse(w):return [inverse[i] for i in w[::-1]]
def evalw(w):
 a=id
 for i in w:a=comp(ags[i],a)
 return a
def elementary(i,j,side,sign):
 p=next(p for p in perms if p[0]==i and p[1]==j)
 if p==(1,2,3):pw=[]
 else:pw=[next(k for k,a in enumerate(ags) if a==tuple((v,) for v in p))]
 base={('L',1):6,('L',-1):7,('R',-1):8,('R',1):9}[(side,sign)]
 w=reverse(pw)+[base]+pw
 expected=list(id);expected[i-1]=((sign*j,i) if side=='L' else(i,sign*j))
 assert evalw(w)==tuple(expected)
 return w
out=[]
for idx,name in enumerate(x['names']):
 typ,i,j,*rest=name
 if typ=='C':
  w=elementary(i,j,'L',1)+elementary(i,j,'R',-1)
  a=list(id);a[i-1]=(j,i,-j)
 else:
  k=rest[0]
  # product of four left Nielsen maps: choose exact ordering by check.
  a=list(id);a[i-1]=(j,k,-j,-k,i)
  w=None
  items=[elementary(i,j,'L',1),elementary(i,k,'L',1),elementary(i,j,'L',-1),elementary(i,k,'L',-1)]
  for order in itertools.permutations(items):
   v=sum(order,[])
   if evalw(v)==tuple(a):w=v;break
  assert w is not None
 assert evalw(w)==tuple(a),(name,w,evalw(w),a)
 out.append({'generator_index':idx,'name':name,'endo_word':w})
 print(name,'length',len(w),w,flush=True)
Path('workspace/agent3_magnus_as_nielsen.json').write_text(json.dumps({'convention':'endo_word append acts on left, indices0based in agent4 data. σ_word(u) equals t*u*t^-1 in RtoL convention, or t^-1*u*t in GAP LTR. All targets verified exactAutF3.','words':out}))
Path('workspace/agent3_magnus_as_nielsen.py').write_text(Path('scratchpad.py').read_text())
