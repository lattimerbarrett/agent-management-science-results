import z3,itertools,time,json

def data(E,le):
 N=len(E)
 lows=[];ups=[0]*N
 for i,x in enumerate(E):
  lows.append(sum(1<<j for j,y in enumerate(E) if i!=j and le(y,x)))
  for j,y in enumerate(E):
   if i!=j and le(x,y):ups[i]|=1<<j
 cp=[];covers=[]
 for i in range(N):
  for j in range(N):
   if i==j:continue
   if (ups[i]>>j)&1:
    if not ups[i]&lows[j]:covers.append((i,j))
   elif not (ups[j]>>i)&1 and lows[i]&~lows[j]==0 and ups[j]&~ups[i]==0:cp.append((i,j))
 return cp,covers,lows,ups

def solve(E,le,t,tm=15000):
 st=time.time();cp,covers,lo,up=data(E,le)
 N=len(E);s=z3.Solver();s.set(timeout=tm)
 R=[[z3.Int(f'r{k}_{i}') for i in range(N)] for k in range(t)]
 for row in R:
  s.add([row[i]<row[j] for i,j in covers])
 for i,j in cp:s.add(z3.Or([row[i]>row[j] for row in R]))
 ans=s.check();print('solve',N,t,len(cp),len(covers),ans,'elapsed',time.time()-st,flush=True)
 if ans==z3.sat:
  m=s.model();rr=[[m.eval(x).as_long() for x in row] for row in R]
  for i in range(N):
   for j in range(N):assert (i==j or (up[i]>>j)&1)==all(row[i]<=row[j] for row in rr)
  return str(ans),rr
 return str(ans),None
S=list(itertools.product(range(2),range(3)))
sl=lambda x,y:x==y or (x[0]==0 and y[0]==1 and x[1]!=y[1])
for n in [9,10,12,14,16,20]:
 Q=list(itertools.combinations(range(n),2));ql=lambda x,y:x==y or x[1]<y[0]
 ans,rr=solve(Q,ql,3,20000)
 if ans=='unsat':
  ans4,r4=solve(Q,ql,4,10000)
  E=list(itertools.product(S,Q));ansp,rp=solve(E,lambda a,b:sl(a[0],b[0]) and ql(a[1],b[1]),4,60000)
  if ansp=='sat':
   json.dump({'n':n,'ranks':rp},open('interval_counterexample.json','w'));break
