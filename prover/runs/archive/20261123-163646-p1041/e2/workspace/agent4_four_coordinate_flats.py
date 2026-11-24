import z3
from itertools import combinations
K=4
MASK=(1<<K)-1
s=z3.Solver()
types=[]
for P in range(1<<K):
    comp=MASK^P
    for Q in range(1<<K):
        if Q&~comp:continue
        if comp and Q&(comp&-comp):continue
        types.append((P,Q))
n={T:z3.Int('n%d_%d'%T) for T in types}
for x in n.values():s.add(x>=0,x<=15)
for i in range(K):
    s.add(sum(x for (P,Q),x in n.items() if P&(1<<i))==7)
s.add(sum(n.values())<=15)
def pw(e):return sum(z3.If(e==i,1<<i,0) for i in range(8))
def intersection(S):
    e=sum(x for (P,Q),x in n.items() if P&S==S)
    conflicts=[]
    for (P,Q),x in n.items():
        fixed=S&~P
        if Q&fixed and ((MASK^Q)&fixed):conflicts.append(x)
    return z3.If(sum(conflicts)==0,pw(e),0)
w=128*K
for k in range(2,K+1):
    for ids in combinations(range(K),k):
        S=sum(1<<i for i in ids)
        w+=(-2)**(k-1)*intersection(S)
for target in [258,274,290,298,306,310,322,326,330,334]:
    s.push();s.add(w==target)
    s.set(timeout=60000)
    ans=s.check();print(target,ans,flush=True)
    assert ans==z3.unsat
    s.pop()
