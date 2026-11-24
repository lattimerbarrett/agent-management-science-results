# Exact finite-dimensional discrepancy certificate
This is a claim about the computed spectral shape model only, not an asserted
solution of the original PDE.

At n=19 set m=18 and P(x')=x_1^2-x_2^2. Let
h=P[1-469|x'|^2/1000+29|x'|^4/500-1461|x'|^6/1000000].
Let K be the positive spectral quadratic form sum_l ((l-1)(l+n-1))^2
kappa_l ||f_l||^2 for compactified boundary displacement f=2h/(1+r^2).
For translated/dilated graph h_{xi,epsilon}(x)=epsilon^{-1}h(xi+epsilon x),
put F=-K. The exact scripts compute a strict local minimum at xi=0,
epsilon=sqrt(t0), with
4453007/5000000 < t0 < 1781203/2000000.

The scale polynomial cp(t)=sum_ij(2+2i+2j)Gij ai aj t^(i+j)
has positive/negative signs at bracket endpoints and cp'<0 throughout
that bracket. Hence IVT gives a unique root there, and the F scale Hessian
is -2t0 cp'(t0)>0.

Individual coordinate reflections preserve h, so all translation gradients
and all off-diagonal Hessian entries vanish at xi=0. Interchanging x1,x2
changes the sign of h but not its quadratic energy, so support-axis Hessians
agree. O(m-2) invariance makes all transverse-axis Hessians agree.
The script certifies both eigen-types have correct strict signs throughout
the root bracket using exact rational interval arithmetic. Thus these two
translation signs and the scale sign certify the entire model Hessian.

Machin alternating-series rational bounds enclose pi; no numerical root
or eigenvalue is trusted for certification. Floating point only proposes
a root bracket, whose endpoint and derivative signs are then checked exactly.

Files: agent3_n19_model_certificate.py/.json. Its exact translation matrices
are provided by agent4_translation_exact.py; interval utilities are shared
with agent4_translation_certificates.py.

This certificate is the obstacle to promoting our local model into the
prompt's claimed sharp n=21 theorem: the same local criticality already
exists at n=19. A source theorem or an identified missing analytic term
is needed to resolve that discrepancy.
