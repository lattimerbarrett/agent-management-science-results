# Audited partial results (agent_1)

## 1. Continuous bounded PSH functions on an Oka domain

Let Y have CAP as in the question and let u be continuous, bounded above,
and plurisubharmonic on Y. For every affine complex disk f defined on a
neighborhood of the closed unit disk and with image in Y, CAP supplies
entire F_j converging uniformly to f there. Each u o F_j is bounded-above
subharmonic on C and hence constant. Continuity of u, uniformly on a
compact neighborhood of f(closed disk), implies u o f is constant. Every
two sufficiently close points in Y lie on such an affine disk. Thus u is
locally constant and constant on each component.

## 2. Strict pseudoconcavity of a smooth compact obstacle is impossible

Suppose at q all tangential Levi eigenvalues of the outward defining
function rho_K are negative. Let r=-rho_K define the exterior by r<0.
Its tangential Hessian is positive definite. In coordinates with
partial r(q)=(0,...,0,1/2), adding C*r^2 to r leaves the tangential block
unchanged and adds C/2 to the normal Hessian entry. Schur complement
therefore makes psi=r+C*r^2 strictly PSH near q for sufficiently large C.
Shrink the neighborhood so psi has the sign of r.

Choose a ball B(q,a) within that neighborhood and eta>0 small enough that
v=psi-eta*|z-q|^2 is still PSH there. On the exterior v<0 and on the
exterior portion of the ball sphere v<-eta*a^2. For 0<delta<eta*a^2,
patch max(v,-delta) on the exterior inside the ball to the constant
-delta outside. Near the ball sphere the two definitions agree, so the
result is a bounded continuous PSH function on the whole exterior.
It is nonconstant on the adjacent component: it approaches 0 at q but
is -delta on exterior points near the local sphere. Such points lie in
the same local exterior component (use graph coordinates).
This contradicts result 1 if the exterior is Oka.

In complex dimension 2, failure of the Levi inequality means its sole
tangential eigenvalue is negative. Hence 2 belongs to N.

## 3. Exact algebraic certificate in dimension 2

For Hessian [[a,b],[conj(b),c]], a>0, b=x+i*y, normalize partial r(q)
to (0,1/2), and choose C=2*((|b|^2+1)/a-c). The Hessian of r+C*r^2 at q
is H=[[a,b],[conj(b),(|b|^2+1)/a]], det H=1, trace T>0.
For epsilon=1/(2*T), det(H-epsilon*I)=1/2+1/(4*T^2)>0 and
its first principal minor is positive, since a*T=a^2+|b|^2+1>=1.
These identities were checked exactly by SymPy in agent1_psh_check.py.

## 4. Limits of these results

For n>=3 a single negative eigenvalue of rho_K does NOT make the exterior
strictly pseudoconvex. The PSH bump above cannot be asserted for mixed
Levi signature. Agent2's quartic Hartogs obstacle demonstrates that even
PSH-Liouville and vanishing pointwise intrinsic metrics are insufficient.

We have NOT proved general necessity or general sufficiency. No broad
compact-locality theorem for Oka complements or omitted-domain theorem
has been verified; such statements must not be inserted as facts.

## 5. Computation audit

The following scripts were executed together successfully:
- workspace/agent1_psh_check.py
- workspace/agent2_hartogs_check.py
- workspace/agent3_nonpoly_check.py
- workspace/agent4_checks.py
- workspace/agent4_basin_hull_check.py

They verify finite algebraic identities and examples, not the requested
uncountably quantified Oka implications.
