## Rigorous result: 2 belongs to N
Let Y have CAP. Every continuous bounded-above psh u on Y is constant on each component. Indeed, for a small affine disc f near any point of Y, CAP gives entire maps F_j:C→Y converging uniformly to f on its closed parameter disc. Each u∘F_j is bounded-above subharmonic, hence constant. Continuity of u passes equality to f, so u is locally constant, hence constant on components.

Suppose a boundary point q of Y is strictly pseudoconvex. Choose r with Y={r<0} near q, r(q)=0. Its tangential Levi form is positive definite. Replacing r by r+A r² for sufficiently large A makes its full Levi form positive definite at q: in tangential/normal coordinates this is a rank-one positive normal correction, and the assertion follows by the Schur complement. Shrinking the neighborhood keeps r+A r² negative precisely when r is negative. Taylor expansion at q=0 writes
r+A r²=2 Re P(z)+H(z)+O(|z|³),
where P is a holomorphic quadratic polynomial with P(0)=0 and H is a positive definite Hermitian quadratic form. Thus Re P(z)≤-c|z|² on Y∩B(0,R), for some c,R>0.

Fix 0<delta<cR² and define u=max(Re P,-delta) on Y∩B(0,R), u=-delta on the rest of Y. On a neighborhood of the artificial sphere |z|=R this agrees with the constant -delta, so it glues to a continuous bounded psh function. Its values approach 0 as z approaches q through Y, whereas it equals -delta somewhere in the same component. (For example, take a point of that component near the artificial sphere.) Hence it is not constant, contradiction.

For K in K_2, if the defining rho has a negative tangential Levi value at q, then r=-rho defines the exterior near q and has positive definite tangential Levi form, since that tangent space has complex dimension one. Thus an Oka exterior forces rho to have nonnegative tangential Levi everywhere. This proves 2∈N without any global Oka theorem.
