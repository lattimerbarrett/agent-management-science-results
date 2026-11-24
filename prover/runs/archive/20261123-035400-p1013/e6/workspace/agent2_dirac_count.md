# A rough Hamilton-cycle count in dense Dirac graphs

**Lemma.** For every fixed gamma>0 there is C_gamma such that every sufficiently
large n-vertex graph F with minimum degree at least (1/2+gamma)n satisfies
h(F) >= n! exp(-C_gamma n), where h counts unoriented Hamilton cycles.

Inputs are only hypergeometric concentration, the integral max-flow theorem,
van der Waerden's permanent theorem, and the directed Dirac theorem
(minimum in- and outdegree at least m/2 implies a directed Hamilton cycle).

First suppose N is divisible by m=ceil(A_gamma log n), with N=n-O(log n).
A uniformly random ordered partition of V(F) into ell=N/m equal blocks is,
with probability at least 1/2, such that every vertex has at least
(1/2+gamma/4)m neighbors in every block. Indeed each count is hypergeometric;
the mean is at least (1/2+gamma/2)m and a union bound over at most n^2
vertex/block pairs applies for sufficiently large A_gamma. Removing the
O(log n) exceptional vertices initially only changes gamma to gamma/2.

A bipartite graph with m vertices on each side and minimum degree
Delta>(1/2+eta)m has an r-factor for r=floor(eta*m/2), for large m.
Here is an explicit max-flow cut verification. More generally suppose
r<=Delta/2 and r<=2Delta-m. For X,Y on the two sides, put x=|X|, y=|Y|,
s=x+y-m. Only s>0 needs checking. Assume x<=y.
* If x>=Delta, then y>=Delta, so e(X,Y)>=x(2Delta-m)>=rs.
* If r<=x<=Delta, then e(X,Y)>=x(Delta-m+y)=x(Delta-x+s)>=rs.
* If x<r, then y>m-r, so e(X,Y)>=x(Delta-r)>=xr>=rs.
These are exactly the r-factor cut inequalities. The r-factor has at least
r^m m!/m^m >= (r/e)^m perfect matchings by van der Waerden.
Thus each consecutive pair of blocks admits at least (c_gamma*m)^m matchings.

Choose such a matching freely between blocks i and i+1 for i=1,...,ell-1.
Their union consists of m vertex-disjoint paths, each with one vertex in every
block. Make a digraph on these m paths: put an arc i->j when the last vertex
of path i is adjacent to the first vertex of path j. After deleting possible
loops, its minimum in/outdegree is still greater than m/2. The directed Dirac
theorem supplies a directed Hamilton cycle, and hence a closing matching
which makes the union ONE Hamilton cycle of F.

There are at least N!/(2(m!)^ell) good ordered partitions. Each resulting
Hamilton cycle is compatible with at most 2N ordered partitions, since a
starting vertex and direction determine the repeating block labels. Its
first ell-1 matchings are then determined. Consequently
 h(F) >= N!/(4N(m!)^ell) * (c_gamma*m)^(N-m)
       >= N! * exp(-O_gamma(N)),
using m!<=m^m and m log m=o(N).

For arbitrary n, set aside a fixed set R of fewer than m vertices so that
N=n-|R| is divisible by m. Apply the preceding argument to F-R. Insert the
vertices of R one at a time, in a fixed order. At each stage every cycle has
at least 2d_C(v)-|C| >= gamma*n admissible insertion edges. Removing the last
inserted vertex is a unique inverse, so the number of final cycles is at
least h(F-R)*(gamma*n)^|R| >= n!*exp(-O_gamma(n)).

**Tail consequence.** The number of cycles, or paths with specified endpoints,
of length at most n-n/sqrt(log n) is at most
 n! * exp(-Omega(n sqrt(log n))).
This is negligible compared with the preceding Hamilton lower bound, even
after multiplication by any polynomial in n. Thus dense-Dirac all-cycle
switching arguments may discard such short cycles uniformly.
