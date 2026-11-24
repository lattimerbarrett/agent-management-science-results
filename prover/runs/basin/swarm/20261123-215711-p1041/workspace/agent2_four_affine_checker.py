from z3 import *
import itertools,time,json
s=Solver();s.set(timeout=300000)
d={0:IntVal(15)}
for I in range(1,32):
 d[I]=Int('d%d'%I);s.add(d[I]>=0,d[I]<=15)
for i in range(4):s.add(d[1<<i]==8,d[(1<<i)|16]==7)
s.add(d[16]==14)
for A in range(32):
 for B in range(32):
  if A&B==A:s.add(d[A]>=d[B])
  s.add(d[A]+d[B]<=d[A|B]+d[A&B])
for J in range(1,16):s.add(d[J]-d[J|16]>=0,d[J]-d[J|16]<=1)
for labs in itertools.product(range(5),repeat=5):
 A=B=C=D=0
 for i,z in enumerate(labs):
  if z==1:A|=1<<i
  elif z==2:B|=1<<i
  elif z==3:C|=1<<i
  elif z==4:D|=1<<i
 if not A or not B or not C or not D:continue
 def r(J):return 15-d[J]
 s.add(r(A|B)+r(A|C)+r(A|D)+r(B|C)+r(B|D)>=r(A)+r(B)+r(C|D)+r(A|B|C)+r(A|B|D))
def term(J):return If(d[J]>d[J|16],Sum([If(d[J]==i,2**(i-1),0) for i in range(1,9)]),0)
w=512-2*Sum([term(j) for j in range(1,16) if j.bit_count()==2])+4*Sum([term(j) for j in range(1,16) if j.bit_count()==3])-8*term(15)
# To enumerate further profiles at a target, fix w then exclude each already ruled-out profile.
# IMPORTANT: satisfiability is only a NECESSARY rank-profile condition, not subspace realization.

Jlist=[j for j in range(1,16) if j.bit_count()>=2]
# Each pair dict indexes AB=3, AC=5, BC=6, AD=9, BD=10, CD=12.
# Triple indices ABC=7, ABD=11, ACD=13, BCD=14.
# The geometric impossibility lemmas are in agent2_four_affine_lemmas.md.
patterns=[
 ({3:8,5:8,6:64,9:1,10:8,12:8},{11:1}),
 ({3:16,5:64,6:0,9:4,10:1,12:4},{}),
 ({3:8,5:1,6:8,9:8,10:64,12:8},{11:4}),
 ({3:0,5:8,6:1,9:64,10:8,12:8},{}),
 ({3:1,5:4,6:8,9:4,10:8,12:64},{}),
 ({3:4,5:64,6:4,9:16,10:1,12:16},{13:8}),
]
blocked=0
for pairs,triples in patterns:
 vals={j:0 for j in Jlist};vals.update(pairs);vals.update(triples)
 seen=set()
 for p in itertools.permutations(range(4)):
  def perm(j):return sum(1<<p[i] for i in range(4) if j>>i&1)
  vv=tuple(vals[perm(j)] for j in Jlist)
  if vv in seen:continue
  seen.add(vv);s.add(Or(*[term(j)!=v for j,v in zip(Jlist,vv)]));blocked+=1
# Hyperplane-pair lemma.
for i,j in itertools.combinations(range(4),2):
 for k in range(4):
  if k in (i,j):continue
  ij=(1<<i)|(1<<j);ik=(1<<i)|(1<<k);jk=(1<<j)|(1<<k);ijk=ij|ik
  s.add(Implies(And(term(ij)==64,term(ijk)==0,term(ik)>0,term(jk)>0),term(ik)==term(jk)))
# General projection lemma.
for a,b,c,dd in itertools.permutations(range(4)):
 A=1<<a;B=1<<b;C=1<<c;DD=1<<dd
 for rr in range(7):
  cond=And(term(A|B)==0,term(A|DD)==1,term(B|DD)==64,term(B|C)==2**rr,term(C|DD)==2**rr,term(B|C|DD)==0,term(A|C|DD)==0)
  s.add(Implies(cond,term(A|C)<=(2**(5-rr) if rr<=5 else 0)))
print('blocked affine size patterns',blocked,flush=True)
results={}
for target in [322,326,330,334]:
 s.push();s.add(w==target);t=time.time();ans=s.check();print(target,ans,time.time()-t,flush=True)
 assert ans==unsat,(target,ans)
 results[target]=str(ans);s.pop()
json.dump(results,open('workspace/agent2_four_affine_results.json','w'))

# Also cover at most three affine7flats (four-flat XOR does not subsume three).
# For three, w=384-2*(p+q+r)+4*t, all nonempty intersections powers of two.
P=[0]+[1<<i for i in range(8)]
profiles={}
for target in [322,326,330,334]:
 profiles[target]=[(v,t) for v in itertools.combinations_with_replacement(P,3) for t in P
  if t<=min(v) and 384-2*sum(v)+4*t==target]
assert profiles=={322:[((1,16,16),1)],326:[],330:[],334:[((1,8,16),0)]}
# 322: two4flat intersections inside a7flat through their triple point must
# intersect in dimension >=4+4-7=1, hence cannot have triple size1.
assert 4+4-7>0
# 334: the 4flat and3flat intersections inside a7flat have complementary
# directions, since the remaining pair meets at a point; hence must meet,
# contradicting triple size0. At most two flats have weight at most256.
assert 4+3==7 and 2*128<322
print('At-most-three-flat intersection profiles excluded:',profiles)
