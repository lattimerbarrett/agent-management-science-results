# Boundary-linking lower-bound criterion
Let g=25, h=24. Let X=M_h,2 and Y=M_h,2^rt, with rational-tail divisor D=Y\X. Its normalization is M_h,1 and its tail is M_0,3. Let psi1,psi2 be the stable marked cotangent classes, and kappa denote logarithmic pointed classes.

Suppose b is a rational degree-12 polynomial in kappa,psi1,psi2, each term having positive total psi-degree, and suppose (psi1+psi2)b=0 in CH^13(Y;Q). For z in CH^12(X;Q), choose any extension zbar to barM_h,2 and put ell_b(z)=integral lambda_h lambda_(h-1) b zbar. This is independent of zbar:
* On every boundary divisor other than D, lambda_h lambda_(h-1) restricts to zero. On a nonseparating divisor lambda_h=0. On a separating divisor with two positive-genus factors, the restriction is a sum each containing lambda_a^2=0.
* On D, each psi_i=0 since its marked rational component is M_0,3. Hence b|D=0.
Projection formula and Chow localization therefore show boundary-supported differences have zero integral.

Moreover ell_b((psi1+psi2)a)=0 for every a in CH^11(X;Q), even non-tautological a. Indeed (psi1+psi2)b vanishes on Y, so any extension of it is supported on the remaining boundary divisors of barM_h,2; multiplying by lambda_h lambda_(h-1) kills it by the same projection-formula argument.

Let F be a degree-12 kappa polynomial on M_25. If F=0 in its Chow ring, Chow localization on the partial compactification M_25 union Delta_irr^o writes its extension as i_*a for a in CH^11(Delta_irr^o;Q). Pulling back to the ordered normalization X and applying the self-intersection formula gives F(kappa_h,2)=-(psi1+psi2)a', because the boundary normal line is (L1 tensor L2)^dual. The restriction of the unpointed stable kappa_i is exactly the pointed logarithmic kappa_i: normalization pulls the dualizing line back to omega(p1+p2).
Consequently ell_b(F)=0. Thus ell_b(F) nonzero proves F nonzero on M_25.

For genus h=24, dim barM_h,2=71, deg(lambda_h lambda_(h-1))=47, and deg b=deg F=12, so the integral has degree71 as required. This is not the ordinary genus25 socle pairing; it is a genuine extra linking functional.

To complete a 44-dimensional lower bound, use the computed 43-dimensional ordinary socle-pairing quotient and its unique radical representative F modulo FZ relations. An actual RT-annihilator b with ell_b(F) nonzero separates F from those 43 classes.
