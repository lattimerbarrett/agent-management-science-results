from pathlib import Path
import mpmath as mp,json
mp.mp.dps=100
out=[]
for a in (1000,2000,10000):
 r=a**5;m=a**9;N=m+r-1
 rr=mp.mpf(r);mm=mp.mpf(m);NN=mp.mpf(N)
 L=mp.log(mp.e*NN/rr);alpha=rr*rr/NN
 d=int(mp.ceil(4*NN/rr*L))
 # Union bound 1: S pairwise intersect. Fixed disjointness p<=exp(-r^2/N).
 log_bad_pair=mp.log(mm*(mm-1)/2)-alpha
 # Union bound 2: no original r-set P misses >=d sampled S.
 # Number P<=(eN/r)^r; Binomial tail <= C(m,d)*p^d<=(em/d)^d*p^d.
 log_bad_near=rr*L+d*mp.log(mp.e*mm/d)-d*alpha
 # Union bound 3: ensure all sampled S distinct, so all weights are exactly 1.
 # C(N,r)>=(N/r)^r.
 log_bad_dup=mp.log(mm*(mm-1)/2)-rr*mp.log(NN/rr)
 assert max(log_bad_pair,log_bad_near,log_bad_dup)<-100
 assert mp.exp(log_bad_pair)+mp.exp(log_bad_near)+mp.exp(log_bad_dup)<1
 proposed=rr*mp.sqrt(d)+rr*rr*d/mm
 ratio=mm/proposed
 assert ratio>1000
 out.append(dict(a=a,r=str(r),W=str(m),N=str(N),d=str(d),log_bad_pair=str(log_bad_pair),log_bad_near=str(log_bad_near),log_bad_duplicate=str(log_bad_dup),tau_to_proposed_ratio=str(ratio)))
print(json.dumps(out,indent=2))
Path('workspace/agent3_nearblocker_counter_checks.json').write_text(json.dumps(out,indent=2))
Path('workspace/agent3_nearblocker_counter_checks.py').write_text(Path('scratchpad.py').read_text())
Path('workspace/agent3_nearblocker_counter_proof.txt').write_text('''COUNTEREXAMPLE TO THE PROPOSED INTERSECTING ALMOST-BLOCKER LEMMA (#515)
Let a tend to infinity through integers, r=a^5, W=m=a^9, N=m+r-1, and alpha=r^2/N~a. Independently sample m uniform r-subsets S_j of [N], each of weight one. Let d=ceil(4(N/r)log(eN/r))=O(a^4 log a).
(1) Each pair is disjoint with probability at most exp(-alpha), since C(N-r,r)/C(N,r)<=exp(-r^2/N). Union bound gives failure <=m^2 exp(-alpha)/2=o(1).
(2) For any fixed r-set P, the number of sampled S_j disjoint from P is binomial(m,p), p<=exp(-alpha). Probability of at least d misses is <=(em/d)^d exp(-alpha d). Union bound over C(N,r)<=(eN/r)^r gives log failure <=r log(eN/r)+d log(em/d)-alpha d, which tends to minus infinity (main terms r*O(log a)-4r*O(log a), since log m=o(alpha)). Thus simultaneously EVERY r-set P misses at most d members of S.
(3) Duplicate probability <=m^2/(2 C(N,r))<=m^2(r/N)^r/2=o(1). Hence we can require all S_j distinct and weights exactly one.
The Python checks evaluate these rigorous union bounds at a=1000,2000,10000 with 100-digit arithmetic, each total failure probability<1.
Therefore there exists an INTERSECTING weighted rank-r family S of total W=m, weights exactly one, such that EVERY r-set P misses S-mass <=d. Consequently the family of all rank-r almost-blockers contains EVERY r-set of [N], and its covering number is N-r+1=m. But r sqrt(d)+r^2 d/W = O(a^7 sqrt(log a)+a^5 log a)=o(a^9)=o(m). Also W/d tends to infinity. This refutes every universal-constant version of the bound proposed in #515, even with intersecting S and weights<=1.
This is agent2's earlier first-order-gradient counterexample (#312), with the added observation that sampled S are themselves intersecting with high probability.
''')
