# Convergence when the number of distinct active eigenvalues is at most s+2

Assume the standard monic-normalized residual map F, its Lyapunov identity, square-summability of even steps, and the minimal-support trapping lemma in agent4_trapping_lemma.md. Then every nonterminating orbit supported initially on at most s+2 distinct eigenvalues has a convergent even normalized residual sequence, for every s.

It suffices to prove this for exactly N=s+2 eigenvalues, since support s+1 is an exact two-cycle, and support at most s terminates. A coordinate annihilated at a finite time stays zero. There are finitely many possible such events, so discard the finite initial segment after the last such event. We may assume all N weights w_{k,i}>0 and all p_k(lambda_i) !=0 forever.

Let Delta(z)=product_i(z-lambda_i), c_i=1/Delta'(lambda_i), p_k the monic degree-s orthogonal polynomial for w_k, and H_k^2=sum_i w_ki p_k(lambda_i)^2. Orthogonality implies

 w_ki p_k(lambda_i)=c_i H_k^2 f_k(lambda_i),

where f_k(z)=z-t_k is monic of degree N-s-1=1. Indeed, the partial-fraction sum sum_i w_ki p_k(lambda_i)/(z-lambda_i) has first nonzero Laurent coefficient H_k^2 z^{-s-1}, so its numerator is H_k^2 f_k. Thus f is a continuous function of w on every neighborhood where H>0, including boundary weights. On a face with support S, f_ambient equals product_{j outside S}(z-lambda_j) times the reduced monic dual polynomial.

At every omega point u, F^2u=u and its support has at most 2s points. Its reduced dual polynomial is unchanged by F: if its degree d=m-s-1, equality of the two-step weights implies that the squares of the two monic dual polynomials coincide on m points; since 2d<m, the polynomials coincide. The same holds for the ambient f after multiplication by the inactive-node factors. Consequently f(Fu)=f(u), and continuity and compactness imply t_{k+1}-t_k ->0.

Suppose, for contradiction, that the even residuals do not converge. We claim that t_k crosses spectral nodes only finitely many times. Otherwise, after taking a subsequence, t_k and t_{k+1} straddle a fixed lambda_j. Since their difference tends to zero, t_k,t_{k+1}->lambda_j along this subsequence. Choose a further subsequence of the normalized residuals of a fixed parity converging to an omega point u. Then f(u)(lambda_j)=0. The barycentric identity above and the cycle identity p_u(lambda_i)p_{Fu}(lambda_i)=H_infinity^2 on active coordinates imply u_j=0. Since H_infinity>0, at least s+1 coordinates survive; N=s+2, so exactly s+1 survive and j is the only inactive coordinate.

If its two-step multiplier L_j(u) were not +1, the minimal-support trapping lemma would imply convergence of the entire even sequence, contrary to assumption. Hence p_u(lambda_j)p_{Fu}(lambda_j)=H_infinity^2>0. But at every finite iterate the exact dual identities give

 f_{k+1}(lambda_j)/f_k(lambda_j) = p_k(lambda_j)p_{k+1}(lambda_j)/H_{k+1}^2.

The left side is negative at a crossing. Passing to the omega limit gives p_u(lambda_j)p_{Fu}(lambda_j)<=0, a contradiction. The argument applies to either parity; odd and even omega points are related by F. Exact contact t_k=lambda_j at finite time would annihilate a coordinate and was already excluded. Thus crossings are eventually absent, and all t_k eventually lie in one fixed spectral gap.

The exact scalar root-ordering lemma now makes t_k monotone. Specifically, if f=OP_1(nu), g(z)=z-c, and h=OP_1(nu f^2/g^2), with f's root a and c in the same spectral gap, then sign(root(h)-c)=sign(c-a). This follows either from the Rayleigh/Stieltjes argument or the exact shift-sign identity. The dual recurrence has precisely this form with nu=I(w_k), f=f_k, g=f_{k+1}, h=f_{k+2}. Hence t_k has finite total variation and a limit t_infinity.

Finally the exact two-step weight ratios are

 w_{k+2,i}/w_{k+2,l} = (w_{k,i}/w_{k,l}) [(lambda_i-t_{k+1})(lambda_l-t_k)/((lambda_i-t_k)(lambda_l-t_{k+1}))]^2.

For nodes lambda_i,lambda_l different from t_infinity, logarithms of these ratios have absolutely summable increments, by the finite variation of t_k and bounded derivatives of log|lambda-t| near the limit. Thus every such even weight ratio converges to a finite positive limit. If t_infinity equals one spectral node lambda_j, every omega point has w_j=0 by the earlier cycle/barycentric argument, so that weight tends to zero. All remaining weights therefore converge by normalization. For each remaining coordinate, f_k(lambda_i) and f_{k+1}(lambda_i) eventually have the same sign, so p_k(lambda_i)p_{k+1}(lambda_i)>0 and the even residual component has an eventually fixed sign. The vanishing coordinate is irrelevant. Hence the even normalized residual vectors converge, completing the contradiction and the proof.

This proves the theorem for all s and N<=s+2. In particular, an s=4 counterexample needs at least seven distinct active eigenvalues. It does not yet prove the required universal s=2,3 statements for arbitrary N.
