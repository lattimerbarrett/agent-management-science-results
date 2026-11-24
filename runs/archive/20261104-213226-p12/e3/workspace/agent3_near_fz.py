import pickle,json
s=open('workspace/agent3_fz25.py').read().replace('for i in range(10):','for i in range(12):').replace('for n in range(11)','for n in range(13)')
s=s[:s.index('json.dump(')]
exec(compile(s,'near_fz.py','exec'))
assert P==1000000007
# exact 56x44 pairing transformed mod P
AQ=pickle.load(open('workspace/pairing25_free_exact_agent4.pkl','rb'))
A=[[int(v.numerator)*pow(int(v.denominator),-1,P)%P for v in row] for row in AQ]
rr=[];pp=[]
for row in rows:
 a=row[:]
 for piv,b in zip(pp,rr):
  c=a[piv]
  if c:a=[(x-c*y)%P for x,y in zip(a,b)]
 piv=next((i for i,x in enumerate(a) if x),None)
 if piv is not None:
  c=pow(a[piv],-1,P);a=[x*c%P for x in a];pp.append(piv);rr.append(a)
assert pp==list(range(33))
near=[];labels=[];images=[]
for sig in sigmas:
 if sum(sig)!=12:continue
 a=[0]*77
 for k,v in E[sig].items():
  if sum(k)==12:a[idx[k]]=v
 for piv,b in zip(pp,rr):
  c=a[piv]
  if c:a=[(x-c*y)%P for x,y in zip(a,b)]
 v=a[33:];image=[sum(x*y for x,y in zip(v,b))%P for b in A]
 near.append(v);images.append(image);labels.append(sig)
 print('sigma',sig,'quotientterms',sum(bool(x) for x in v),'pairingterms',sum(bool(x) for x in image))
# Find linear combinations of images zero using row elimination tracking
n=len(labels);rr=[];pp=[];relations=[]
for rowno,image in enumerate(images):
 a=image[:];comb=[0]*n;comb[rowno]=1
 for piv,b,cmb in zip(pp,rr,relations):
  c=a[piv]
  if c:a=[(x-c*y)%P for x,y in zip(a,b)];comb=[(x-c*y)%P for x,y in zip(comb,cmb)]
 piv=next((i for i,x in enumerate(a) if x),None)
 if piv is not None:
  c=pow(a[piv],-1,P);a=[x*c%P for x in a];comb=[x*c%P for x in comb];pp.append(piv);rr.append(a);relations.append(comb)
 else:
  radical=[sum(comb[k]*near[k][j] for k in range(n))%P for j in range(44)]
  print('NEAR COMBINATION',rowno,'nonzero quotient',sum(bool(x) for x in radical),'support',[(labels[k],c) for k,c in enumerate(comb) if c])
print('near count',n,'pairing-image rank',len(pp))
