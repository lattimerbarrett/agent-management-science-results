import random,json,time
random.seed(911)
def prop(adj):
 n=len(adj);full=(1<<n)-1;ans=set()
 for B in range(1<<n):
  if any(adj[i]&B for i in range(n) if B>>i&1):continue
  A=full^B;todo=A; tri=c4=lin=claw=True
  while todo:
   q=todo&-todo;comp=0
   while q:
    b=q&-q;q^=b;i=b.bit_length()-1;comp|=b;q|=(adj[i]&A&~comp&~q)
   todo&=~comp;vs=[i for i in range(n) if comp>>i&1];d=[(adj[i]&comp).bit_count() for i in vs];s=len(vs);ed=sum(d)//2;md=max(d)
   tri &= s<=3 and md<=2
   c4 &= (s<=4 and md<=2 and ed<=s and not(s==3 and ed==3))
   lin &= md<=2 and ed<s
   claw &= s<=4 and ed==s-1 and (s<=3 or md==3)
  if tri:ans.add('tri')
  if c4:ans.add('c4')
  if lin:ans.add('lin')
  if claw:return None
 return ans
start=time.time()
for it in range(30000):
 n=random.randrange(8,13);a=(n-1)//2; adj=[0]*n; es=[]
 p=random.uniform(.25,.8)
 for i in range(a):
  for j in range(a,n-1):
   if random.random()<p:es.append((i,j))
 for i in range(n-1):
  if random.random()<random.uniform(.5,.95):es.append((i,n-1))
 for i,j in es:adj[i]|=1<<j;adj[j]|=1<<i
 ans=prop(adj)
 if ans and {'tri','c4','lin'}<=ans:
  print('FOUND',it,n,es,ans)
  import networkx as nx
  H=nx.Graph(es)
  for k in range(3,n+2):
   ok=False
   for B in range(1<<n):
    if any(adj[i]&B for i in range(n) if B>>i&1):continue
    A=[i for i in range(n) if not B>>i&1];R=H.subgraph(A)
    if all(max(dict(R.subgraph(c).degree()).values())<=2 and ((R.subgraph(c).number_of_edges()==len(c) and len(c)==k) or (R.subgraph(c).number_of_edges()==len(c)-1 and len(c)<=k)) for c in nx.connected_components(R)):
     ok=True;print('cycle',k,'witness A',A);break
   if not ok:print('cycle',k,'FAIL')
  break
else:print('no counterexample in',it+1,'trials')
print('elapsed',time.time()-start)
open('workspace/agent4_claw_search.py','w').write(open(__file__).read())
