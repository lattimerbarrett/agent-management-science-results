import random,json,time
random.seed(912)
def prop(adj):
 n=len(adj);full=(1<<n)-1;ans=set()
 # enumerate independent sets by include/exclude recursion, avoid full 2^n scan
 def rec(todo,B):
  if not todo:
   yield B;return
  b=todo&-todo;i=b.bit_length()-1
  yield from rec(todo^b,B)
  yield from rec(todo&~b&~adj[i],B|b)
 for B in rec(full,0):
  A=full^B;todo=A;tri=c4=lin=p4=True
  while todo:
   q=todo&-todo;comp=0
   while q:
    b=q&-q;q^=b;i=b.bit_length()-1;comp|=b;q|=(adj[i]&A&~comp&~q)
   todo&=~comp;vs=[i for i in range(n) if comp>>i&1];d=[(adj[i]&comp).bit_count() for i in vs];s=len(vs);ed=sum(d)//2;md=max(d)
   tri &= s<=3 and md<=2
   c4 &= (s<=4 and md<=2 and ed<=s and not(s==3 and ed==3))
   lin &= md<=2 and ed<s
   p4 &= s<=4 and md<=2 and ed<s
  if tri:ans.add('tri')
  if c4:ans.add('c4')
  if lin:ans.add('lin')
  if p4:return None
 return ans
start=time.time(); count=100000
for it in range(count):
 n=random.randrange(10,17);a=(n-1)//2; adj=[0]*n; es=[]
 p=random.uniform(.2,.8)
 for i in range(a):
  for j in range(a,n-1):
   if random.random()<p:es.append((i,j))
 for i in range(n-1):
  if random.random()<random.uniform(.5,.95):es.append((i,n-1))
 for i,j in es:adj[i]|=1<<j;adj[j]|=1<<i
 ans=prop(adj)
 if ans and {'tri','c4'}<=ans:
  print('FOUND',it,n,es,ans);break
else:print('no counterexample in',it+1,'trials')
print('elapsed',time.time()-start)
open('workspace/agent4_p4_search.py','w').write(open(__file__).read())
