from collections import defaultdict
import json,os
N=3;L=4
one={():1};X=[{(i,):1} for i in range(N)]
def add(*args):
 o=defaultdict(int)
 for p,c in args:
  for w,v in p.items():o[w]+=c*v
 return {w:v for w,v in o.items() if v}
def mul(p,q):
 o=defaultdict(int)
 for a,u in p.items():
  for b,v in q.items():
   if len(a)+len(b)<=L:o[a+b]+=u*v
 return {w:v for w,v in o.items() if v}
def bracket(p,q):return add((mul(p,q),1),(mul(q,p),-1))
def app(d,p):
 o={}
 for w,c in p.items():
  for j,x in enumerate(w):
   q={w[:j]:c};q=mul(q,d[x]);q=mul(q,{w[j+1:]:1});o=add((o,1),(q,1))
 return o
def db(a,b):return [add((app(a,b[i]),1),(app(b,a[i]),-1)) for i in range(N)]
gens=[];info=[]
for i in range(N):
 for j in range(N):
  if i!=j:
   a=[{} for _ in range(N)];a[i]=bracket(X[j],X[i]);gens.append(a);info.append(('K',i,j))
 j,k=[j for j in range(N) if j!=i]
 a=[{} for _ in range(N)];a[i]=bracket(X[j],X[k]);gens.append(a);info.append(('M',i,j,k))
def D(i,j,k):return db(db(gens[i],gens[j]),gens[k])
relation=[((0,5,2),3),((0,2,5),-1),((0,1,1),-4),((1,2,3),-2)]
res=[{} for _ in range(N)]
for inds,c in relation:
 d=D(*inds)
 for i in range(N):res[i]=add((res[i],1),(d[i],c))
assert res==[{}, {}, {}]
print('Independent exact integer cubic derivation identity: TRUE')

# Independent direct action, integer Magnus series truncated at word length4.
y=[add((one,1),(p,1)) for p in X]
def pinv(a):
 b=add((a,1),(one,-1));o=one;p=one
 for k in range(1,L+1):p=mul(p,b);o=add((o,1),(p,(-1)**k))
 return o
maps={}
for a,desc in enumerate(info):
 for sign in [1,-1]:
  z=y.copy();typ,i,j,*rest=desc
  if typ=='K':
   f=y[j] if sign==1 else pinv(y[j]);z[i]=mul(mul(f,y[i]),pinv(f))
  else:
   k=rest[0];f=mul(mul(mul(y[j],y[k]),pinv(y[j])),pinv(y[k]));f=f if sign==1 else pinv(f);z[i]=mul(f,y[i])
  maps[(a,sign)]=[add((p,1),(one,-1)) for p in z]
def subst(p,images):
 out={}
 for w,c in p.items():
  a={():c}
  for j in w:a=mul(a,images[j])
  out=add((out,1),(a,1))
 return out
def winv(w):return [(i,-s) for i,s in reversed(w)]
def wc(a,b):return a+b+winv(a)+winv(b)
def W(i,j,k):return wc(wc([(i,1)],[(j,1)]),[(k,1)])
w=[]
for inds,e in relation:
 a=W(*inds);a=a if e>0 else winv(a);w+=a*abs(e)
# reduce elementary letters before composition
reduced=[]
for token in w:
 if reduced and token==(reduced[-1][0],-reduced[-1][1]):reduced.pop()
 else:reduced.append(token)
images=X
for token in reversed(reduced):images=[subst(p,maps[token]) for p in images]
assert images==X
print('Independent exact direct actual automorphism degree<=4: identity;',len(reduced),'elementary letters')

# Independent square-zero target signature.
def tmul(p,q):
 out=set()
 for a in p:
  for b in q:
   if a and b and a[-1]==b[0]:continue
   w=a+b
   if w in out:out.remove(w)
   else:out.add(w)
 return out
def tb(p,q):return tmul(p,q)^tmul(q,p)
A={('A',)};B={('B',)};C={('C',)};targets=[B,A,A^B,C,A,A^C,C,B,B^C]
P=set()
for inds,c in relation:
 if c%2:
  i,j,k=inds;P^=tb(tb(targets[i],targets[j]),targets[k])
assert P=={tuple(w) for w in ['ACB','BAC','BCA','CAB']}
print('Independent target degree3 polynomial:', '+'.join(''.join(w) for w in sorted(P)))
os.makedirs('workspace',exist_ok=True)
with open('workspace/agent3_cubic_independent.py','w') as f:f.write(open(__file__).read())

# Additional convention audit: derive every target matrix directly from Fox rows.
import sympy as sp
AA=sp.Matrix([[-1,0],[0,1]]);BB=sp.Matrix([[-1,2],[0,1]]);CC=sp.Matrix([[1,0],[2,-1]])
targetmatrices=[BB,AA,AA*BB,CC,AA,AA*CC,CC,BB,BB*CC]
foxmatrices=[]
for desc,expected in zip(info,targetmatrices):
 typ,i,j,*rest=desc;J=sp.eye(3)
 if typ=='K':J[i,i]=-1;J[i,j]=2
 else:J[i,j]=2;J[i,rest[0]]=-2
 assert J*sp.ones(3,1)==sp.ones(3,1)
 Q=sp.Matrix(2,2,lambda r,s:J[r,s]-J[2,s]);Q=Q.inv()
 assert Q==expected or Q==-expected
 foxmatrices.append(Q)
a=sp.eye(2);b=sp.eye(2)
for i,s in reduced:a=a*(foxmatrices[i]**s);b=b*(targetmatrices[i]**s)
assert a==b or a==-b
print('Direct inverse-Fox quotient matrices match projective reflection words: TRUE')
print('Actual inverse-Fox image of cubic u:', a.tolist())

# Finite class-three detector: H maps to UT4(F2).
U=sp.eye(4);TA=U.copy();TA[0,1]=1;TC=U.copy();TC[1,2]=1;TB=U.copy();TB[2,3]=1
finitegens=[TB,TA,TA*TB,TC,TA,TA*TC,TC,TB,TB*TC]
finite=U.copy()
for i,s in reduced:finite=(finite*(finitegens[i]**s)).applyfunc(lambda z:z%2)
expected=U.copy();expected[0,3]=1
assert finite==expected
print('Finite UT4(F2) target of cubic u: I+E14 (NONIDENTITY)')

