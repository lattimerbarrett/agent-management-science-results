import random,itertools,z3,time,json
random.seed(154)
def solve(mat,t,timeout=2000):
 N=len(mat)
 lows=[{h for h in range(N) if h!=i and mat[h][i]} for i in range(N)]
 ups=[{h for h in range(N) if h!=i and mat[i][h]} for i in range(N)]
 cp=[(i,j) for i in range(N) for j in range(N) if not mat[i][j] and not mat[j][i] and lows[i]<=lows[j] and ups[j]<=ups[i]]
 s=z3.Solver();s.set(timeout=timeout)
 R=[[z3.Int(f'x{l}_{i}') for i in range(N)] for l in range(t)]
 for row in R:
  s.add([row[i]<row[j] for i in range(N) for j in range(N) if i!=j and mat[i][j]])
 for i,j in cp:s.add(z3.Or([row[i]>row[j] for row in R]))
 ans=s.check()
 if ans==z3.sat:
  m=s.model();rr=[[m.eval(x).as_long() for x in row] for row in R]
  assert all(mat[i][j]==all(row[i]<=row[j] for row in rr) for i in range(N) for j in range(N))
  return 'sat',rr
 return str(ans), None
count=0
for trial in range(2000):
 n=5
 p=random.uniform(.35,.8)
 adj=[[random.random()<p for j in range(n)] for i in range(n)]
 mat=[[i==j or (i<n and j>=n and adj[i][j-n]) for j in range(2*n)] for i in range(2*n)]
 ans,_=solve(mat,3)
 if ans!='unsat':continue
 d4,_=solve(mat,4)
 if d4!='sat':continue
 count+=1
 E=list(itertools.product(range(6),range(2*n)))
 pm=[[ (a==c or (a<3 and c>=3 and a!=c-3)) and mat[b][d] for c,d in E] for a,b in E]
 ans,rr=solve(pm,4,3000)
 print(trial,count,ans,flush=True)
 if ans=='sat':
  json.dump({'mat':mat,'ranks':rr},open('counterexample.json','w'));break
 if count>=50:break
print('finished',count)
