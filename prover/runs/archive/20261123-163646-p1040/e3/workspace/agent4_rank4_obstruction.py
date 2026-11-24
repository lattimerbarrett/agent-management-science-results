import sys,itertools,json
sys.path.insert(0,'workspace')
from agent4_derivations import *
from z3 import *
n=4;gs=generators(n);pairs=list(itertools.combinations(range(len(gs)),2));rows={};rels=[]
for q,(i,j) in enumerate(pairs):
 D=deriv_bracket(gs[i],gs[j]);v=0
 for h,p in enumerate(D):
  for w,c in p.items():
   if c%2:v^=1<<(h*n**3+sum((x-1)*n**(2-k) for k,x in enumerate(w)))
 comb=1<<q
 while v:
  bit=(v&-v).bit_length()-1
  if bit in rows:v^=rows[bit][0];comb^=rows[bit][1]
  else:rows[bit]=(v,comb);break
 if not v:rels.append([pairs[k] for k in range(len(pairs)) if comb>>k&1])
f=[[Bool(f'f{i}_{a}') for a in range(3)] for i in range(len(gs))];s=Solver();constraints={}
core={0:[0,1,0],1:[1,0,0],3:[1,1,0],6:[0,0,1],7:[1,0,0],9:[1,0,1],12:[0,0,1],13:[0,1,0],15:[0,1,1]}
for i,vals in core.items():
 for a,v in enumerate(vals):
  key=f'fixed_{i}_{a}';constraints[key]=f[i][a]==bool(v);s.assert_and_track(constraints[key],key)
def xx(vals):
 z=False
 for x in vals:z=Xor(z,x)
 return z
for q,r in enumerate(rels):
 for a,b in [(0,1),(0,2),(1,2)]:
  key=f'rel_{q}_{a}_{b}';constraints[key]=Not(xx([And(f[i][a],f[j][b]) for i,j in r]+[And(f[i][b],f[j][a]) for i,j in r]));s.assert_and_track(constraints[key],key)
assert s.check()==unsat
corekeys=[str(x) for x in s.unsat_core()]
print('initial unsatcore',len(corekeys),flush=True)
# deletion-minimize
for key in corekeys.copy():
 t=Solver();t.add([constraints[k] for k in corekeys if k!=key])
 if t.check()==unsat:corekeys.remove(key)
print('minimal core',corekeys)
for key in corekeys:
 if key.startswith('rel'):
  q=int(key.split('_')[1]);print(key,rels[q])
