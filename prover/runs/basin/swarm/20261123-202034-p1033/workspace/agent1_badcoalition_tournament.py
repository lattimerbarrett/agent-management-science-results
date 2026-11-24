import itertools,json,time
from pathlib import Path
st=time.time(); r=7; N=2*r-1; v=N-1
Q={1,2,4}
def beats(a,b):return (b-a)%r in Q
edges=[]; classes=[[] for _ in range(r)]
for E in itertools.combinations(range(N),r):
 S=[a for a in E if a<r]
 opts=S if len(S)==1 else [a for a in S if any(beats(b,a) for b in S if b!=a)]
 i=min(opts); e=sum(1<<x for x in E); classes[i].append(e); edges.append(e)
assert all(classes)
for i,cl in enumerate(classes):
 core=(1<<N)-1
 for e in cl:core&=e
 assert core==1<<i
zero=[[e for e in cl if not(e>>v&1)] for cl in classes]
# All possible covers C of v-free edges: masks on N-1 vertices.
cover_cost=[N]* (1<<r)
for C in range(1<<(N-1)):
 A=sum(1<<i for i,cl in enumerate(zero) if all(e&C for e in cl))
 c=C.bit_count(); sub=A
 while True:
  cover_cost[sub]=min(cover_cost[sub],c)
  if not sub:break
  sub=(sub-1)&A
bad=[I for I in range(1,1<<r) if cover_cost[I]<I.bit_count()]
minimal=[I for I in bad if not any(J!=I and J&I==J for J in bad)]
lam=min(T.bit_count() for T in range(1<<r) if all(T&I for I in minimal))
gamma=min(T.bit_count() for T in range(1<<r) if all(any((T>>b&1) and (b==a or beats(b,a)) for b in range(r)) for a in range(r)))
assert gamma==3 and lam>=gamma
Ias=[sum(1<<b for b in range(r) if b==a or beats(b,a)) for a in range(r)]
assert all(I in bad for I in Ias)
assert all(I&J for I in minimal for J in minimal)
out={'r':r,'n':N,'classes':[len(cl) for cl in classes], 'all_edges':len(edges),'minimal_bad_coalitions':[[i for i in range(r) if I>>i&1] for I in minimal], 'lambda':lam, 'tournament_domination':gamma,'seconds':time.time()-st}
Path('workspace/agent1_badcoalition_tournament.py').write_text(Path(__file__).read_text())
Path('workspace/agent1_badcoalition_tournament.json').write_text(json.dumps(out,indent=2))
print(json.dumps(out,indent=2))