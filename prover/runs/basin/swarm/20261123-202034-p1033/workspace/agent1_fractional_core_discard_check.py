from pathlib import Path
from itertools import combinations
import numpy as np,scipy.optimize as opt,json
n,m=8,2;T=n*m;c=T+1;r=n-2*m
es=list(combinations(range(n),2));idx={e:j for j,e in enumerate(es)};N=len(es)
rows=[]
for a in range(n):
 star=[idx[tuple(sorted((a,b)))] for b in range(n) if b!=a]
 for h in range(m):
  i=a*m+h
  for P in combinations(star,r):
   P=set(P);omit=[b for b in range(n) if b!=a and idx[tuple(sorted((a,b)))] not in P]
   target=[b*m+j for b in omit for j in range(m)]+[T]
   row=np.zeros(N+T+1);row[list(P)]=1;row[N+i]=1
   for j in target:row[N+j]=1/c
   rows.append(row)
row=np.zeros(N+T+1);row[N+T]=1;rows.append(row)
A=np.array(rows);res=opt.linprog(np.ones(N+T+1),A_ub=-A,b_ub=-np.ones(len(rows)),bounds=(0,None),method='highs')
assert res.success
W=res.fun;x=res.x
assert np.min(A@x)>1-1e-8
positive=[i for i in range(T+1) if x[N+i]>1e-8]
assert positive==[T]
# Removing the apex class and its target incidence leaves pureactual weight .8? here16/17.
actual_mins=min(sum(x[p] for p in range(N) if row[p]) for row in rows[:-1])
assert actual_mins<1-1e-5
expected=1+(1-1/c)*N/r
assert abs(W-expected)<1e-8
assert abs(actual_mins-(1-1/c))<1e-8
from fractions import Fraction as F
xp=[F(c-1,c*r)]*N+[F(0)]*T+[F(1)]
yp=[F(1,2*m*__import__('math').comb(n-2,r-1))]*(len(rows)-1)+[F(10,17)]
Ar=[[F(1) if a==1 else F(1,c) if a else F(0) for a in row] for row in rows]
assert all(sum(a*b for a,b in zip(row,xp))>=1 for row in Ar)
assert all(sum(Ar[i][j]*yp[i] for i in range(len(Ar)))<=1 for j in range(len(xp)))
assert sum(xp)==sum(yp)==F(129,17)
out=dict(old_t=T,new_t=T+1,core_size=c,patterns=len(rows),lp_value=W,exact_primal_dual=str(sum(xp)),expected_value=expected,positive_core_classes=positive,remaining_actual_min_pattern_weight=actual_mins,needed_scale=c/(c-1),global_fractional_bound=2*(r+m*(2*m-1)+1)+1)
print(json.dumps(out,indent=2))
Path('workspace/agent1_fractional_core_discard_check.json').write_text(json.dumps(out,indent=2))
Path('workspace/agent1_fractional_core_discard_check.py').write_text(Path('scratchpad.py').read_text())
