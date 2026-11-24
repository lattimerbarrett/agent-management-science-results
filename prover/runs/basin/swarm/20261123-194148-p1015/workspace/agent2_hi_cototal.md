# Infinite literally cototal hyperimmune set

This answers the subsidiary question in Slack #246 affirmatively. It does not settle the skip problem.

Let H_s be a monotone computable approximation to the ordinary halting set H. Choose a strictly increasing computable b(n), with b(0)=0, so that the settling function
    g(n)=least s such that H_s restricted to b(n) equals H restricted to b(n)
eventually dominates every computable function. Such b exists: for every e,k<=n, include below b(n) an index of a program simulating phi_e(k) and then waiting more than its output many steps. For any total computable f=phi_e and all sufficiently large n, this program on input n halts later than f(n), hence g(n)>f(n). Use the standard step-by-step halting approximation. Make b monotone by taking finite maxima.

View binary strings of lengths b(n) as nodes at level n. Begin with the root. At stage s, for each level n<=s in increasing order, expand the node H_s restricted to b(n), if it has been created and has not previously been expanded. Expansion of a node at level n creates all 2^(b(n+1)-b(n)) immediate next-block children. Assign each child a distinct fresh natural-number token, larger than all tokens assigned previously and at least s. The construction is computable and creates only finitely many objects at each stage.

When expanding a node tau, enumerate the finite hyperedge E_tau consisting of:
  (i) all tokens of the immediate children of tau;
  (ii) for every proper ancestor rho of tau, all tokens of rho's children except the child lying on tau.
All these child lists are known because tau could be created only after each ancestor was expanded. Thus the hypergraph is computably enumerable.

The created tree has exactly one infinite branch, namely the block-prefix sequence of H. Every true prefix is eventually expanded. A false prefix agrees with H_s only at finitely many stages, so its subtree is expanded only to bounded depth; finite branching then makes that subtree finite. Let M be the tokens of the non-root nodes on the true branch.

M hits every hyperedge. If tau is on the true branch, exactly one child token in E_tau belongs to M, and none of the ancestor-sibling tokens belongs to M. If tau is off the true branch, at the first divergence from the true branch, the true chosen child is an ancestor-sibling token in E_tau. Moreover, the edge belonging to the parent of any true-branch token x has intersection with M exactly {x}. Hence M is an infinite minimal transversal.

Define an enumeration operator Gamma by putting (x,E\{x}) among its axioms for every enumerated edge E and x in E. If x belongs to M, its private edge witnesses x in Gamma(complement M). If x does not belong to M, no edge E containing x can have E\{x} disjoint from M, since M hits E. Consequently
    M = Gamma(complement M),
so M is literally cototal.

Finally, write its tokens increasingly as m_1<m_2<...; token assignments increase along the true branch, so m_j is the token at level j. Its parent, the true level-(j-1) prefix, cannot be expanded before it first appears in H_s, namely before stage g(j-1). Therefore m_j >= g(j-1). The function j |-> g(j-1) still eventually dominates every computable function (apply domination to the computable shifted function). Thus the principal function of M dominates every computable function. In particular it is not computably dominated, so M is hyperimmune.

In fact M and its complement both have total enumeration degree H. To decide whether a number x is a token, simulate through stage x: all later tokens have labels greater than x. If it is a token for a node tau, membership in M is exactly tau being a prefix of H, decidable in H. Thus M <=_e H. Conversely, M contains true-prefix tokens at arbitrarily large levels, so positive M uniformly enumerates both H and its complement, giving H <=_e M. Since M <=_e complement(M) by cototality, and complement(M) is H-computable, both sets have enumeration degree H.

Supplementary finite verification: workspace/agent2_hi_cototal_check.py checks all 3905 monotone finite halting histories on up to five bits (each bit absent or enumerated at one of four stages), checking 21510 hyperedges and 43020 tokens. It verifies transversal and private-edge identities, exact Gamma(complement M)=M, and the creation-time lower bound. The infinite domination argument is proved above, not inferred from that experiment.
