from itertools import combinations, product
from collections import defaultdict
from sympy import Matrix, ZZ
from sympy.matrices.normalforms import smith_normal_form
import json,time,os

def comm(u,v):
    out=defaultdict(int)
    for a,x in u.items():
      for b,y in v.items():out[a+b]+=x*y;out[b+a]-=x*y
    return {a:x for a,x in out.items() if x}
def add(a,b,sgn=1):
    c=defaultdict(int,a)
    for w,v in b.items():c[w]+=sgn*v
    return {w:v for w,v in c.items() if v}
def apply(D, wordpoly):
    i,p=D;out=defaultdict(int)
    for w,c in wordpoly.items():
      for k,j in enumerate(w):
        if i==j:
          for v,d in p.items():out[w[:k]+v+w[k+1:]]+=c*d
    return {w:c for w,c in out.items() if c}
def bracket(D,E):
    i,p=D;j,q=E
    out={}
    for w,c in apply(D,q).items():out[(j,)+w]=c
    for w,c in apply(E,p).items():out[(i,)+w]=out.get((i,)+w,0)-c
    return {w:c for w,c in out.items() if c}
def compute(n):
    basis=[(i,comm({(j,):1},{(k,):1})) for i in range(n) for j,k in combinations(range(n),2)]
    rows=list(product(range(n),repeat=4));idx={w:i for i,w in enumerate(rows)}
    cols=[bracket(D,E) for D,E in combinations(basis,2)]
    M=Matrix(len(rows),len(cols),lambda i,j:cols[j].get(rows[i],0))
    # Check Morita trace contracts the dual index against the first tensor letter,
    # then symmetrizes the other two letters.
    for col in cols:
      trace=defaultdict(int)
      for (i,a,b,c),v in col.items():
        if i==a:trace[tuple(sorted((b,c)))]+=v
      assert not any(trace.values())
    S=smith_normal_form(M,domain=ZZ)
    inv=[abs(int(S[i,i])) for i in range(min(S.shape)) if S[i,i]]
    expected=n*(n**3-n)//3-n*(n+1)//2
    assert len(inv)==expected,(n,len(inv),expected)
    assert all(x==1 for x in inv), (n,inv)
    return dict(n=n,degree_one_rank=len(basis),columns=len(cols),tensor_rows=len(rows),bracket_rank=len(inv),nonzero_smith_invariants=sorted(set(inv)),trace_vanishes=True)
if __name__=='__main__':
  out=[]
  for n in range(2,6):
    t=time.time();r=compute(n);r['seconds']=time.time()-t;out.append(r);print(r,flush=True)
  os.makedirs('workspace',exist_ok=True)
  with open('workspace/agent4_degree2_checks.json','w') as f:json.dump(out,f,indent=2)
  with open('workspace/agent4_degree2_checks.py','w') as f:f.write(open(__file__).read())
