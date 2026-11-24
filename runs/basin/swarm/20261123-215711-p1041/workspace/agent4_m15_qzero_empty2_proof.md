# Conditional m=15, Q=0 exclusion (proved reduction)

Assumption still needed: every putative word of weight w in {322,326,330,334} has an empty affine codimension-two flat. This file does NOT prove that assumption.

Given it, affine-normalize f on F2^2 x F2^13 to have branches (0,a,b,h). Each a,b,h has degree at most7; c=a+b+h has degree at most6. Order the three nonzero branches by weight a<=b<=h using GL(2,2). By the standard <2.5d numerical KTA list for codimension6, the only possible small branch weights <=156 are
64,96,112,120,124,126,128,136,144,148,152,154,156.
In particular, a<=floor(334/3)=111, so |a|=64 or96.

Let G=F2^13 and let A,B,H be support vectors in F2[G]. Embed the four branches by the outer group basis s,t: F=sA+tB+stH. For even support vectors define
q(V)=sum_{unordered distinct x,y in supp V} e_(x+y) + (|V|/2 mod2)e_0.
For even vectors its polarization is q(V+W)+q(V)+q(W)=VW. Multiplying a support by a group element leaves q unchanged. The coefficient at outer st in q(F) is therefore exactly AB, coming only from the sA,tB cross product. If the derivative parity functional Q of f is zero and |f|=2 mod4, the earlier group-algebra parity lemma gives q(F)=J_15. Hence
AB=J_13.   (1)
Similarly AH=BH=J_13, although only (1) is needed below.

CASE |a|=64. The minimum-weight theorem says a is the indicator of an affine6-flat L. Equation(1) says every L-direction coset meets b oddly. There are128 such cosets, hence |b|>=128. But sorted b<=floor((w-64)/2)<=135, and KTA permits only b=128 in this interval (the next allowed weight is136). It would then require h=w-192 in {130,134,138,142}, each excluded by the same KTA numerical list. Contradiction.

CASE |a|=96. The second-weight classification says a is supported in an affine8-flat L and its restriction is an unbalanced rank4 quadratic q on L, of weight96. Translate L to linear. Decompose b into its32 cosets of L. Because A is supported on L, (1) says separately on each L-coset that
q * B_t = J_L.
Each B_t must have at least4 points:
- zero points gives zero convolution;
- an odd number (1 or3) of translates of q leaves its nonzero homogeneous quadratic part, so cannot be the constant1 function;
- two points gives a first derivative of q. It is constant only in a radical direction. An unbalanced quadratic has no nonzero linear component on its polar radical (otherwise it is balanced), so this constant derivative is0, never1.
Thus |b|>=32*4=128. But sorting gives |b|<=floor((334-96)/2)=119, contradiction.

Therefore, CONDITIONAL ON THE EMPTY CODIMENSION-TWO FLAT LEMMA, no Q=0 codeword in RM(8,15) has any of the four target weights. Combined with the already proved Q!=0 argument (conditional on the m14 holes), this reduces all dimensions to m14 once the empty-flat KTA consequence is verified.
