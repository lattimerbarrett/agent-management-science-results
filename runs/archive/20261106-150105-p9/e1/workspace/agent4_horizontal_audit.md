# Independent audit: monotone horizontal Cantor lower bound
Fix p,q and K large. Put epsA=K^-1, epsB=K^(-1/(p-1)), rhoA=1-epsA, rhoB=1-epsB, a=rhoA^(1/p), b=rhoB^(1/q), r=ab/4, h=K^(-1/p). Let C be the two-child Cantor set with child ratio r and t its monotone distribution staircase. Set D=min(dist(x,C),1), and extend t by 0 and 1 outside [0,1].

Define alpha,beta by 2r^(1-alpha)=rhoA, 2r^(1-beta)=rhoB. If d=log2/log(1/r), then alpha/p+beta/q=d exactly, and alpha,beta<1-d. For K large (depending p), r lies in a fixed compact neighborhood of 1/4 and alpha,beta lie in a fixed compact subset of (0,1).

Put A=D^-alpha, B=D^-beta and
 F=[[h A^(1/p),h A^(1/p)t],[0,B^(-1/q)]], W=(F*F)^(p/2).
This is a matrix weight: ||W||=||F||^p <=C_p(h^p A+B^(-p/q)), locally integrable. Polar decomposition gives |W^(1/p)f|=|Ff| and the exact equality of kernel operator norms used in the problem.

Distance estimates: uniform Ahlfors regularity gives |I intersect {D<u}| <= C |I|^d u^(1-d), u<=|I|<=1. Layer cake yields avg_I D^-theta <= C(1-rho)^-1 |I|^-theta, with rho=2r^(1-theta). Indeed (1-d)-theta=log(rho)/log(r) is comparable to 1-rho. If dist(I,C)>=|I| then D is comparable on I; otherwise its positive powers are bounded by C|I|^(positive exponent). These two cases prove [D^-theta]_{A_s} <=C_s/(1-rho), for every fixed s>1. Large intervals use capped D. The Cantor probability satisfies mu(I)<=C|I|^d, so osc_I t<=C min(1,|I|^d).

The three nonzero entries of F(x)F(y)^-1 are
 (A(x)/A(y))^(1/p), (B(y)/B(x))^(1/q), h A(x)^(1/p)B(y)^(1/q)(t(x)-t(y)).
Mixed-norm Minkowski and the preceding estimates imply
 [W]_{A_p} <=C_p{epsA^-1+epsB^(-(p-1))+h^p epsA^-1 epsB^(-(p-1))} <=C_p K.
For the last entry, use avg A (avg B)^(p-1)(osc t)^p and the exact zero exponent pd-alpha-(p-1)beta=0.

Let E_n be the union of gaps deleted after n binary choices (the central gap is E_0). Its A-mass is GA rhoA^n, and its B-mass is GB rhoB^n, where GA,GB are central-gap integrals and bounded above and below uniformly. Let nu_n^A,nu_n^B be the corresponding normalized probability distributions.

For k<=min(m,n)-2 select x in the 00 grandchild, y in the 11 grandchild of each length-k cylinder, and include reverse order. Their probability is 2^(-k-3); t-difference >=2^(-k-1); distance <=r^k. Distinct k regions are disjoint because their first differing binary digit is k+1. All other pairs have nonnegative commutator kernel because t is monotone. Hence
 integral integral (t(x)-t(y))/(x-y) dnu_m^A(x)dnu_n^B(y)
 >= (1/16) sum_{k=0}^{min(m,n)-2}(4r)^(-k).

In the conjugated Hilbert operator, choose input G=(0,B^(1/p)phi_n) on E_n and dual test J=(A^(1/q)psi_m,0) on E_m, finitely many levels. Normalizing their Lp and Lq norms gives the radial matrix lower bound (including the Hilbert factor 1/pi)
 (h GA^(1/p)GB^(1/q)/(16pi)) a^m b^n sum_{k<=min(m,n)-2}(ab)^(-k).
After shifting both indices by 2 this is a fixed bounded-positive factor times h L_a L_b*, where (L_a)_{ij}=a^(i-j) for i>=j. Its lp norm is exactly 1/((1-a)(1-b)): upper by convolution Young, lower by finite constant sequences on long windows far from the starting boundary. Since 1-a is comparable to epsA and 1-b to epsB (p fixed),
 ||H||_{Lp(W)} >=c_p h/(epsA epsB)=c_p K^(1-1/p+1/(p-1)).

The finite-window inputs above correspond to original f=(-t B phi,B phi), supported in finitely many open gaps. In each gap t is constant. Smoothly truncate B phi within these gaps and away from endpoints, then approximate smoothly. Weighted input norms converge. Pair against similarly truncated dual tests; different selected gaps have positive separation and same-gap commutator vanishes, so the bilinear form converges. This supplies smooth compactly supported admissible f with the same lower bound up to a fixed factor.

All constants above are uniform as K tends to infinity for fixed p. Therefore every gamma below 1-1/p+1/(p-1) fails, by choosing K large enough that c_p K^alpha > C(C_p K)^gamma. Combined with the upper half, this proves the claimed infimum. This audit contains no appeal to a recent lower-bound theorem.
