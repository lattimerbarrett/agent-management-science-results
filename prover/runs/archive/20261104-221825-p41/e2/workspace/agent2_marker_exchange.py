import json,itertools,time,z3
M=[tuple(x) for x in json.load(open('workspace/agent2_orbit_shelling.json'))['markers']];rank={x:i for i,x in enumerate(M)}
n=8;m=z3.Int('m');a=[z3.Int('a%d'%i) for i in range(n)];b=[z3.Int('b%d'%i) for i in range(n)]
def support(Q):return Q[1:3] if Q[0]=='e' else Q[1:4]
def valid(Q,c):
 S=support(Q);L=[c[i]>=1 if i in S else c[i]==0 for i in range(n)]
 if Q[0]=='e':L += [c[i]>=2 for i in S]
 else:
  p=Q[-1];L += [c[p]>=2]
  for i in S:
   if rank[('t',)+S+(i,)]<rank[Q]:L += [c[i]==1]
 return z3.And(*L)
def lexless_counts(c,d):
 return z3.Or(*[z3.And(*(c[j]==d[j] for j in range(i)),c[i]>d[i]) for i in range(n)])
def earlier_same(Q,c,d):
 if Q[0]=='e':return lexless_counts(c,d)
 p=Q[-1];return z3.Or(c[p]>d[p],z3.And(c[p]==d[p],lexless_counts(c,d)))
start=time.time();checked=0
for rf,F in enumerate(M):
 S=support(F)
 base=[m>=2,sum(a)==m+2,sum(b)==m+2,*[z3.And(x>=0,x<=m) for x in a+b],valid(F,a)]
 earlier_swaps={}
 for i in S:
  opts=[]
  for j in range(n):
   if i==j:continue
   c=[a[k]-(1 if k==i else 0)+(1 if k==j else 0) for k in range(n)]
   candidates=[]
   for rh,H in enumerate(M[:rf+1]):
    U=support(H)
    if not set(U)<=set(S)|{j}:continue
    # any old positive coordinate other than i persists
    if not (set(S)-{i})<=set(U):continue
    if j not in U:continue
    if rh==rf:
     # Cross-origin lex order depends only on which origins exchanged.
     if F[0]=='e':sameearlier=(j<i)
     else:
      p=F[-1];sameearlier=(j==p) or (i!=p and j!=p and j<i)
     if not sameearlier:continue
    candidates.append(valid(H,c))
   opts.append(z3.And(a[j]<m,z3.Or(*candidates)))
  earlier_swaps[i]=z3.Or(*opts)
 bad=[z3.Implies(a[i]>b[i],z3.Not(earlier_swaps[i])) for i in S]
 solver=z3.Solver();solver.add(*base,*bad)
 for rg,G in enumerate(M[:rf+1]):
  solver.push();solver.add(valid(G,b))
  if rg==rf:solver.add(earlier_same(F,b,a))
  result=solver.check();checked+=1
  if result!=z3.unsat:
   print('FAIL',rf,F,rg,G,result,solver.model() if result==z3.sat else '',flush=True)
   json.dump({'F':F,'G':G,'model':str(solver.model())},open('workspace/agent2_marker_exchange_failure.json','w'));raise SystemExit
  solver.pop()
 if rf%10==0:print('throughmarker',rf,'pairs',checked,'time',time.time()-start,flush=True)
print('ALL UNIVERSAL MULTISET EXCHANGE CHECKS UNSAT',checked,'time',time.time()-start,flush=True)
open('workspace/agent2_marker_exchange_result.json','w').write(json.dumps({'pairs':checked,'result':'unsat','seconds':time.time()-start}))
open('workspace/agent2_marker_exchange.py','w').write(open(__file__).read())
