# Direct completion of (64,126,136/144), via Hilbert/flattening bound

First an elementary general lemma. Let S support h in RM(6,12), and
suppose S has affine span12. Let T in Lambda^6(F2^12) be the degree6
moment form: coefficient at I is sum_{x in S} product_{i in I}x_i.
All moments of degree<=5 vanish since RM(6,12) is orthogonal to RM(5,12).
Consequently T is Hodge(TOP6 h). Let R2,R3 be its 2/4 and3/3 flatten ranks.
Let C_j be evaluations on S of all polynomials of degree<=j, H_j=dim C_j.
Full affine span gives H1=13. A quadratic polynomial vanishing on S
has leading quadratic in kernel of the2/4 flattening T: multiply by an
arbitrary quartic and sum on S; only degree6 products survive. Its leading
part map is injective on vanishing quadratics because no nonzero affine
linear polynomial vanishes on S. Thus
 H2 >= 13+R2.
The vanishing moments<=5 imply C2 is isotropic and C3 subset C2^perp.
The Gram rank on C3 is exactly R3, because all products involving a
monomial of degree<=2 vanish, and products of two cubic monomials give
the3/3 flattening T. The ambient nondegenerate quotient C2^perp/C2 has
dimension |S|-2H2. Therefore
 |S| >= 2H2+R3 >= 26+2R2+R3.  (HILBERT-FLATTENING BOUND)
No KTA classification or computational assumption occurs in this lemma.

Now the (64,126) branch has leading h=A+B+C, three decomposable6-forms,
where B,C are complementary (firm KT for b126). Also qtop(h)=0 since
wt h136/144 is divisible4. Since q(B+C)=1, exactly one of A,B or A,C
is a complementary pair; choose A,B complementary. Use X=a-direction,
Y=B-direction. Since C-direction is complementary to B, it is a graph
Y=M X. Thus, after independent X,Y bases, the leading form is
 omega_d = X1...X6+Y1...Y6+product_i(Y_i+X_i if i<=d else Y_i),
where d=rank M. The middle quadratic invariant of omega_d is det M,
so qtop0 implies d<=5. If d0 or1, omega has a nonzero linear wedge
annihilator; the already-checked agent1_64126_proof.md excludes these
cases by elementary topfactor+purepair5-gap reasoning.

For d>=2, compute the ranks of T=Hodge(omega_d). The small exact GF2
bitmatrix checker agent3_64126_hilbert_checker.py gives:
 d       2    3    4    5
 R2     38   42   44   45
 R3     52   58   60   60
 bound 154  168  174  176.
If h has full affine span12, the Hilbert bound excludes wt136/144.
If h has proper affine support, its leading form has a nonzero linear
wedge annihilator, so agent1_64126_proof.md again excludes it. Thus
all cases are excluded, with only firm KT below2d and the proved
purepair5 moment gap. No universal KTA geometry is required.
