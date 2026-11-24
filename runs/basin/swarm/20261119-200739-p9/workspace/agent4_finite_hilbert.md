# Rigorous finite discretization for searching lower bounds

Let I_i=[i,i+1), i=0,...,N-1, and let f have constant value f_i on I_i
and vanish outside [0,N]. Let the positive matrix weight have constant
value W_i on I_i. Jensen on each output cell gives

 ||Hf||Lp(W;[0,N])^p >= sum_i |W_i^(1/p) sum_j T_ij f_j|^p,

where T_ii=0 and for d=i-j!=0,
T_ij=sgn(d)/pi[(|d|+1)log(|d|+1)-2|d|log|d|+(|d|-1)log(|d|-1)],
with 0log0=0. This is the EXACT cell average of the Hilbert kernel,
not the rough sampling1/(i-j). The code verifies20coefficients by
independent quadrature of the triangular difference distribution.
Thus a finite-dimensional norm lower is a true continuum lower.

Extend the N-cell weight periodically. Let C be the largest exact
mixed characteristic on aligned intervals of integer lengths1,...,N+2
and any initial cell (cyclic). Then global[W]Ap<=3^p C.
Indeed for an interval length>=N, cover by a union of whole periods,
with length ratio<=3; its normalized weight distribution is exactly
the period distribution. For lengths1<=|I|<N, the smallest aligned
cover has length<|I|+2<=3|I| and integer length<=N+2. Increasing both
integrations from I to its cover changes the characteristic by at
most(length ratio)^p. Finally intervals length<1 contain at mosttwo
matrix values, with arbitrary probabilities. Each probability is at
most2times the equal-probability distribution on the adjacent pair;
the mixed integral therefore costs at most2^p, and the equal pair is
included in C. This gives a global upper independent ofN.

The finite-valued periodic weight is bounded above and below by fixed
positive constants. Step f can therefore be approximated by smooth
compactly supported f in both input and output weighted norms using
ordinary unweighted Hilbert Lp boundedness. Hence these lower models
are admissible for the question's smooth-input formulation.
