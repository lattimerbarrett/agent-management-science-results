import json,itertools,time
exec(open('workspace/agent1_four_subspace_realblocks.py').read().split('blocks=[];')[0])
blocks=json.load(open('workspace/agent1_four_subspace_realblocks.json'))
for b in blocks:b['kind']='real'
for T in range(1,15):
 blocks.append({'D':1,'dims':[int(T>>i&1) for i in range(4)],'U':[[1] if T>>i&1 else [] for i in range(4)],'kind':'coordinate'})
# All regular companion blocks, allowing duplicate arm permutations.
def pmul(a,b):
 c=0
 while b:
  if b&1:c^=a
  a<<=1;b>>=1
 return c

def pmod(a,b):
 while a and a.bit_length()>=b.bit_length():a^=b<<(a.bit_length()-b.bit_length())
 return a

def irred(p):
 k=p.bit_length()-1
 return not any(pmod(p,q)==0 for j in range(1,k//2+1) for q in range((1<<j)|1,1<<(j+1),2))
for k in range(1,7):
 for d in range(1,k+1):
  if k%d:continue
  for p in range((1<<d)|1,1<<(d+1),2):
   if not irred(p):continue
   f=1
   for _ in range(k//d):f=pmul(f,p)
   cols=[1<<(i+1) for i in range(k-1)]+[f^1<<k]
   A=[[1<<i for i in range(k)],[1<<(k+i) for i in range(k)],[(1<<i)|(1<<(k+i)) for i in range(k)],[(1<<i)|(cols[i]<<k) for i in range(k)]]
   # p=x is separately needed (nilpotent); p=x+1 included here.
   perms=itertools.permutations(range(4)) if d==1 else [tuple(range(4))]
   for perm in perms:
    U=[A[i] for i in perm]
    blocks.append({'D':2*k,'dims':[k]*4,'U':U,'kind':'regular','polynomial':f})
 # nilpotent x^k block
 cols=[1<<(i+1) for i in range(k-1)]+[0]
 A=[[1<<i for i in range(k)],[1<<(k+i) for i in range(k)],[(1<<i)|(1<<(k+i)) for i in range(k)],[(1<<i)|(cols[i]<<k) for i in range(k)]]
 for perm in itertools.permutations(range(4)):
  blocks.append({'D':2*k,'dims':[k]*4,'U':[A[i] for i in perm],'kind':'regular','polynomial':1<<k})

subsets=[s for s in range(1,16) if s.bit_count()>=2]

def profile(b):
 D=b['D'];U=b['U'];Ns=[kernel(B,D) for B in U]
 relations=[]
 for i in range(1,4):relations +=[v<<((i-1)*D) for v in U[i]]
 relations +=[v|(v<<D)|(v<<(2*D)) for v in U[0]]
 P=basis(relations);Q=[]
 for j in range(3*D):
  v=1<<j
  while v:
   p=v.bit_length()-1
   if p in P:v^=P[p]
   else:P[p]=v;Q.append(j);break
 assert len(Q)==3*D-sum(b['dims']) # common intersection of allfour is0
 grouped=[];dims=[]
 for S in subsets:
  P={};cons=[]
  normals=[]
  for i in range(4):
   if not S>>i&1:continue
   for a in Ns[i]:
    v=a;z=(a<<((i-1)*D)) if i else 0
    normals.append(a)
    while v:
     p=v.bit_length()-1
     if p in P:v^=P[p][0];z^=P[p][1]
     else:P[p]=(v,z);break
    if not v and z:cons.append(sum(((z>>j)&1)<<l for l,j in enumerate(Q)))
  dims.append(D-len(basis(normals)))
  grouped.append(list(basis(cons).values()))
 masks=[];flips=[0]*len(Q);t=0
 for C in grouped:
  m=0
  for c in C:
   m|=1<<t
   for j in range(len(Q)):
    if c>>j&1:flips[j]|=1<<t
   t+=1
  masks.append(m)
 out=set();st=0
 for a in range(1<<len(Q)):
  if a:st^=flips[(a&-a).bit_length()-1]
  out.add(sum((not(st&m))<<i for i,m in enumerate(masks)))
 return dims,sorted(out),len(Q)

start=time.time();unique={}
for i,b in enumerate(blocks):
 dims,flags,K=profile(b)
 key=(b['D'],tuple(b['dims']),tuple(dims),tuple(flags))
 if key not in unique:unique[key]={'D':b['D'],'dims':b['dims'],'intersection_dims':dims,'affine_flags':flags,'offset_dimension':K,'U':b['U'],'kind':b['kind']}
 if i%50==0:print(i,len(blocks),'unique',len(unique),'sec',time.time()-start,flush=True)
print('done',len(blocks),'unique',len(unique),'sec',time.time()-start)
open('workspace/agent1_four_subspace_blockprofiles.json','w').write(json.dumps({'subsets':subsets,'blocks':list(unique.values())}))
open('workspace/agent1_four_subspace_blockprofiles.py','w').write(open(__file__).read())
