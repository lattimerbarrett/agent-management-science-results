from itertools import combinations,product

def counter(t):
 k=2*t-1; petals=[];n=1
 for i in range(t):petals.append(set(range(n,n+k-1)));n+=k-1
 C={min(p) for p in petals};U=set(range(n,n+2*t-3));n+=2*t-3
 H=list(combinations(U,t-1))
 E=[{0}|p for p in petals]
 G=[]
 for a in product(*[tuple(p) for p in petals]):
  if len(set(a)&C)>=2:
   for h in H:G.append(set(a)|set(h))
 return k,n,C,E,G
for t in range(2,5):
 k,n,C,E,G=counter(t);F=E+G
 masks=[sum(1<<v for v in e) for e in F]
 assert all(len(e)==k for e in F)
 assert all(a&b for a in masks for b in masks)
 assert all(C&e for e in F)
 for a in combinations(range(n),t-1):
  m=sum(1<<v for v in a)
  assert any(not(m&e) for e in masks)
 S=[]
 for ci in C:
  Ci=C-{ci}
  sensitive={v for v in range(n) if all((Ci|{v})&e for e in F)}
  assert sensitive in E
  S.append(sensitive)
 assert len(set.union(*S))==t*k-t+1
 print(t,k,n,len(F),'sensitive-union deficit',t*k-len(set.union(*S)))
