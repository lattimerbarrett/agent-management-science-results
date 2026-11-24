from pathlib import Path
code = r'''"""Exact finite-poset dimension certificates with z3 integer ranks.
A certificate is checked independently by ordinary Python comparisons.
"""
import z3

def relation_Q(n):
    elems=[(i,) for i in range(n)]+[(i,j) for i in range(n) for j in range(i+1,n)]
    return elems, [[set(x)<=set(y) for y in elems] for x in elems]

def relation_S(n, bounded=False):
    elems=[('a',i) for i in range(n)]+[('b',i) for i in range(n)]
    R=[[x==y or (x[0]=='a' and y[0]=='b' and x[1]!=y[1]) for y in elems] for x in elems]
    if bounded:
        elems=['0']+elems+['1']; N=len(elems)
        R=[[i==j or i==0 or j==N-1 or (0<i<N-1 and 0<j<N-1 and R[i-1][j-1]) for j in range(N)] for i in range(N)]
    return elems,R

def product(A,B):
    X,R=A;Y,S=B
    return [(x,y) for x in X for y in Y],[[R[i][k] and S[j][l] for k in range(len(X)) for l in range(len(Y))] for i in range(len(X)) for j in range(len(Y))]

def verify(R, orders):
    N=len(R)
    ranks=[]
    for order in orders:
        assert sorted(order)==list(range(N))
        ranks.append({x:i for i,x in enumerate(order)})
    assert ranks
    for x in range(N):
        for y in range(N):
            assert bool(R[x][y])==all(r[x]<=r[y] for r in ranks), (x,y)
    return True

def decide(R,t,timeout_ms=60000):
    N=len(R); sol=z3.Solver();sol.set(timeout=timeout_ms)
    a=[[z3.Int('r_%d_%d'%(k,x)) for x in range(N)] for k in range(t)]
    for k in range(t):
        sol.add(z3.Distinct(a[k]))
        for x in range(N):
            sol.add(a[k][x]>=0,a[k][x]<N)
            for y in range(N):
                if x!=y and R[x][y]:sol.add(a[k][x]<a[k][y])
    for x in range(N):
        for y in range(x):
            if not R[x][y] and not R[y][x]:
                sol.add(z3.Or([a[k][x]<a[k][y] for k in range(t)]))
                sol.add(z3.Or([a[k][y]<a[k][x] for k in range(t)]))
    status=sol.check()
    if status==z3.sat:
        model=sol.model()
        orders=[sorted(range(N),key=lambda x:model.eval(a[k][x]).as_long()) for k in range(t)]
        verify(R,orders)
        return 'sat',orders
    return str(status),None
'''
Path('workspace/agent4_dimension_sat.py').write_text(code)
import sys
sys.path.insert(0,'workspace')
from agent4_dimension_sat import *
for n,t in [(2,1),(2,2),(3,2),(3,3),(4,2),(4,3)]:
    _,R=relation_Q(n)
    status,orders=decide(R,t,10000)
    print('Q',n,'t',t,status)
    assert status==('sat' if t>= {2:2,3:3,4:3}[n] else 'unsat')
print('All base checks passed.')
def B(n):
    X=list(range(2**n)); return X,[[x&y==x for y in X] for x in X]
for n,m in [(2,3),(3,3),(3,4),(4,3)]:
    _,R=product(B(n),relation_Q(m))
    for t in range(max(n,3),n+4):
        status,orders=decide(R,t,20000)
        print('B',n,'x Q',m,'t',t,status,flush=True)
        if status=='sat':break
