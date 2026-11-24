import itertools, time
import z3

def check_q(n,t):
 S=list(itertools.product(range(2),range(3)))
 sl=lambda x,y:x==y or (x[0]==0 and y[0]==1 and x[1]!=y[1])
 Q=[frozenset([i]) for i in range(n)]+[frozenset(e) for e in itertools.combinations(range(n),2)]
 E=list(itertools.product(S,Q));N=len(E)
 mat=[[sl(a[0],b[0]) and a[1]<=b[1] for b in E] for a in E]
 cp=[]
 for i in range(N):
  for j in range(N):
   if mat[i][j] or mat[j][i]:continue
   if all(h==i or not mat[h][i] or mat[h][j] for h in range(N)) and all(h==j or not mat[j][h] or mat[i][h] for h in range(N)):cp.append((i,j))
 so=z3.Solver();so.set(timeout=100000)
 rr=[[z3.Int(f'r{k}_{i}') for i in range(N)] for k in range(t)]
 lt=[(i,j) for i in range(N) for j in range(N) if i!=j and mat[i][j]]
 for r in rr:so.add([r[i]<r[j] for i,j in lt])
 for i,j in cp:so.add(z3.Or([r[i]>r[j] for r in rr]))
 st=time.time();ans=so.check();print(n,N,t,len(cp),ans,time.time()-st,flush=True)
 if ans==z3.sat:
  m=so.model();ranks=[[m.eval(r).as_long() for r in row] for row in rr]
  # independently check that each row isotone and all incomparable pairs are separated
  for i in range(N):
   for j in range(N):
    assert mat[i][j] == all(row[i]<=row[j] for row in ranks)
  print('Embedding independently verified on all ordered pairs',N*N,flush=True)
for n,t in [(3,3),(4,3),(5,4),(6,4)]:check_q(n,t)
