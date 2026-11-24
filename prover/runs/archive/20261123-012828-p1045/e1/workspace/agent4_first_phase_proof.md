# First-phase weighted upper, a<=1/12

Suppose a<=1/12 and b<1/2. Then sqrt(a)+sqrt(b)<1, since
sqrt(1/12)+sqrt(1/2)<1. The established Hilbert two-row lemma implies
that red-loop vertices form a pure-red clique. Use the established greedy
minimum-cross-norm partition of the blue-loop vertices.

A maximal greedy blue-loop red-support clique has size k. The established
weighted reciprocal-degree inequality excludes k>=4. The established
partition cost inequality for k<=2 gives
b >=min{1/2,(1-sqrt(a))²}=1/2,
contradiction. Consequently k=3: there is a red-support triangle of
blue-loop rows f1,f2,f3.

Let F=f1+f2+f3 and c=1-b>1/2. Summing the three blue-row caps and the
three red-pair caps gives
  3c <=int(2F)-sum_i ||fi||²
      =int(2F-F²)+2sum_{i<j}<fi,fj>
      <=1+6a <=3/2,
because 2F-F²=1-(F-1)²<=1 pointwise. This contradicts c>1/2.

Thus b>=1/2 whenever a<=1/12. In Ramsey parameters this proves the upper
coefficient 2 for alpha<=1/6, contingent only on the team's weighted
regularity/counting reduction. The mixed-loop elimination itself is complete
in this first phase.
