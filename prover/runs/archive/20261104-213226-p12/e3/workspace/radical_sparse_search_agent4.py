import json,random,time,math
F={};src=open('workspace/agent3_fz25.py').read();src=src[:src.index('json.dump(dict')].replace('P=1000000007;','P=1000003;');exec(src,F)
P=1000003;B=F['basis'];rows=F['rows'];rd=json.load(open('workspace/radical25_agent4.json'));v=[0]*77
for b,c in zip(rd['basis'],rd['coefficients']):v[B.index(tuple(b))]=c%P

def reduce(order):
 A=[r[:] for r in rows];w=v[:];rank=0
 for j in order:
  i=next((i for i in range(rank,len(A)) if A[i][j]),None)
  if i is None:continue
  A[rank],A[i]=A[i],A[rank];inv=pow(A[rank][j],-1,P);row=[x*inv%P for x in A[rank]];A[rank]=row
  for k in range(rank+1,len(A)):
   a=A[k][j]
   if a:A[k]=[(x-a*y)%P for x,y in zip(A[k],row)]
  a=w[j]
  if a:w=[(x-a*y)%P for x,y in zip(w,row)]
  rank+=1
  if rank==33:break
 return sum(bool(x) for x in w),w
orders=[]
for key in [lambda b:len(b),lambda b:max(b),lambda b:b.count(1),lambda b:sum(x*x for x in b),lambda b:b]:
 for rev in [False,True]:orders.append(sorted(range(77),key=lambda i:key(B[i]),reverse=rev))
random.seed(783)
for _ in range(300):
 order=list(range(77));random.shuffle(order);orders.append(order)
best=77;start=time.time()
for k,order in enumerate(orders):
 n,w=reduce(order)
 if n<best:
  best=n;bestorder=order[:];print('best',best,'at',k,'time',time.time()-start,flush=True)
print('support',[B[i] for i,x in enumerate(w) if x])
json.dump({'order':bestorder,'support':best},open('workspace/radical_sparse_order_agent4.json','w'))
