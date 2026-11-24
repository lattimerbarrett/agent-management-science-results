import z3,itertools

def dimtest(E,le,t,tm=30000):
 N=len(E); mat=[[le(a,b) for b in E] for a in E]
 cp=[]
 for i in range(N):
  for j in range(N):
   if mat[i][j] or mat[j][i]:continue
   if all(h==i or not mat[h][i] or mat[h][j] for h in range(N)) and all(h==j or not mat[j][h] or mat[i][h] for h in range(N)):cp.append((i,j))
 so=z3.Solver();so.set(timeout=tm);rr=[[z3.Int(f'r{k}_{i}') for i in range(N)] for k in range(t)]
 lt=[(i,j) for i in range(N) for j in range(N) if i!=j and mat[i][j]]
 for r in rr:so.add([r[i]<r[j] for i,j in lt])
 for i,j in cp:so.add(z3.Or([r[i]>r[j] for r in rr]))
 ans=so.check();print(N,t,len(cp),ans,flush=True);return ans
S=list(itertools.product(range(2),range(3)))
sl=lambda x,y:x==y or (x[0]==0 and y[0]==1 and x[1]!=y[1])
for n in [5,6,7,8]:
 Q=list(itertools.combinations(range(n),2));ql=lambda x,y:x==y or x[1]<y[0]
 if dimtest(Q,ql,2)==z3.unsat:
  print('test product',n,flush=True)
  E=list(itertools.product(S,Q));dimtest(E,lambda a,b:sl(a[0],b[0]) and ql(a[1],b[1]),3)
