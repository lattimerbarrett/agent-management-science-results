# Proved ring lemmas (agent 3)
Let d=h_+-h_->0, z_k=exp(2*pi*i*k/m),
q(theta)=1/(d+sqrt(d^2+R^2+r^2-2Rr*cos(theta))),
c_k=(R*z_k^(-1)-r)q(2*pi*k/m), b_k=z_k*c_k, c0=c_0.
Write C_A=prod(1-c_k*T), C_B=prod(T+b_k).

## Positive coefficients of Q_A=C_A/(1-c0*T)
The elementary identity
  1/(d+sqrt(d^2+u))=(2/pi)*integral_0^infty
     v^2/((v^2+d^2)(v^2+d^2+u)) dv
follows by partial fractions. Put A(v)=v^2+d^2+R^2+r^2,
B=Rr, s(v)=2B/(A+sqrt(A^2-4B^2)). Then 0<s(v)<r/R,
and the Poisson expansion gives the Fourier coefficients
  qhat_j=integral s^j dnu(s), j>=0,
with positive finite measure induced by
  (2/pi)*v^2/((v^2+d^2)*sqrt(A^2-4B^2)) dv.

Let S be the cyclic shift with eigenvalues z_k. The real circulant
C=(R*S^(-1)-r*I)q(S) has eigenvalues c_k. Write C=sum C_j*S^j.
Periodizing the moment formula gives, for 0<=j<m,
  C_j=integral [(R-rs)*s^(m-j-1)-(r-Rs)*s^j]/(1-s^m) dnu(s).
Consequently C_0<C_1<...<C_(m-1), since R-rs>0 and r-Rs>0.
Set D=I-S and L=-DC. Its diagonal is C_(m-1)-C_0>0,
and its j-th offdiagonal is -(C_j-C_(j-1))<0 for j=1,...,m-1.
Thus L is a strict balanced directed-graph Laplacian, and D is a cycle Laplacian.

By simultaneous diagonalization on the complement of constants,
  cofactor(D+T*L)=prod_(k=1)^(m-1)(1-c_k*T)=Q_A(T),
because every cofactor of D is 1. The directed matrix-tree theorem expresses
this as a sum of spanning-tree edge products, each edge weight being a
nonnegative constant plus a strictly positive multiple of T. A cycle tree
alone contributes (1+ell*T)^(m-1) for ell>0, so every coefficient is strictly
positive. For m=1 the quotient is 1.

The same L gives D'=I-S^(-1), D'SC=L and
  C_B(T)=(T+c0)*cofactor(L+T*D').

## Other core facts
Every b_k has positive real part. Pairing conjugates proves C_B has strictly
positive real coefficients. The regular-ring polynomial
 H_m(T)=prod_(k=1)^(m-1)(1+i exp(-pi*i*k/m)*T)
has h_0=1 and h_j/h_(j-1)=cot(j*pi/(2m)); hence h_j>0 and h is log-concave.
The ratio follows by comparing coefficients in
 (1+i*q*T)H(q*T)=(1-i*T)H(T), q=exp(-pi*i/m).

## Short-factor m-section inequality
If h_0,...,h_(m-1)>0 is log-concave and C_0,...,C_m>=0,
with C_0,...,C_(m-1)>0, let p=h*C. Then
  p_q*p_(q+m+1) < p_(q+1)*p_(q+m), 0<=q<m-1,
provided the RHS entries are nonzero (in the degree-2m-2 case the final
numerator on the left is zero).
Proof: expand the two products. Shared monomials C_i*C_j have i<=q and
j>=q+2. Their coefficient on the left minus the right is
  h_(q-i)*h_(q+1+m-j)-h_(q+1-i)*h_(q+m-j)<=0,
by log-concavity and q-i<=q+m-j. All unshared monomials occur negatively;
in particular C_(q+1)^2*h_0*h_(m-1) has a strictly negative coefficient.

Applying this to H_m*C_B and H_m*Q_A proves their initial linear m-sections
have strictly ordered negative roots (allowing the final constant section
for H_m*Q_A). The standard cyclic m-section interlacing operator for
multiplication by (T+t), t>0, preserves this ordered interlacing family.
Thus the full B-ring m-sections have only negative real roots; the full
A-quotient G=P_A/(1-c0*T) has the same property and ordered interlacing.
The actual A-sections are G_q-c0*G_(q-1) for q>0 and
G_0-c0*x*G_(m-1) for q=0, so they are real-rooted, with at most one
positive root, by interlacing.

## Scope / gap
These are structural ring lemmas, NOT a proof of eventual nonvanishing.
A further comparison using the exact Joukowski coupling of the two axis
parameter lists is still required to show the two ring rows remain
independent modulo the axial row span, or to produce any uniform N_m.

Computational files: agent3_ring.py (floating-point canonical identities,
19,000 exact rational short-factor inequalities, and high-precision
cofactor checks); agent2_moment_laplacian.py checks the matrix-tree identity
exactly for rational moment mixtures, m=2,...,15.
