from itertools import combinations
from fractions import Fraction
from pathlib import Path
import json
n=8;m=2;q=2*m-1;t=n*m;r=n-2*m
edges=list(combinations(range(n),2));ind={e:j for j,e in enumerate(edges)}
stars=[set(ind[e] for e in edges if a in e) for a in range(n)]
patterns=[[set(c) for c in combinations(stars[a],r)] for a in range(n)]
checks=0
for a,b in combinations(range(n),2):
 e=ind[a,b]
 for P in patterns[a]:
  for Q in patterns[b]:
   u=e not in P;v=e not in Q
   assert (not(P&Q))==(u or v)
   assert (not(P&stars[b]))==u
   assert (not(stars[a]&Q))==v
   checks+=1
assert all(P&Q for cl in patterns for P in cl for Q in cl)
O=[{(a+j)%n for j in range(1,q+1)} for a in range(n)]
assert all(not(a in O[b] and b in O[a]) for a,b in combinations(range(n),2))
selected=[stars[a]-{ind[tuple(sorted((a,b)))] for b in O[a]} for a in range(n) for z in range(m)]
seed=[stars[a] for a in range(n) for z in range(m)]
Qold=sum(not(P&Q) for j,P in enumerate(selected) for Q in selected[:j]);assert Qold==t*m*q
# Explicit lifted realization.
N0=len(edges)
old=[{p for p in P}|{N0+i*N0+p for p in P} for i,P in enumerate(selected)]
dummy=[{N0+j*N0+p for p in A for j in range(t) if j!=i} for i,A in enumerate(seed)]
assert all(not(old[i]&dummy[i]) for i in range(t))
for i,j in combinations(range(t),2):
 assert bool(old[i]&old[j])==bool(selected[i]&selected[j])
 assert bool(old[i]&dummy[j])==bool(selected[i]&seed[j])
 assert bool(dummy[i]&old[j])==bool(seed[i]&selected[j])
 assert bool(dummy[i]&dummy[j])==bool(seed[i]&seed[j])
G=[]
for i in range(t):
 row=[]
 for j in range(t):
  if i==j:v=2
  else:v=int(bool(old[i]&old[j]))+int(bool(dummy[i]&dummy[j]))-int(bool(old[i]&dummy[j]))-int(bool(dummy[i]&old[j]))
  assert v==(2 if i==j else 0);row.append(v)
 G.append(row)
cert=[]
for alpha in (Fraction(m*q)-Fraction(1,2),Fraction(m*q),Fraction(m*q)+Fraction(1,2)):
 w=(1+m*q-alpha)/2
 cross=sum(w*w*int(not(old[i]&old[j]))+w*(1-w)*int(not(old[i]&dummy[j]))+(1-w)*w*int(not(dummy[i]&old[j]))+(1-w)**2*int(not(dummy[i]&dummy[j])) for i,j in combinations(range(t),2))
 within=t*w*(1-w);bonus=alpha*t*(1-w);value=cross+within+bonus
 upper=alpha*t+t*((m*q-alpha+1)*w-w*w)
 assert value==upper
 cert.append(dict(alpha=str(alpha),old_mass_per_color=str(w),objective=str(value),global_upper_bound=str(upper)))
res=dict(n=n,m=m,t=t,actual_rank=r,target_size=m*q,patterns_per_color=len(patterns[0]),cross_pattern_pairs_checked=checks,original_actual_Qmax=Qold,lifted_point_ground=(t+1)*N0,lifted_old_ranks=sorted(set(map(len,old))),dummy_ranks=sorted(set(map(len,dummy))),Gram='2I_%d'%t,global_mixed_optimality_certificates=cert)
print(json.dumps(res,indent=2))
Path('workspace/agent3_lifted_star_qp_checks.json').write_text(json.dumps(res,indent=2))
Path('workspace/agent3_lifted_star_qp_checks.py').write_text(Path('scratchpad.py').read_text())
Path('workspace/agent3_lifted_star_qp_proof.txt').write_text('''EXACT STAR QP OPTIMUM AND LIMITATION OF LIFTED-SEED ROOT METHOD
Parameters n>4m-1, q=2m-1, T=nm, actual rank r=n-2m. Each of m classes at center a has all r-subsets of the n-1 actual K_n star points; its seed is the whole star. Every old pattern omits exactly q neighbor centers. Let w_i be total old mass of color i, and p_i(b) its conditional probability of omitting bridge to center b.
For colors i,j at different centers a,b, the old-old petals are disjoint iff at least one side omits bridge ab. Old_i/seed_j are disjoint iff i omits b. Seeds always intersect. Thus cross-color Q contribution is w_i p_i(b)+w_j p_j(a)-w_i w_j p_i(b)p_j(a). At the same center all petals intersect, so contribution zero. Summing the linear terms over the m copies at every neighbor gives mq sum_i w_i. Therefore original actual Q is at most Tmq, attained by pure old choices with no mutual omissions.
Such omissions exist: choose an oriented q-outregular cyclic graph on centers (steps 1,...,q), possible since n>=2q+1. Let every class at center a omit exactly its q outneighbors. No two centers omit one another. This attains original Q=Tmq exactly. The Hall condition holds for these ACTUAL FAMILIES: a point set C of actual K_n edges covers every r-subset of star(a) iff deg_C(a)>=q+1=2m; the number of activated colors is m times activated centers, at most |C| by the handshake lemma. Any color subunion has no larger activation count. Thus this really tests the full-Hall colored QP scale, not a deficient example.
LIFT: old P_i contains common p and private(p,i) for every p in P_i; dummy seed i contains private(p,j) for p in seed A_i and j!=i. Old rank doubles; dummy rank is (T-1)(n-1). For T>=3 all cross-color intersections agree with original old/seed intersections, while own old/dummy are disjoint. So within-color Q is w_i(1-w_i), all old-old pairs within a color still intersect.
With bonus alpha times dummy mass, f=alpha*T+sum_i[(mq-alpha+1)w_i-w_i^2]-sum_{i<j,different centers}w_iw_j p_i(b)p_j(a). The last term is nonpositive. Choosing the no-mutual-omission graph above sets it to zero. Thus GLOBAL optimum is attained with ALL colors mixed equally at w_i=(mq-alpha+1)/2 whenever mq-1<alpha<mq+1. The mixed root Gram has diagonal2 and off-diagonal exactly mutual-omission indicators, hence is EXACTLY 2I_T at this GLOBAL optimum.
Conclusion: the lifted-seed trick repairs the vacuous norm-zero directions of unlifted linear seed bonuses, but even full mixing at a global optimum can give completely orthogonal roots. Because dummy ranks are huge, ADE root classification alone still does not control T in terms of old rank/target budget. More seed-geometry/cover-number information is necessary.
The Python checks all 34300 cross-center pattern pairs for n8,m2 (plus all within-center intersections), explicitly realizes all lifted sets, checks the Gram2I_16, and gives exact Fraction-valued global upper-bound attainment for three interior alpha values.
''')
