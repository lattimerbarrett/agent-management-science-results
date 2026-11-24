import json,math
P=1000000007;G=25;PSI=(0,-2)
def parts(n,lo=1):
 if n==0:yield ()
 for i in range(lo,n+1):
  for t in parts(n-i,i):yield(i,)+t

def convert(filename,psimul):
 data=json.load(open(filename));ans={}
 for mon,c in data:
  poly={((),psimul):c}
  for i,j in mon:
   assert i==0
   fac={}
   if (i,j)==PSI:fac[((),1)]=1
   else:
    assert j%2==0;d=j//2;fac[((),d)]=1
    for a in range(1,d+2):
     k=a-1;b=d+1-a;coeff=math.comb(d+1,a)*pow(2,-d-1,P)%P
     if k:fac[((k,),b)]=coeff
     else:fac[((),b)]=(fac.get(((),b),0)+48*coeff)%P
   out={}
   for (mon1,b1),c1 in poly.items():
    for (mon2,b2),c2 in fac.items():
     key=(tuple(sorted(mon1+mon2)),b1+b2);out[key]=(out.get(key,0)+c1*c2)%P
   poly=out
  for (mon,b),c in poly.items():
   if b==0:continue
   k=b-1;dest=tuple(sorted(mon+(k,))) if k else mon
   ans[dest]=(ans.get(dest,0)+c*(1 if k else 48))%P
 return {k:v for k,v in ans.items() if v}
D=json.load(open('workspace/agent3_fz25.json'))
assert D['p']==P
basis=[tuple(m) for m in D['basis']];idx={m:i for i,m in enumerate(basis)}
rows=D['rows'];rref=[];pivs=[]
for row in rows:
 a=row[:]
 for piv,b in zip(pivs,rref):
  c=a[piv]
  if c:a=[(x-c*y)%P for x,y in zip(a,b)]
 piv=next((i for i,x in enumerate(a) if x),None)
 if piv is not None:
  c=pow(a[piv],-1,P);a=[x*c%P for x in a];pivs.append(piv);rref.append(a)
for n in [18,24]:
 r=n//2
 for psimul in range(0,14-r):
  rel=convert(f'workspace/agent3_jacobian_p31_{n}.json',psimul)
  degree=r+psimul-1
  for multiplier in parts(12-degree):
   a=[0]*77
   for mon,c in rel.items():a[idx[tuple(sorted(mon+multiplier))]]=c
   for piv,b in zip(pivs,rref):
    c=a[piv]
    if c:a=[(x-c*y)%P for x,y in zip(a,b)]
   nz=sum(bool(x) for x in a)
   print('n',n,'psimul',psimul,'multiplier',multiplier,'relationterms',len(rel),'remainderterms',nz)
