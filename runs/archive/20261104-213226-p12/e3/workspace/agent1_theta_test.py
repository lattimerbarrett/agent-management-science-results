import math,json,time
from collections import defaultdict
P=1000000007; A=B=7; R=A+B+12
inv2=pow(2,-1,P)
fact=[1]*(R+1)
for i in range(1,R+1):fact[i]=fact[i-1]*i%P
ifact=[pow(x,-1,P) for x in fact]
def conv(a,b):
 c=[0]*(R+1)
 for i,x in enumerate(a):
  if x:
   for j,y in enumerate(b[:R+1-i]):
    if y:c[i+j]=(c[i+j]+x*y)%P
 return c
F={}; Q={}; C={}
for s in range(A+B+1):
 for p in range(max(0,s-B),min(A,s)+1):
  q=s-p; c=(p-q)**2*inv2%P; z=ifact[p]*ifact[q]%P
  F[p,q]=[z*pow(c,r,P)*ifact[r]%P for r in range(R+1)]
  if not s:continue
  v=F[p,q][:];den=p or q
  for a in range(p+1):
   for b in range(q+1):
    w=a if p else b
    if not w or (a,b)==(p,q):continue
    co=w*pow(den,-1,P)%P
    d=conv(Q[a,b],F[p-a,q-b])
    v=[(x-co*y)%P for x,y in zip(v,d)]
  Q[p,q]=v
  C[p,q]={(() if m==0 else (m,)):((-1)**(s-1)*v[s+m]*(48 if m==0 else 1))%P for m in range(13)}
E={(0,0):{():1}}
for s in range(1,A+B+1):
 for p in range(max(0,s-B),min(A,s)+1):
  q=s-p;den=p or q; out=defaultdict(int)
  for a in range(p+1):
   for b in range(q+1):
    w=a if p else b
    if not w:continue
    co=w*pow(den,-1,P)%P
    for k,x in C[a,b].items():
     for l,y in E[p-a,q-b].items():
      if sum(k)+sum(l)<=12:
       mon=tuple(sorted(k+l));out[mon]=(out[mon]+co*x*y)%P
  E[p,q]={k:v for k,v in out.items() if v}
rel={k:v for k,v in E[A,B].items() if sum(k)==12}
print('theta relation',len(rel))
fz=json.load(open('workspace/agent2_fz25.json')); mons=list(map(tuple,fz['monomials']));basis={}
for row in fz['rows']:
 row=row[:]
 for j,c in enumerate(row):
  c=row[j]
  if not c:continue
  if j in basis:row=[(a-c*b)%P for a,b in zip(row,basis[j])]
  else:basis[j]=[a*pow(c,-1,P)%P for a in row];break
row=[rel.get(m,0) for m in mons]
for j in range(len(row)):
 if row[j] and j in basis:
  c=row[j];row=[(a-c*b)%P for a,b in zip(row,basis[j])]
print('FZ remainder nonzero',sum(bool(v) for v in row))
json.dump({'prime':P,'monomials':mons,'relation':[rel.get(m,0) for m in mons],'remainder':row},open('workspace/agent1_theta_relation.json','w'))
