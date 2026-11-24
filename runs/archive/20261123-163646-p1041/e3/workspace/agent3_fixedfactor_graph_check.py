"""Exhaustive hard graph-subclass check; does NOT prove general K."""
import itertools,json,random,time
VARS=[sum(1<<x for x in range(16) if x>>i&1) for i in range(4)]
ONE=65535
QUADS=[VARS[i]&VARS[j] for i in range(4) for j in range(i+1,4)]
AFF=[ONE]+VARS

def basis(vs):
 d={}
 for v in vs:
  for k in sorted(d,reverse=True):
   if v>>k&1:v^=d[k]
  if v:
   k=v.bit_length()-1
   for j in list(d):
    if d[j]>>k&1:d[j]^=v
   d[k]=v
 return tuple(d[k] for k in sorted(d,reverse=True))

def span(bs):
 a=[0]
 for b in bs:a += [v^b for v in a]
 return a

def image_perm(cols):
 return tuple(__import__('functools').reduce(int.__xor__,(cols[i] for i in range(4) if x>>i&1),0) for x in range(16))

def compose(a,b):return tuple(a[b[x]] for x in range(16))

def action_poly(p,perm):return sum(((p>>perm[x])&1)<<x for x in range(16))

ALLPOLY=span(AFF+QUADS)
POLYIDX={p:i for i,p in enumerate(ALLPOLY)}
# Quadratic top expressed as a truth table with affine terms removed.
def top(p):
 q=p ^ (ONE if p&1 else 0)
 for i in range(4):
  if q>>(1<<i)&1:q^=VARS[i]
 return q

def stabilizer_generators(W):
 WS=set(span(W));perms=[]
 for cols in itertools.permutations(range(1,16),4):
  if len(basis(cols))<4:continue
  perm=image_perm(cols)
  if all(top(action_poly(w,perm)) in WS for w in W):perms.append(perm)
 identity=tuple(range(16)); subgroup={identity};gens=[]
 for p in perms:
  if p in subgroup:continue
  gens.append(p); todo=list(subgroup)
  for q in todo:
   for g in gens:
    r=compose(q,g)
    if r not in subgroup:subgroup.add(r);todo.append(r)
 assert len(subgroup)==len(perms)
 # Add translations, which always preserve the quadratic homogeneous space.
 gens += [tuple(x^(1<<i) for x in range(16)) for i in range(4)]
 return gens,len(perms)

def enumerate_spaces(W):
 out=set()
 for t in span(AFF):
  if t in (0,ONE):continue
  # Select any complement to the one-dimensional space <t>.
  A=[];B=(t,)
  for a in AFF:
   if len(basis(B+(a,)))>len(B):A.append(a);B=basis(B+(a,))
  assert len(A)==4
  lifts=span(A)
  for ls in itertools.product(lifts,repeat=3):
   P=basis((t,)+(tuple(w^l for w,l in zip(W,ls))))
   assert len(P)==4
   union=0
   for p in P:union|=p
   if 16-union.bit_count()>4:out.add(P)
 return out

def orbit_representatives(W):
 spaces=enumerate_spaces(W);total=len(spaces);original=set(spaces)
 gens,order=stabilizer_generators(W)
 maps=[{p:action_poly(p,g) for p in ALLPOLY} for g in gens]
 reps=[]
 while spaces:
  P=min(spaces);spaces.remove(P);todo=[P]
  for Q in todo:
   for g in maps:
    R=basis(g[p] for p in Q)
    assert R in original
    if R in spaces:spaces.remove(R);todo.append(R)
  reps.append((P,len(todo)))
 return reps,total,order

def support(P):
 S=set(range(16)) # A: y=0,z=0.
 for x in range(16):
  z=sum(((p>>x)&1)<<i for i,p in enumerate(P))
  for y in range(2):
   a=x+16*y+32*z
   if a in S:S.remove(a)
   else:S.add(a)
 return S

def flat(points,dim):
 if len(points)!=(1<<dim):return False
 a=next(iter(points));return len(basis(p^a for p in points))==dim

def candidate_flats(S,rng,count):
 L=sorted(S)
 for _ in range(count):
  picks=rng.sample(L,5);a=picks[0];B=basis(p^a for p in picks[1:])
  if len(B)==4:yield {a^v for v in span(B)}

def three_decomposition(S,seed):
 rng=random.Random(seed)
 for H in candidate_flats(S,rng,20000):
  if len(H&S)<(len(S)+16-30+1)//2:continue
  R=S^H
  if flat(R,4):return [sorted(H),sorted(R)]
  if len(R) not in (24,28,30):continue
  for K in candidate_flats(R,rng,500):
   T=R^K
   if flat(T,4):return [sorted(H),sorted(K),sorted(T)]
 raise AssertionError(('no witness',len(S),seed))

def wedge4(a,b):
 # a,b six-bit alternating2-forms on a four-space.
 pairs=list(itertools.combinations(range(4),2));v=0
 for i,I in enumerate(pairs):
  for j,J in enumerate(pairs):
   if a>>i&1 and b>>j&1 and not set(I)&set(J):v^=1
 return v

def verify_lagrangians():
 spaces=set()
 for a,b,c in itertools.combinations(range(1,64),3):
  B=basis((a,b,c))
  if len(B)==3 and all(wedge4(x,y)==0 for x,y in itertools.combinations(B,2)):spaces.add(B)
 assert len(spaces)==135
 # The GL4 orbit sizes below are 15,15,105 and thus exhaust these135 spaces.
 star=(QUADS[0],QUADS[1],QUADS[2])
 top3=(QUADS[0],QUADS[1],QUADS[3])
 mixed=(QUADS[0],QUADS[1],QUADS[2]^QUADS[3])
 orders=[]
 for W in (star,top3,mixed):
  _,order=stabilizer_generators(W);orders.append(order)
 assert orders==[1344,1344,192]
 assert sum(20160//o for o in orders)==135
 print('135 Lagrangians: GL4 orbits15,15,105')

def verify_affine_lifts(W):
 # No affine perturbations of these three quadratic forms have >half common zeros.
 maximum=0
 for ls in itertools.product(span(AFF),repeat=3):
  union=0
  for w,l in zip(W,ls):union|=w^l
  maximum=max(maximum,16-union.bit_count())
 assert maximum<=8
 return maximum

def verify():
 verify_lagrangians()
 classes=[(QUADS[0],QUADS[1],QUADS[3]),(QUADS[0],QUADS[1],QUADS[2]^QUADS[3])]
 result=[]
 for k,W in enumerate(classes):
  maximum=verify_affine_lifts(W)
  reps,total,order=orbit_representatives(W)
  print('class',k,'max lift zeros',maximum,'spaces',total,'stabilizer',order,'orbits',len(reps),flush=True)
  for i,(P,sz) in enumerate(reps):
   S=support(P);D=three_decomposition(S,10000*k+i)
   assert all(flat(set(H),4) for H in D)
   R=set()
   for H in D:R ^= set(H)
   assert R==S
   result.append(dict(type=k,P=P,orbit=sz,weight=len(S),flats=D))
  assert sum(sz for P,sz in reps)==total
 with open('workspace/agent3_fixedfactor_graph_check.json','w') as f:json.dump(result,f)
 print('PASS hard graph class:',len(result),'orbits, all XOR<=3 affine4flats')
 return result
if __name__=='__main__':verify()
