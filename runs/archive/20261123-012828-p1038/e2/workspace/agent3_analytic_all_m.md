# General-m extension: the literal definitions imply S=Z_{>=1}

This supplements agent3_analytic_m1.md. The same fixed geometry works for every fixed m: lower cluster at -30, upper at 3/5, h_-=0,h_+=1/10,r=1,R=100. Let a=b=A=mq. Use x,y,u,v,G_A,G_B,g_A,g_B,tau_A,tau_B as defined in that note. All scalar inequalities are independently checked by agent3_exact_scalar_checks.py.

## Ring polynomial factors
Let zeta=exp(2 pi i/m), d=1/10,
D_j=d+sqrt(d^2+|100 zeta^j-1|^2),
C_m(T)=prod_(j=1)^(m-1) (1+i exp(-pi i j/m) T),
H_A(T)=prod_(j=0)^(m-1) (1-(100 zeta^(-j)-1)T/D_j),
H_B(T)=prod_(j=0)^(m-1) (T+(100-zeta^j)/D_j).
Put F_A=C_m H_A and F_B=C_m H_B. Directly from the problem's factors, the A_0 and B_0 polynomials are
P_A(T)=G_A(T)^A F_A(T), P_B(T)=G_B(T)^A F_B(T).

C_m has strictly positive real coefficients: pair factors j,m-j to obtain 1+2 sin(pi j/m)T+T^2, with an extra 1+T when m is even. Similarly H_B has strictly positive real coefficients: each conjugate pair gives T^2+2(100-cos theta)/D_j T+|100-exp(i theta)|^2/D_j^2, and the real factors have positive constants. Thus all coefficients of F_B are strictly positive.

Put q_0=99/(1/10+sqrt((1/10)^2+99^2)), the cross-ring slope denoted q in the m=1 note; it is unrelated to the integer q in A=mq. Then F_A(v)>0: C_m(v)>0; each nonreal conjugate pair in H_A evaluates to a positive modulus square; the j=0 factor is 1-q_0 v>0; if m is even the extra real factor j=m/2 is positive. Nonreal pair factors cannot vanish at positive real v.

## Cyclic blocks
Here is an explicit covariance check, including the within-ring ordering convention. For any ordered horizontal pair with Delta=w_j-w_i, define the canonical factor h_(ij)=1-conj(Delta)/|Delta| T. If i<j it is the original factor. If i>j, the original factor is T-Delta/|Delta|=(-Delta/|Delta|)h_(ij). Thus within-ring factors differ from the canonical factors only by nonzero constants c_i depending on m and the vertex index (not on height or radius). Canonical within-ring products at vertex i are exactly C_m(zeta^(-i)T).

For the A_i polynomial, each of the a lower-axis factors T+x_l zeta^i contributes a scalar zeta^i on substituting zeta^(-i)T. All upper-axis and A-to-B factors transform by that substitution without a scalar. Consequently P_(A_i)(T)=c_i zeta^(ia)P_A(zeta^(-i)T). For B_i the a lower-axis factors and m B-to-A factors each contribute zeta^i; hence P_(B_i)(T)=c_i zeta^(i(a+m))P_B(zeta^(-i)T). These scalars are all nonzero; indeed the displayed zeta powers are 1 because a=mq.

Rescale the rows by these nonzero constants. The discrete Fourier combination (1/m)sum_i zeta^(ie)P_A(zeta^(-i)T) is exactly sum_(d congruent e mod m)[T^d]P_A T^d, and likewise for B. This Fourier transformation is invertible. The axial rows already lie in single residues. Grouping columns and rows by residues now gives the following real diagonal blocks. Therefore the full matrix is singular iff one of these blocks is singular. The row rescalings and Fourier transformations are fixed throughout radial scaling (their constants depend only on m and vertex index), so the block determinants below are continuous real functions along that path.

For e=0,...,m-1 use z=T^m. The block has size 2q+2, lower axis rows z^j(1-x^m z)(1-y^m z), 0<=j<q, upper rows z^(q+j)(z-u^m)(z-v^m), 0<=j<q, followed by ring rows with coefficients [T^(e+mj)]P_A and [T^(e+mj)]P_B, j=0,...,2q+1.

Define dual kernels for s=u,v by
K_s(j)=s^(m(j-q)) for j>=q,
K_s(j)=C_s x^(m(q-j))+D_s y^(m(q-j)) for j<=q,
C_s=(s^m-y^(-m))/(x^(-m)-y^(-m)), D_s=1-C_s.
Exactly as for m=1, K_s annihilates all axis rows, K_s(j)>0, and
K_s(j)<=D_s s^(m(j-q)).
The block determinant has the same sign as E_e=A_(u,e)B_(v,e)-A_(v,e)B_(u,e), where A_(s,e) and B_(s,e) denote pairing the respective ring row with K_s. Orientation is positive: boundary Wronskian v^m-u^m>0, and all recurrence transfer determinants are positive.

## Exponential estimates
All constants below may depend on m,e but not A.
The coefficientwise absolute value of P_A is bounded by G_A^A times the polynomial of absolute values of coefficients of F_A. The positive-kernel bound gives
|A_(u,e)|<=C g_A(u)^A, 0<B_(v,e)<=C g_B(v)^A.

For A_(v,e), replace K_v(j) by v^(m(j-q)) for all j. The full pairing becomes
v^(-A-e)/m * sum_(h=0)^(m-1) zeta^(-eh) P_A(v zeta^h).
The h=0 term is F_A(v)/(m v^e) g_A(v)^A>0. Every other mode is exponentially smaller: G_A has strictly positive coefficients in degrees 0,1,2, so |G_A(v zeta^h)|<G_A(v) whenever h!=0. The correction from indices j<q is O(g_A(tau_A)^A), by the same argument as m=1 (now degree d=e+mj satisfies d-A-e<0). Since g_A(tau_A)<g_A(v), it follows that
A_(v,e)>=c g_A(v)^A>0 eventually.

Finally positivity and K_u(q)=1 imply
B_(u,e)>=[T^(A+e)]P_B >= [T^e]F_B * [T^A]G_B^A.
The elementary central-coefficient argument in agent3_analytic_m1.md gives
[T^A]G_B^A >= g_B(tau_B)^A/(2A+1).
Therefore
E_e <= C [g_A(u)g_B(v)]^A - c [g_A(v)g_B(tau_B)]^A/(2A+1)
     <= C (19/4)^A - c (27/5)^A/(2A+1)<0
for all sufficiently large A=mq. Every one of the finitely many m blocks is therefore negative for sufficiently large q.

## Distinct heights and positive radial endpoint
For a chosen sufficiently large q, split lower heights as -30+j epsilon and upper as 3/5+j epsilon, 0<=j<A. Each cyclic block remains real and continuous and its determinant remains negative for sufficiently small positive epsilon.

Now scale both radii by t>0, keeping all the distinct heights fixed. The internal ring factors C_m are independent of t. As t decreases to zero, cross-ring H_A tends to 1 and H_B tends to T^m; all lower-axis direction ratios and upper-axis ratios tend to zero. Hence
P_A -> T^A C_m, P_B -> T^(A+m) C_m;
lower axial row i -> T^(i-1), upper axial row j -> T^(A+j-1+2m).
Write c_e=[T^e]C_m>0. In residue e, the limiting block rows are
1,z,...,z^(q-1);
z^(q+2),...,z^(2q+1);
c_e z^q;
c_e z^(q+1).
Its determinant is c_e^2>0, because moving the last two rows across q upper rows gives sign (-1)^(2q)=1.

Thus each real block determinant is negative at t=1 and positive for sufficiently small t>0. By the intermediate value theorem it vanishes at an admissible t in (0,1). The resulting configuration is singular, obeys all strict height/radius inequalities, and has n=2mq+2m. Since q can be arbitrarily large, every positive integer m belongs to S.

Conclusion for the literal displayed definitions: S=Z_{>=1}. In particular the requested exclusion of m=1,2, and hence the stipulated answer, are false.
