# Countable spectral-compression norm detection

## Statement
Let A be a unital AW*-algebra and 0 <= a <= b in A. For each positive
rational t let q_t be the carrier projection of (t*1-a)_+; this is the
spectral cut 1_{(-infinity,t)}(a). If

    ||q_t b q_t|| = ||q_t a q_t||   for every positive rational t,

then b=a. Thus a strict ordered increase is detected by one of this
countable family of compression norms. No quasitrace or finiteness is used.

## Proof
Put c=b-a >= 0 and R=||a||. For rational t>R, q_t=1, so the hypothesis
implies ||b||=R and hence b<=R*1. For every positive rational t, positivity
and the norm hypothesis imply

    q_t b q_t <= ||q_t a q_t|| q_t <= t q_t,
    q_t c q_t <= (t*1-a) q_t.                         (1)

Suppose c is nonzero. Choose a state psi with psi(c)>0. The positive linear
functional f -> psi(c^(1/2) f(a) c^(1/2)) on C(sigma(a)) has a finite positive
Radon representing measure mu, with total mass psi(c)>0. This is a measure
on the ordinary compact spectrum; we do NOT identify its values on Borel
sets with psi evaluated on AW* spectral projections.

Fix positive rational t and positive integer n. For s in sigma(a) write
r=(t-s)_+ and define

    f_n(s) = r/(r+1/n)^2,     g_n(s)=sqrt(f_n(s)).

These are continuous functions, q_t g_n(a)=g_n(a), and
0 <= (t-s) f_n(s) <= 1. Sandwiching (1) by g_n(a) gives

    0 <= g_n(a) c g_n(a) <= 1.

The C*-identity ||z*z||=||zz*||, applied to z=c^(1/2)g_n(a), consequently gives

    0 <= c^(1/2) f_n(a) c^(1/2) <= 1.

Apply psi. As n increases, f_n(s) increases pointwise to
1_{s<t}/(t-s), with value zero when s=t. Monotone convergence yields

    H(t) := integral_{s<t} dmu(s)/(t-s) <= 1            (2)

for positive rational t. For fixed s, the function of t equal to 0 for
t<=s and 1/(t-s) for t>s is nonnegative and lower semicontinuous. Fatou's
lemma therefore makes H lower semicontinuous on (0,infinity). Approaching
any t>0 by positive rationals in (2) proves H(t)<=1 for every t>0.

But Tonelli's theorem, using sigma(a) subset [0,R], now gives

    R+1 >= integral_0^(R+1) H(t) dt
        = integral_[0,R] (integral_s^(R+1) dt/(t-s)) dmu(s).

Every inner integral is infinite, including s=R. Since mu has positive
mass, the right side is infinite: a contradiction. Thus c=0.

## Scope / remaining gap
This detects increases from a FIXED reference a. In an omega_1 increasing
chain, eventual constancy of these countably many norms need not begin at
the ordinal carrying that reference. Applying the lemma at a later element
introduces new spectral projections. No solution of that changing-reference
problem, nor of the user's diffuse finite-AW* problem, is claimed here.

## Computational checks
agent3_spectral_norm_detector_checks.py checks exact rational finite-matrix
certificates for a rational subfamily: known spectral cuts, a nonzero
positive increment, and an explicit Rayleigh witness proving strict norm
increase. It also verifies the scalar regularizer identities symbolically.
The infinite-dimensional scalar-measure argument above is analytic, not
certified by those finite computations.
