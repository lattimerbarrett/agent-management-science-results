# Exact graphon reduction and loop classification

For a symmetric measurable W:[0,1]²->[0,1], set f_x(z)=W(x,z),
R(x,y)=<f_x,f_y>, Q(x,y)=<1-f_x,1-f_y>. A sequence of red-blue
countercolorings on N_j->infinity, whose normalized red/blue book bounds
converge to a,b, has a cut-limit graphon W. It satisfies
 W(x,y)>0 => R(x,y)<=a,
 W(x,y)<1 => Q(x,y)<=b
for almost every pair (x,y).

Indeed for every fixed integer k>=1, the finite book bound implies
 t(B_k,W_j)=int W_j R_j^k <= a_j^k int W_j.
Homomorphism densities of a fixed finite simple graph are continuous in
cut distance (telescope edges and use the defining cut norm), so
 int W R^k <=a^k int W for all k. A positive measure set where W>0 and
R>a would contain a subset with W>=eta and R>=a+eta, contradicting this
inequality as k->infinity. Apply the same argument to the blue complement.
For finite graphons the complement differs from the blue adjacency graphon
only on diagonal vertex atoms, of total measure1/N_j, irrelevant in the limit.

Every such graphon has the EXACT measurable loop partition:
 almost every x satisfies ||f_x||²<=a OR ||1-f_x||²<=b.
To prove this, suppose the set violating both inequalities has positive
measure. On a positive measure subset the two excesses exceed some eta>0.
The map x->f_x into separable L² is measurable. Cover its image by countably
many sufficiently small L² balls. One ball contains a positive measure set
A of violating rows. If the radius is small enough in terms of eta, every
pair x,y in A has R(x,y)>a and Q(x,y)>b, since all row norms are at most1
and inner products vary continuously in the L² norm. The pair constraints
would require simultaneously W(x,y)=0 and W(x,y)=1 almost everywhere
on A², impossible.

If sqrt(a)+sqrt(b)<1 the two row classes are disjoint by the triangle
inequality ||1||<=||f||+||1-f||. Thus define R as the small-red-norm rows
and B as the small-blue-norm rows. All previously proved Hilbert and clique
lemmas apply to these measurable classes, using almost-everywhere-good
representative vertices, which Fubini allows at each of finitely many steps.

For the greedy partition choose each blue vertex within delta of the
essential infimum of q_R(x)=int_R W(x,z)² among the current candidate set;
remove its red nonneighbors. If no blue-loop red K4 exists, this terminates
in at most3 steps, otherwise a positive-measure candidate set supplies a
fourth good representative and contradicts the K4 inequality. The resulting
classes V_i have weights theta_i and satisfy W(v_i,x)=0 on V_i and
 sum theta_i q_R(v_i)<=int_B q_R+delta.
Take delta->0 and pass to a subsequence of the finitely many row moments
and theta_i. All moment/row/pair inequalities are closed, giving the exact
finite-moment partition model and cost budget used by the team. Empty
classes are harmless and correspond to k<=2 boundary cases.

## Cut compactness, if not taken as a standard theorem

The weak regularity energy-increment argument gives compactness directly.
For epsilon>0 and any finite partition P, repeatedly choose a rectangle
S×T on which W-E[W|P×P] has integral magnitude>epsilon, and refine every
part by S and T. The L² energy of the conditional expectation increases
by at least epsilon² each time (orthogonal projection and Cauchy), while
remaining at most1. Thus at most epsilon^-2 refinements, each increasing
part count by at most4, give cut-norm error<=epsilon.

For a sequence W_j apply this with epsilon=2^-k, successively refining the
previous partition. At each k the number of parts is bounded independently
of j. Relabel the nested partition cells in a fixed tree order, and take a
diagonal subsequence on which every cell weight and block density converges.
The limiting step graphons U_k are consistent conditional expectations on
nested limiting partitions. Their bounded L² energies imply, by the
orthogonality of successive increments, that U_k converge in L² to a
measurable W in[0,1]. For fixed k the jth step approximation tends in L¹
to U_k; the original W_j is within2^-k in cut norm of that approximation.
The triangle inequality, first j->infinity and then k->infinity, gives
cut-distance convergence to W. This proves the compactness used above.
