# Unconditional proper support of weight68, codimension5

THEOREM. For M>=11, every word of weight68 in RM(M-5,M) has an affine-linear factor.

Parseval gives a nontrivial Walsh magnitude>=12: coefficients are multiples4, and their mean square is68(2^M-68)/(2^M-1)>64. A hyperplane section therefore has weight<=28. In codimension4 the minimum is16, and the firm <32 KT classification shows every such section has a linear factor (its order M-5>=6 exceeds4). Thus original support has an empty affine codimension-two flat.

Write branches0,a,b,h on n=M-2 variables, of degree<=p=M-6, with a+b+h degree<=p-1. Sorting nonzero branch weights, minimum is16 and second16or24. Hence tuples are(16,16,36) and(16,24,28). If an additional branch is zero, the whole word is already properly supported.

A common top linear factor ell of a,b is also a top factor of h. The branches below32 then are supported in an ell-level (otherwise the two ell-levels each have minimum16); the36 branch has the same conclusion because16+20 is impossible by firm <32 KT, and any other two nonzero levels total>=40. Three branch levels can be fitted by an affine function of the two selector bits, giving a global affine support hyperplane.

For(16,16,36), a,b are minimum affine4-flats, and their top p-form annihilator spaces have dimensionp in n=p+4. Sincep>=5, they intersect nontrivially. This gives ell.

For(16,24,28), alpha=TOP_p(a) is decomposable; beta=TOP_p(b)=vol(F_(p-2)) wedge q4 for rank4 quadratic q. Gamma=alpha+beta is either vol(F'_(p-2)) wedge rank6 quadratic, or vol(G_(p-3)) wedge sum of complementary cubic monomials (the two <32 KT forms for28).

If alpha shares a factor with F, done. Otherwise p+(p-2)<=n=p+4, hencep<=6. Forp5, the2/3 flattening ranks are alpha10,beta16,gamma22or19. A shear of Q4 byF puts the support intersection intoQ4; one image intersection is0 and the transposed image intersection at most the line<q>, so rankgamma>=10+16-1=25, contradiction. Forp6, middle3 ranks are20,32,44or38; both image intersections vanish under the same shear, so rankgamma>=52, contradiction. These are the same canonical rank checks as agent4_weight136_flattening_checks.json. Thus a common factor always exists and the theorem follows.

No KTA above2d normal-form statement or numerical gap is used.
