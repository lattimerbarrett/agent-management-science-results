# Upper bound, independently complete
Put n=2^(s-1), j=2n-2, d=3n-2. We prove every j absolutely
continuous probabilities on R^d admit a common partition into four quarters.

Represent an oriented affine hyperplane by u=(a,b) in S^d in
R^d x R, with sign function eps_u(z)=sign(a.z+b). For a nonzero a,
the zero set has measure zero for every given measure. For a=0 the
sign is constant. Each integral below is continuous in u: for any
sequence converging to u, signs converge away from the affine hyperplane
(or everywhere when a=0), and dominated convergence applies.

For each probability mu_i define the three coordinates
  integral eps_u dmu_i,
  integral eps_v dmu_i,
  integral eps_u eps_v dmu_i.
Together they define a continuous map F:S^d x S^d -> R^(3j).
Changing u to -u changes signs of coordinates one and three; changing
v changes signs of coordinates two and three. Thus F defines a section
of the vector bundle
 E = (L_1 directsum L_2 directsum (L_1 tensor L_2))^(directsum j)
over RP^d x RP^d, where L_1,L_2 are pulled-back tautological lines.

Use mod-two cohomology. The projective-space ring and Whitney product
formula give
 H^*(RP^d x RP^d;F2)=F2[x,y]/(x^(d+1),y^(d+1)),
 w_(3j)(E)=[xy(x+y)]^j.
A nowhere-zero section would split off a trivial real line (using a
bundle metric), forcing its top Stiefel-Whitney class to vanish.

Here j=2n-2 and n is a power of two. In characteristic two,
 (x+y)^j = product_(r=1)^(s-1) (x^(2^r)+y^(2^r)).
Consequently its coefficient at x^k y^(j-k) is one precisely for
even k between 0 and j. In the quotient, multiplying by x^j y^j,
only k in [n-2,n] can survive, and their parity leaves exactly
  w_(3j)(E) = x^(d-2)y^d + x^d y^(d-2) != 0.
The two monomials are distinct basis elements since d>=10.
Thus every section F has a zero.

At a zero, for signs alpha,beta in {+1,-1}, Fourier inversion gives
 mu_i(eps_u=alpha,eps_v=beta)
 = (1+alpha int eps_u+beta int eps_v+alpha beta int eps_u eps_v)/4
 = 1/4.
In particular neither a normal is zero. The hyperplanes cannot coincide
or be parallel, because then their complement would have at most three
regions, forcing at least one of the four sign regions to be empty.
Nonparallel affine hyperplanes have exactly four connected components,
namely the four nonempty open intersections of their halfspaces. These
components each have measure 1/4, as required.

This establishes D_s <= 3*2^(s-1)-2, NOT equality. The remaining requested
lower bound is the critical dimension d=3*2^(s-1)-3.
