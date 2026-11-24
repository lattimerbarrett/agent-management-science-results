# Finite variation of the residual polynomial near a regular cycle stratum

Let m distinct fixed spectral nodes be present with strictly positive weights, s+1<=m<=2s. Let F be the normalized monic degree-s orthogonal-polynomial weight map and G=F^2. At a two-cycle w, write P=p_w, Q=p_Fw, C=H(w)^2. Assume P,Q are coprime. Then locally the fixed points of G form a smooth s-dimensional manifold, and

 ||p_{Gv}-p_v|| <= K ||Gv-v||^2

for v in a neighborhood of w. Consequently, an orbit remaining in a compact union of such regular charts has finite total variation of its even residual-polynomial coefficients.

Here and below polynomial norms are any fixed coefficient norm.

## Smooth fixed-point family

Put D(x)=product_i(x-lambda_i), d=m-s-1. At every cycle,

 P Q=C+D U,

where U is monic of degree 2s-m. The cycle weights can be written

 w_i=C f(lambda_i)/(D'(lambda_i)P(lambda_i))
     =f(lambda_i)Q(lambda_i)/D'(lambda_i),

with f monic of degree d. Conversely, choose (C,U,f) close to the given values. Since P,Q are coprime, the Sylvester linear map (a,b)->Qa+Pb on polynomials deg a,deg b<s is invertible. Thus the prescribed product C+D U has a unique nearby factorization into monic P,Q, depending analytically on C and U. The roots remain real and simple. Define w by the displayed formula. Barycentric interpolation gives sum_i w_i=1 and sum_i w_i P(lambda_i)lambda_i^j=0 for j<s. The same identities with the updated weights show that Q is the next orthogonal polynomial and G w=w. Positivity persists locally.

The inverse parameters are recovered analytically from w by its orthogonal polynomials, C=H(w)^2, U=(PQ-C)/D, and the monic dual f. Hence these are genuine local coordinates on a smooth fixed-point family. Their number is 1+(2s-m)+d=s.

## Derivative and its rank

Let V_i=(1,lambda_i,...,lambda_i^(s-1)), M=sum_i w_i V_i V_i^T, and N=sum_i z_i V_i V_i^T with z=Fw. For a weight perturbation eta with sum eta_i=0, let a=delta P and b=delta Q (coefficient vectors). Differentiating orthogonality gives

 a=-M^(-1) sum_i eta_i P_i V_i,
 b=-N^(-1) M a.

The derivative of C is delta C=sum_i eta_i P_i^2. Since P_iQ_i=C, it is a linear function of a. If R=DG-I, then

 (R eta)_i=(2w_i/C)[Q_i a(lambda_i)+P_i b(lambda_i)-delta C].

Multiplying by P_i V_i and summing gives zero, because PQ=C and Ma+Nb=0. Therefore Dp_w R=0.

The map eta->a has rank s. Indeed, a failure of rank would give a nonzero polynomial ell of degree<s such that P_i ell(lambda_i) is constant over the nodes. But P is invertible modulo D, with inverse Q/C. Hence ell is congruent to a constant multiple of Q, and since both degrees are below m this is polynomial equality. This contradicts deg ell<s unless ell=0.

Thus ker Dp has dimension d, so rank R<=d. Conversely, R eta=0 implies

 Qa+Pb-delta C=D delta U,

with deg delta U<=2s-m-1. Coprimality makes a->Qa+Pb injective (b is already determined by a), so its preimage of the vector space of constants plus D times such delta U has dimension at most 2s-m+1. Since eta->a is onto and has d-dimensional kernel, dim ker R<=d+(2s-m+1)=s. Consequently rank R>=m-1-s=d, proving rank R=d.

The s-dimensional smooth fixed-point family found above therefore has tangent space ker R, and its codimension equals rank R.

## Error bound and quadratic vanishing

Select d components of Gv-v whose transverse derivatives have full rank. The implicit-function theorem, together with the known fixed-point manifold, gives a local bound

 dist(v,Fix G)<=K1 ||Gv-v||.

The analytic function B(v)=p_{Gv}-p_v vanishes on Fix G. Its entire derivative also vanishes there, because DB=Dp(DG-I)=0 at every cycle in the chart. Taylor expansion around the fixed-point manifold therefore gives

 ||B(v)||<=K2 dist(v,Fix G)^2<=K ||Gv-v||^2.

For an actual residual orbit, ||G w-w||<=2||F^2 y-y||. The latter squared differences have finite sum by the Lyapunov identity. Summing the preceding estimate proves finite variation of the even orthogonal-polynomial coefficients while the orbit remains in a compact regular stratum.

## Limitation

This does not cover vanishing weights or common roots of P,Q. At a boundary +1-neutral coordinate, several fixed-point branches can meet and the rank of DG-I can drop. Those singular strata are precisely the unresolved source of possible polynomial drift. This lemma alone does not establish the required universal s=2,3 convergence theorem.
