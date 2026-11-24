import itertools,json,time
from pathlib import Path
out=[]
for t in range(2,7):
 # Cyclic orientation, tie in even order resolved by numerical order.
 arcs={(i,j) for i in range(t) for j in range(t) if i!=j and ((j-i)%t<t/2 or ((j-i)%t==t/2 and i<j))}
 assert len(arcs)==t*(t-1)//2
 indeg=[sum((j,i) in arcs for j in range(t)) for i in range(t)]
 cores=[];last=0
 for x in indeg:
  cores.append(tuple(range(last,last+x+1)));last+=x+1
 n=last;fam=[]
 for i in range(t):
  targets=[j for j in range(t) if (i,j) in arcs]
  for values in itertools.product(*(cores[j] for j in targets)):
   F=frozenset(cores[i]+values);assert len(F)==t
   fam.append((i,F,sum(1<<v for v in F)))
 assert all(A&B for _,A,_ in fam for _,B,_ in fam)
 count=0
 for C in itertools.combinations(range(n),t-1):
  mask=sum(1<<v for v in C)
  assert any(not (mask&m) for _,_,m in fam)
  count+=1
 out.append(dict(t=t,k=t,n=n,members=len(fam),deficits=[t-len(X) for X in cores],sum_deficits=sum(t-len(X) for X in cores),checked_covers=count))
print(json.dumps(out,indent=2))
Path('workspace/agent3_rank_t_tournament_checks.json').write_text(json.dumps(out,indent=2))
