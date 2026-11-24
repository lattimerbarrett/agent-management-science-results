from pathlib import Path
# Load helper definitions but avoid rebuilding cached pairing.
s=Path('workspace/agent2_g12rt_algebra.py').read_text().split('MM=[mons')[0]
exec(s)
from sage.all import vector,identity_matrix,zero_matrix
A=pickle.load(open('workspace/agent2_g12rt_pairing.pkl','rb'));BB=A['bases'];F=GF(P);rr=list(map(len,BB))
@lru_cache(None)
def pairmon(a,b):
 c,m=prod(a,b);return F(c*integral(m)) if c else F(0)
invG=[]
for d in range(13):invG.append(matrix(F,[[pairmon(a,b) for b in BB[12-d]] for a in BB[d]]).inverse())
@lru_cache(None)
def coord(m):
 t,ks,e,f=m;d=sum(ks)+e+f+t
 return vector(F,[pairmon(m,b) for b in BB[12-d]])*invG[d]

def opmon(m):
 result=[]
 for d in range(12):
  rows=[]
  for a in BB[d]:
   c,z=prod(a,m);rows.append(c*coord(z) if c else vector(F,rr[d+1]))
  result.append(matrix(F,rows))
 return result
U=opmon((0,(),1,0));V=opmon((0,(),0,1));DD=opmon((1,(),0,0));SS=[u+v for u,v in zip(U,V)];TT=[u-v for u,v in zip(U,V)]
# Graded Jordan chains for S. Each chain is a dict birth -> vector per degree.
chains=[];active=[]
for d in range(13):
 if d==0:
  for e in identity_matrix(F,rr[0]).rows():chains.append({'a':0,'vecs':[e]});active.append(len(chains)-1)
 if d==12:
  for c in active:chains[c]['b']=12
  break
 indep=[];ims=[];ended=[]
 for c in sorted(active,key=lambda c:chains[c]['a']):
  ch=chains[c];im=ch['vecs'][-1]*SS[d]
  if not ims or matrix(F,ims+[im]).rank()>len(ims):
   if im:indep.append(c);ims.append(im);continue
  co=matrix(F,ims).solve_left(im) if ims else vector(F,[])
  for e in range(ch['a'],d+1):
   for older,cc in zip(indep,co):ch['vecs'][e-ch['a']]-=cc*chains[older]['vecs'][e-chains[older]['a']]
  assert ch['vecs'][-1]*SS[d]==0
  ch['b']=d;ended.append(c)
 for c,im in zip(indep,ims):chains[c]['vecs'].append(im)
 active=indep[:]
 span=ims[:]
 for e in identity_matrix(F,rr[d+1]).rows():
  if not span or matrix(F,span+[e]).rank()>len(span):
   chains.append({'a':d+1,'vecs':[e]});active.append(len(chains)-1);span.append(e)
 assert len(span)==rr[d+1]
J=[];chain_at=[]
for d in range(13):
 ids=[i for i,c in enumerate(chains) if c['a']<=d<=c['b']];chain_at.append(ids)
 J.append(matrix(F,[chains[i]['vecs'][d-chains[i]['a']] for i in ids]))
 assert J[-1].is_invertible()
T=[J[d]*TT[d]*J[d+1].inverse() for d in range(12)];D=[J[d]*DD[d]*J[d+1].inverse() for d in range(12)]
H=[(i,j) for i,c in enumerate(chains) for j,q in enumerate(chains) if q['a']<=c['a']<=q['b']<=c['b']]
print('chains',len(chains),'interval counts',sorted((a,sum(c['a']==a for c in chains)) for a in set(c['a'] for c in chains)),flush=True)
print('HomS degree0',len(H),flush=True)
# Column representation of homogeneous endomorphisms commuting S.
# At each degree it sends source chain i -> target chain j while target alive.
loc=[{c:i for i,c in enumerate(ids)} for ids in chain_at]
# Construct sparse constraints in rows indexed by commutator and D products.
constraints={};offset=0
for d in range(12):
 n=rr[d]*rr[d+1]
 for k,(i,j) in enumerate(H):
  # E_d*T_d - T_d*E_{d+1}; row convention.
  if i in loc[d] and j in loc[d]:
   a,b=loc[d][i],loc[d][j]
   for l,x in enumerate(T[d][b]):
    if x:constraints[(offset+a*rr[d+1]+l,k)]=x
  if i in loc[d+1] and j in loc[d+1]:
   a,b=loc[d+1][i],loc[d+1][j]
   for l in range(rr[d]):
    x=-T[d][l,a]
    if x:
     key=(offset+l*rr[d+1]+b,k);constraints[key]=constraints.get(key,0)+x
 offset+=n
 # D E_{d+1}=0.
 for k,(i,j) in enumerate(H):
  if i in loc[d+1] and j in loc[d+1]:
   a,b=loc[d+1][i],loc[d+1][j]
   for l in range(rr[d]):
    x=D[d][l,a]
    if x:constraints[(offset+l*rr[d+1]+b,k)]=x
 offset+=n
 # E_d D=0.
 for k,(i,j) in enumerate(H):
  if i in loc[d] and j in loc[d]:
   a,b=loc[d][i],loc[d][j]
   for l,x in enumerate(D[d][b]):
    if x:constraints[(offset+a*rr[d+1]+l,k)]=x
 offset+=n
C=matrix(F,offset,len(H),constraints,sparse=True)
print('constraints',C.nrows(),C.ncols(),'nonzero',len(constraints),flush=True)
idvec=vector(F,[int(i==j) for i,j in H]);cid=C*idvec;ofs=0
for d in range(12):
 n=rr[d]*rr[d+1]
 assert not any(cid[ofs:ofs+n])
 ofs+=3*n
print('sanity: identity lies in full commutator kernel',flush=True)

K=C.right_kernel().basis_matrix();print('compact commuting endomorphisms',K.nrows(),flush=True)
# Functional of each Hom basis via expansion of v(kappa left + kappa right).
an=json.load(open('workspace/agent2_anomaly25.json'));terms={}
for ks,c in zip(an['monomials'],an['coefficients']):
 if not int(c):continue
 for mask in range(1<<len(ks)):
  aa=tuple(x for j,x in enumerate(ks) if mask>>j&1);bb=tuple(x for j,x in enumerate(ks) if not(mask>>j&1));key=(aa,bb)
  terms[key]=(terms.get(key,0)+int(c))%P
L=vector(F,len(H))
@lru_cache(None)
def kapcoord(ks):
 d=sum(ks);return coord((0,ks,0,0))*J[d].inverse()
for (aa,bb),cf in terms.items():
 e=sum(bb);right=kapcoord(bb)
 leftpairs=vector(F,[sum(x*pairmon(a,(0,aa,0,0)) for x,a in zip(J[e][r],BB[e])) for r in range(rr[e])])
 for k,(i,j) in enumerate(H):
  if i in loc[e] and j in loc[e]:L[k]+=F(cf*((-1)**e))*right[loc[e][i]]*leftpairs[loc[e][j]]
values=K*L
print('BANANA NONZERO count',sum(bool(x) for x in values),'of',len(values),flush=True)
pickle.dump({'chains':chains,'H':H,'kernel':K,'L':L,'values':values},open('workspace/agent2_banana_test.pkl','wb'))
if Path(__file__).name=='scratchpad.py':Path('workspace/agent2_banana_test.py').write_text(Path(__file__).read_text())
