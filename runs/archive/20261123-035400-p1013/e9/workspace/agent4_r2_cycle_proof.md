# Exact cycle comparison for the r=2 endpoint construction

Put P(x)=1+9x+7x^2+x^3 and Q(x)=1+4x+x^2.
For m>=1 set B=3m, A_m=(m P3) join I_B, and
B_m=((m-1)P3 union 2K2) join I_(B-1).
Then c(B_m)>c(A_m) for every sufficiently large m.

## Path-forest identity
For a graph F let p_F(x) be the sum over all choices of a vertex set S
and an acyclic max-degree-at-most-two spanning subgraph L on S, weighted
by 2^(number of non-singleton components) x^(number of components).
The empty choice contributes 1. Then p_(F union F')=p_F p_F',
p_P3=P and p_K2=Q.
For any F on a vertices and independent set I_b,

 c(F join I_b)=c(F)+(1/2) sum_(k>=1) k!(k-1)! [x^k]p_F(x) binom(b,k)-ab/2.

Proof: contract every maximal nontrivial path lying in F in an original
cycle using both sides. Together with each selected isolated vertex in F,
these paths form k blocks alternating with k selected vertices of I_b.
For k>=2 the number of cycles on the distinguishable blocks is
k!(k-1)!/2, and each nontrivial path can be oriented in two ways.
For k=1 the same formal expression gives the correct number when the
F block is a nontrivial path, but gives 1/2 for every pair of singleton
vertices; subtracting ab/2 removes exactly these spurious length-two
objects. Cycles wholly in F contribute c(F).

The code workspace/agent4_cycle_tools.py checks this identity against
independent direct cycle enumeration on all 53 unlabeled graphs F on at
most five vertices, for b=0,1,2,3 (212 cases), and verifies P,Q.

## Limits
Set R(x)=x^3 P(1/x)=1+7x+9x^2+x^3 and lambda=7/3.
Normalize counts by Z_B=B!(B-1)!/2. Applying the identity, reversing the
coefficients, and putting j=B-k gives

 c(A_m)/Z_B = sum_(j=0)^(B-1)
 [x^j]R(x)^m (B-j-1)!/((B-1)!j!) + o(1).

The subtracted a*b/2 divided by Z_B tends to zero. For each fixed j,
B^(-j)[x^j]R(x)^m -> lambda^j/j!.
Since R <= (1+lambda*x)^3 coefficientwise, the j-th summand is bounded by

 (B/(B-j)) lambda^j/(j!)^2 <= (j+1)lambda^j/(j!)^2.

This bound is summable, so dominated convergence gives the limit
F0(lambda)=sum_(j>=0)lambda^j/(j!)^2.

For B_m its internal path polynomial is P^(m-1)Q^2, of degree B+1.
Its reversed polynomial is S_m=R^(m-1)Q^2, since Q is palindromic.
Put j=(B-1)-k. The corresponding expression is

 c(B_m)/Z_B = sum_(j=0)^(B-2)
 [x^(j+2)]S_m(x) (B-j-2)!/(B(B-1)!j!) + o(1).

For fixed j the coefficient divided by B^(j+2) tends to
lambda^(j+2)/(j+2)!. Moreover Q <= (1+lambda*x)^2 coefficientwise,
so S_m <= (1+lambda*x)^(B+1). Its summand is at most

 ((B+1)/(B-j-1)) lambda^(j+2)/(j!(j+2)!)
 <= (j+3) lambda^(j+2)/(j!(j+2)!).

Again dominated convergence applies, yielding
F2(lambda)=sum_(j>=0)lambda^(j+2)/(j!(j+2)!).

## Exact rational certificate of a strict gap
The first three terms give F2(7/3)>=21217/3888.
For F0, after j=2 the first omitted term is lambda^3/(3!)^2,
and each succeeding ratio is at most lambda/4^2=7/48.
Consequently F0(7/3)<=67849/13284.
The difference between these rational bounds is 55709/159408>0.
Therefore c(B_m)>c(A_m) for all sufficiently large m.
