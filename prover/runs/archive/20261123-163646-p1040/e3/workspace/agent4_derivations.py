import sys
sys.path.insert(0,'workspace')
from agent4_tensor import *
from itertools import combinations

def action(D,p):
    ans={}
    for w,c in p.items():
        for k,x in enumerate(w):
            for v,a in D[x-1].items():
                term=w[:k]+v+w[k+1:]
                ans[term]=ans.get(term,0)+c*a
    return {w:c for w,c in ans.items() if c}

def deriv_bracket(D,E): return tuple(add(action(D,e),action(E,d),-1) for d,e in zip(D,E))
def generators(n):
    out=[]
    for i in range(n):
        for j in range(n):
            if i==j: continue
            D=[{} for _ in range(n)]; D[i]={(j+1,i+1):1,(i+1,j+1):-1}; out.append(tuple(D))
        for j,k in combinations([j for j in range(n) if j!=i],2):
            D=[{} for _ in range(n)]; D[i]={(j+1,k+1):1,(k+1,j+1):-1}; out.append(tuple(D))
    return out

def independent(ds,p=1000003):
    rows={}; basis=[]
    for D in ds:
        v={(i,w):c%p for i,a in enumerate(D) for w,c in a.items() if c%p}
        while v:
            pivot=min(v)
            if pivot in rows:
                factor=v[pivot]
                for k,c in rows[pivot].items():
                    v[k]=(v.get(k,0)-factor*c)%p
                    if not v[k]: del v[k]
            else:
                inv=pow(v[pivot],-1,p)
                rows[pivot]={k:c*inv%p for k,c in v.items()}
                basis.append(D)
                break
    return basis
