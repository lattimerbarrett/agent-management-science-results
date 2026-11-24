# A Fatou--Bieberbach domain with no ambient-closed analytic curves

Let H(z,w)=(w/10,z/10+10w^2). Its derivative at zero has eigenvalues +/-1/10, so zero is attracting, and its basin is biholomorphic to C^2 by the standard attracting-basin theorem.

If |w|>max(|z|,2), then |w'|>=10|w|^2-|z|/10>2|w| and |z'|=|w|/10. Thus this cone is forward invariant and escaping. The forward nonescaping set K+ is contained in {|w|<=max(|z|,2)}.

Suppose A is an ambient-closed irreducible analytic curve contained in K+. Projection to z is proper, since over bounded z the inequality bounds w, and it has finite fibers, since a vertical curve component would be compact. The monic Weierstrass polynomial of this finite covering has coefficients entire in z, and its coefficient of degree d-j in w has growth O((1+|z|)^j). Therefore all coefficients are polynomials; A is algebraic.

Choose a point at infinity of its compact normalization. Let p_j,q_j denote pole orders of the two coordinates of H^j on this branch, with order zero for functions bounded at this point. The cone bound gives 0<=q_j<=p_j. Properness of polynomial automorphism H implies at least one coordinate has a pole after every iterate, hence p_j>0. If q_j=0, then z_{j+1}=w_j/10 is bounded but w_{j+1}=z_j/10+10w_j^2 has pole order p_j, contradicting the cone bound. Therefore q_j>0.

Now p_{j+1}=q_j. If p_j != 2q_j, the pole order of w_{j+1} is max(p_j,2q_j)>q_j=p_{j+1}, another contradiction. Thus p_j=2q_j for every j, giving p_{j+1}=p_j/2 indefinitely. Positive integers cannot satisfy this recurrence. No A exists.

Consequently, if F:C^2 -> Omega is a biholomorphism, the globally strictly plurisubharmonic function ||F||^2 on C^2 is unbounded but admits no nonconstant holomorphic curve proper with respect to it. Such a curve would give an ambient-proper map into C^2 and hence an ambient-closed analytic curve in Omega by Remmert's theorem.

This blocks a speculative proof route; it does NOT settle the user's dimension sets.
