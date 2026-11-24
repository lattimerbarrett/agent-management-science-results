from pathlib import Path
import math,json
rows=[]
for j in [10,11,12,16,20,30,50,100]:
 q=2**j;r=q**5;N=q**9;W=N;d=100*j*q**4
 assert d<W and r<N
 # Union bounds for disjoint pair, duplicate pair, and any bad rank-r nearblocker.
 log_pair=18*j*math.log(2)-q
 log_dup=(18-4*r)*j*math.log(2)
 assert 1+9*j*math.log(2)<=q/2
 log_bad_bound=r*(1+4*j*math.log(2))-d*q/2
 assert log_pair<-math.log(4) and log_dup<-math.log(4) and log_bad_bound<-math.log(4)
 nearcover_target=r*math.sqrt(d)+(r*r*d)/W
 tau=N-r+1
 ratio=tau/nearcover_target
 rows.append(dict(j=j,q=q,log_pair_failure=log_pair,log_duplicate_failure=log_dup,log_any_bad_P_failure_upper=log_bad_bound,tau_to_proposed_rhs=ratio))
print(json.dumps(rows,indent=2))
Path('workspace/agent1_intersecting_nearblocker_counter.json').write_text(json.dumps(rows,indent=2))
Path('workspace/agent1_intersecting_nearblocker_counter.py').write_text(Path('scratchpad.py').read_text())
Path('workspace/agent1_intersecting_nearblocker_counter_proof.txt').write_text('''COUNTEREXAMPLE TO PROPOSED ALMOST-BLOCKER THEOREM (#515)
For integer j>=10 put q=2^j, r=q^5, N=q^9, W=N, d=100*j*q^4.
Take W independent uniform r-subsets S_1,...,S_W of [N].
(1) A pair is disjoint with probability at most exp(-r^2/N)=exp(-q).
The union-bound failure probability is <=W^2 exp(-q)=exp(18*j*log2-q)<1/4.
The exponent is negative enough at j=10 and decreases since its successive
increment is 18*log2-2^j<0.
(2) A pair is equal with probability 1/binom(N,r), and
binom(N,r)>=(N/r)^r=q^(4r). Duplicate failure <=q^(18-4r)<1/4.
(3) For ANY fixed r-set P, the number Z_P of sampled S_i disjoint from P
is Binomial(W,p), p<=exp(-q). Thus Pr[Z_P>=d]<=(e*W*p/d)^d.
The number of P is <=(e*N/r)^r, so the union failure is at most exp(E),
E=r*(1+4*j*log2)+d*(1+9*j*log2-log(d)-q).
For j>=10, 1+9*j*log2<=q/2 (check base; the RHS doubles and its
increment dominates 9*log2). Therefore E<=q^5*(1+4*j*log2-50*j)
<=-q^5, using log2<1 and j>=1. Hence this failure is also <1/4.
Consequently there exists a DISTINCT pairwise-intersecting rank-r family
S of W edges, each weighted 1, such that EVERY r-subset P of [N] misses
at most d members of S. Therefore its rank-r nearblocker hypergraph
contains ALL r-subsets and has transversal number AT LEAST N-r+1.
Yet r*sqrt(d)+r^2*d/W=10*sqrt(j)*q^7+100*j*q^5, whereas
N-r+1>=q^9/2. The ratio is at least
q^2/(20*sqrt(j)+200*j/q^2), tending to infinity.
This refutes ANY universal constant in the proposed bound
O(r*sqrt(d)+r^2*d/W), even with S intersecting, weights<=1 and W>>d.
It does NOT refute a QP-optimal-support version, since S is arbitrary.
''')
