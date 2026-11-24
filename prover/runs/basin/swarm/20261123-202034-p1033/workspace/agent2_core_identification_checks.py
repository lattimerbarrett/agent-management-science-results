import itertools as it,json,time
from pathlib import Path
start=time.time()
def covers_of_size(fam,U,s):
 return [frozenset(C) for C in it.combinations(sorted(U),s) if all(set(C)&F for F in fam)]
def tau(fam,U,cap):
 for s in range(cap+1):
  C=covers_of_size(fam,U,s)
  if C:return s,C
 raise AssertionError('cap too small')
def merge(classes,cores,i,v,w,t):
 U=set().union(*[F for cl in classes for F in cl]);z=max(U)+1;u=z+1;R=set(range(u+1,u+t+2));newcores=[set(X) for X in cores];newcores[i]=(newcores[i]-{v,w})|{z,u};cand=[]
 for j,cl in enumerate(classes):
  for F in cl:
   E=set(F-{v,w})|({z} if F&{v,w} else set())
   if j==i:E.add(u);cand.append((j,frozenset(E)))
   elif {v,w}<=F:
    for q in R:cand.append((j,frozenset(E|{q})))
   else:cand.append((j,frozenset(E)))
 assigned={}
 for j,F in cand:assigned.setdefault(F,j)
 out=[set() for _ in classes]
 for F,j in assigned.items():out[j].add(F)
 newU=set().union(*assigned)
 k=len(next(iter(classes[0])))
 assert all(len(F)==k for F in assigned)
 assert all(newcores[j]<=F for F,j in assigned.items())
 assert all(F&G for F,G in it.combinations(assigned,2))
 return out,newcores,newU
# Exhaustively test all core pairs in a 4-class duplicate-center instance.
n=4;m=1;T=4;k=7;E=list(it.combinations(range(n),2));ix={e:j for j,e in enumerate(E)}
cores=[set(range(6+i*T,6+(i+1)*T)) for i in range(T)];classes=[set() for _ in range(T)]
for a in range(n):
 star={j for j,e in enumerate(E) if a in e}
 for P in it.combinations(star,2):
  P=set(P);b=next(b for b in range(n) if b!=a and ix[tuple(sorted((a,b)))] not in P)
  for x in cores[b]:classes[a].add(frozenset(cores[a]|P|{x}))
fam=set().union(*classes);U=set().union(*fam);assert tau(fam,U,T)[0]==T
mincovers=covers_of_size(fam,U,T);cases=[]
for i in range(T):
 for v,w in it.combinations(sorted(cores[i]),2):
  cooccur=any({v,w}<=C for C in mincovers);out,X,U2=merge(classes,cores,i,v,w,T);newfam=set().union(*out);newtau=tau(newfam,U2,T)[0]
  assert newtau==T-int(cooccur)
  if newtau==T:assert all(out)
  cases.append({'core':i,'pair':[v,w],'minimum_cover_cooccurrence':cooccur,'new_tau':newtau})
print('four-class cases',len(cases),'preserve',sum(x['new_tau']==T for x in cases),'drop',sum(x['new_tau']<T for x in cases),flush=True)
# Padding-active example: core0=4 points, core1=2 points, all residual pairs in core0.
cores2=[set(range(4)),{4,5}];classes2=[{frozenset(range(4))},{frozenset({4,5}|set(P)) for P in it.combinations(range(4),2)}];fam2=set().union(*classes2)
assert tau(fam2,set(range(6)),2)[0]==2
out,X,U2=merge(classes2,cores2,0,0,1,2);assert tau(set().union(*out),U2,2)[0]==2
assert len(out[1])==6 # Three reservoir-padded edges, plus three distinct unpadded quotients.
# Obstruction-active example: both core0 points form a minimum2-cover.
cores3=[{0,1},{2,3}];classes3=[{frozenset({0,1,4})},{frozenset({2,3,0}),frozenset({2,3,1})}]
assert tau(set().union(*classes3),set(range(5)),2)[0]==2
out,X,U2=merge(classes3,cores3,0,0,1,2);assert tau(set().union(*out),U2,2)[0]==1
results={'four_class_cases':cases,'four_class_minimum_covers':len(mincovers),'padding_active_new_class_sizes':list(map(len,merge(classes2,cores2,0,0,1,2)[0])),'obstruction_tau':1,'seconds':time.time()-start}
Path('workspace/agent2_core_identification_checks.py').write_text(Path('scratchpad.py').read_text());Path('workspace/agent2_core_identification_checks.json').write_text(json.dumps(results,indent=2));print(results['seconds'])
