from itertools import combinations,product
from pathlib import Path
import json,time
import z3

def tournament(t):
 out=[[] for _ in range(t)]
 for i,j in combinations(range(t),2):
  # cyclic regular for odd; nearly regular restriction for even
  n=t if t%2 else t+1
  a,b=(i,j) if (j-i)%n<=n//2 else (j,i)
  out[a].append(b)
 ind=[sum(i in out[j] for j in range(t)) for i in range(t)]
 cores=[];n=0
 for v in ind:cores.append(set(range(n,n+v+1)));n+=v+1
 classes=[]
 for i in range(t):
  classes.append([frozenset(cores[i]|set(p)) for p in product(*(cores[j] for j in out[i]))])
 return cores,classes,n

def check(t):
 start=time.time();X,H,n=tournament(t)
 ds=[t-len(x) for x in X];d=max(ds);k=t+2*d
 Y=[];N=n
 for di in ds:Y.append(set(range(N,N+k-2*di)));N+=k-2*di
 # All old points are actual copies 0..n-1. Reservoir used for q<di.
 Z=list(range(N,N+t+d));N+=len(Z)
 HH=[]
 for i,cl in enumerate(H):
  target=[]
  for F in cl:
   P=set(F)-X[i];owners=[j for j in range(t) if P&X[j]]
   for choices in product(*(Y[j] for j in owners)):
    for pad in combinations(Z,ds[i]-len(owners)):
     E=frozenset(Y[i]|P|set(choices)|set(pad));assert len(E)==k
     target.append(E)
  HH.append(list(set(target)))
 E=[e for cl in HH for e in cl]
 assert len(set(E))==len(E)
 for i,F in enumerate(E):
  assert all(F&G for G in E[:i])
 assert all(Y[i]<=e and len(e-Y[i])==2*ds[i] for i,cl in enumerate(HH) for e in cl)
 assert all(not(Y[i]&Y[j]) for i,j in combinations(range(t),2))
 s=z3.Solver();s.set(timeout=60000);v=[z3.Bool('v%d_%d'%(t,i)) for i in range(N)]
 s.add(z3.PbLe([(q,1) for q in v],t-1))
 for e in E:s.add(z3.Or([v[p] for p in e]))
 status=str(s.check());assert status=='unsat'
 canonical={min(y) for y in Y};assert all(e&canonical for e in E)
 return dict(t=t,old_n=n,old_core_sizes=list(map(len,X)),old_class_sizes=list(map(len,H)),old_deficits=ds,k=k,s=k-t,new_core_sizes=list(map(len,Y)),new_class_sizes=list(map(len,HH)),new_n=N,new_edges=len(E),intersection_pairs=len(E)*(len(E)-1)//2,small_cover_status=status,seconds=time.time()-start)
results=[check(t) for t in (3,4,5)]
# Exercise padding branch: six Fano lines, cores singleton 0,1,2,
# petals consist only of external actual points 3,4,5,6.
X=[{0},{1},{2}];old=[[{0,3,6},{0,4,5}],[{1,3,5},{1,4,6}],[{2,3,4},{2,5,6}]]
Y=[set(range(7+3*i,10+3*i)) for i in range(3)];Z=set(range(16,21));E=[]
for i in range(3):
 for f in old[i]:
  for pad in combinations(Z,2):
   e=frozenset(Y[i]|(f-X[i])|set(pad));assert len(e)==7;E.append(e)
assert all(F&G for j,F in enumerate(E) for G in E[:j])
v=[z3.Bool('fano_%d'%i) for i in range(21)];sol=z3.Solver();sol.add(z3.PbLe([(p,1) for p in v],2))
for f in E:sol.add(z3.Or([v[p] for p in f]))
assert str(sol.check())=='unsat'
results.append(dict(case='Fano six lines padding branch',t=3,k=7,new_core_sizes=[3,3,3],new_deficits=[4,4,4],old_petals_rank=2,target_owners_per_petal=0,padding_per_petal=2,new_edges=len(E),intersection_pairs=len(E)*(len(E)-1)//2,small_cover_status='unsat'))
print(json.dumps(results,indent=2))
Path('workspace/agent3_rank_excess_normalization_checks.json').write_text(json.dumps(results,indent=2))
Path('workspace/agent3_rank_excess_normalization_checks.py').write_text(Path('scratchpad.py').read_text())
Path('workspace/agent3_rank_excess_normalization_proof.txt').write_text('''RANK-EXCESS NORMALIZATION (agent_1 idea, independent formalization)
Given valid t-class configuration with deficits d_i<=d, make actual copies v* of EVERY original point v. Let k'=t+2d. Choose fresh disjoint cores Y_i of size k'-2d_i>=t, and a fresh padding reservoir Z of size t+d. For each original petal P=F\\X_i, |P|=d_i, let J(P)={j:P intersects X_j}; q=|J(P)|<=d_i. Include in new class i ALL sets Y_i union {v*:v in P} union {y_j:j in J(P)} union B, with arbitrary y_j in Y_j and arbitrary B subset Z of size d_i-q. Every member has size |Y_i|+d_i+q+(d_i-q)=k', and new deficit exactly 2d_i. Distinct classes cannot share a member: a class-i member contains at most ONE point of any foreign core Y_j, whereas class-j members contain all |Y_j|>=t>=2 points.
Intersection: same-class members share Y_i. For different original edges F in class i and G in class j, take any p in F cap G. If p belongs to both petals, actual copy p* is shared. Otherwise p belongs to X_i and G's petal (or symmetrically), so i in J(G), and G's new member contains a target choice in Y_i, wholly contained in F's new member.
Cover: one arbitrary point of each Y_i is a t-cover. Suppose C has size<t and covers the new family. Let I={i:C misses Y_i}. For any original petal P from an i in I disjoint from C's actual projection, choose every target choice y_j outside C (possible since |Y_j|>=t), and padding B outside C (possible since |Z\\C|>=d+1>=d_i-q). This gives a new member disjoint C, contradiction. Hence the actual projection of C covers ALL original petals of colors I. Petal Hall tau(union petals of I)>=|I| implies C contains at least |I| actual points. C also contains at least t-|I| core points, in disjoint reservoirs, contradiction. Thus tau=t. Each class is nonempty because every original class is nonempty and all choice reservoirs are large enough. The generated classes are disjoint by the foreign-core observation above.
Total deficit doubles exactly. Rank excess k'-t=2d. This reduction applies after selecting the low-deficit half of classes; any class subunion has cover number equal to its number of classes.
''')
