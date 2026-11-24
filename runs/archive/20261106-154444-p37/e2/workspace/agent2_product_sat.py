import z3
from itertools import combinations

def test(n,r,t,timeout=60000):
    Q=[1<<i for i in range(n)]+[(1<<i)|(1<<j) for i,j in combinations(range(n),2)]
    els=[(p,a) for p in range(1<<r) for a in Q];N=len(els)
    le=[[p&q==p and a&b==a for q,b in els] for p,a in els]
    cp=[]
    for x in range(N):
      for y in range(N):
        if le[x][y] or le[y][x]:continue
        if all(not(le[z][x] and z!=x) or le[z][y] for z in range(N)) and all(not(le[y][z] and z!=y) or le[x][z] for z in range(N)):cp.append((x,y))
    ranks=[[z3.Int(f'r_{i}_{x}') for x in range(N)] for i in range(t)]
    s=z3.Solver();s.set(timeout=timeout)
    for row in ranks:
      s.add(z3.Distinct(row))
      s.add(*[z3.And(x>=0,x<N) for x in row])
      s.add(*[row[x]<row[y] for x in range(N) for y in range(N) if x!=y and le[x][y]])
    s.add(*[z3.Or(*[row[x]>row[y] for row in ranks]) for x,y in cp])
    typeII=[(x,y) for x,y in cp if els[x][0]==0 and els[y][0]==(1<<r)-1]
    for i in range(t):
      s.add(z3.Or(*[z3.And(ranks[i][x]>ranks[i][y],*[ranks[j][x]<ranks[j][y] for j in range(t) if j!=i]) for x,y in typeII]))
    # symmetry: assign first t clique critical pairs distinct colors if possible
    # Solver's critical-pair reversal criterion is checked against full realizer if SAT.
    ans=s.check();print(dict(n=n,r=r,t=t,elements=N,critical_pairs=len(cp),result=str(ans)),flush=True)
    if ans==z3.sat:
      m=s.model(); rr=[[m[x].as_long() for x in row] for row in ranks]
      assert all(le[x][y]==all(row[x]<=row[y] for row in rr) for x in range(N) for y in range(N))
      return rr
    return str(ans)
if __name__=='__main__':test(5,3,5,timeout=30000)
