# The remaining 256/P16 branch in the weight288 classification

The complete coorder7 boundary256 classification is in
agent4_boundary256_gaps260_268.md. For irreducible288 in11 variables,
quotient averaging gives k8->272 or k16->256. Agent3 classified all
k8 branches. This note finishes k16. If quotient256 has affine span<=9,
its outside P16 cannot leave that span (co6 restriction minimum32), so
the original288 has affine span<=10 and is not irreducible11. Thus the
quotient has affine span10 and is exceptional E256 or a quadratic graph
of8 base variables with two independent quadratic outputs.

## Exceptional E256

Write E256=B32 times F2^3, B32 in F2^7. It is2-closed only after adding
16 base points, so cl2(E256)\E256 has128 points. If outside P16 is not
contained in this closure, a quadratic separator selects a nonempty
3-even subset of P16; minimum16 forces this subset to be all P16 and
to be an affine4-flat. An affine4-flat in base7 times radical3 can be
straightened, preserving E256, into Q_d times F2^(4-d), where Q_d is an
affine d-flat in base7 and 1<=d<=4. Radical GL, translations and shears
remove the graph of Q into the unused radical quotient.

The degree5 relative syndrome condition reduces to

    sum nu_(d+1)(Q_d) in span nu_(d+1)(B32).

agent4_T288_E_affineP16.py enumerates ALL affine Q_d (8128,85344,188976,
94488 respectively), for EACH of the three exceptional presentations.
There are304 valid d1 pairs, of which120 are contained in the16 extras
and184 are outside; no d2/d3/d4 solutions. All552 actual outside-cl2
lifts were constructed and checked. Each has affine rank11 and K5
dimension12, exactly affine-evaluation rank, hence admits no nonaffine
graphlift. Its indicator is quartic, so it and all affine embeddings
are4-closed. The contained-cl2 case is independently classified by
agent3's1016-case fibre enumeration, not claimed proved by this file.

## Quadratic-graph quotient: exactly two pencils

Write the quotient support as (x,q1(x),q2(x)), x in F2^8. Affine parts
of the quadratics can be removed. Coorder7 in10 dimensions is exactly
indicator degree<=3. Its indicator is the product of the two graph
equations, so q1 wedge q2=0 in the exterior algebra. Conversely this
condition cancels its degree4 part and suffices.

The two quadratic forms are independent, or the affine span is<10.
We claim that their pencil is equivalent to one of

 A: q1=x0*x1, q2=x0*x2;
 B: q1=x0*x1, q2=x0*x2+x1*x3.

Here is an elementary proof. Put a nonzero form q1 in symplectic normal
form sum_(i=1)^h e_(2i-2) wedge e_(2i-1). If h>=3, coefficient
comparison shows the kernel of q1 wedge - on exterior2 is exactly
<q1>: for a coefficient using vectors from distinct hyperbolic pairs,
choose a third pair to isolate it; coefficients involving radical
vectors are likewise isolated; the remaining pair coefficients must
all be equal. This contradicts independence of q2.

For h2, the same comparison shows q2 is supported on the active4-space.
The Pfaffian quadratic on exterior2 of that4-space has polar pairing
given by wedge. On the2-dimensional pencil its polar pairing is zero,
so its Pfaffian is a linear functional. Some nonzero pencil member is
therefore rank2. For h1 we already have such a member. Choose it as
q1=e0 wedge e1. The wedge condition says

    q2=e0 wedge a + e1 wedge b.

If a,b are dependent modulo <e0,e1>, independence gives pencil A;
if independent it gives pencil B, after absorbing a q1 multiple and
changing the base coordinates. Thus only A/B occur.

## The affine P16 enumeration

The quadratic graph equations vanish on the quotient support. For a
relative outside P16, the separator argument forces P16 to be an
affine4-flat and each graph equation to be constant on it. Let those
constants be epsilon!=(0,0). Projection to base8 is injective on P16,
since a nonzero vertical direction would change a graph equation.
Its image is an affine4-flat A on which both q_i are affine functions.

For pencil A only3 base variables are active and5 are free; for B,
4 are active and4 free. Changes of free base coordinates and free
shears preserve the graph and straighten A into

    Q_d times F2^(4-d),

with Q_d an affine d-flat in the active3/4 space. We enumerate ALL such
Q_d and the THREE nonzero epsilon values. There are

    (51+307)*3=1074 cases.

The actual checker agent4_T288_quadgraph_P16.py constructs each P,
tests affine dimension4, reduces its FULL nu5 syndrome modulo the
quotient's span, and builds each valid288 lift. It finds96 cases:
72 have affine rank11,K5 dimension14, and24 have affine rank11,K5
 dimension13. These are not terminal, so checking only initial closure
would NOT suffice.

## Closure inheritance: K4 orthogonal K5

For a finite support S, write Kd(S) for the kernel of its degree<=d
Veronese columns (binary functions on S with all such moments zero).
Suppose S is4-closed and K4(S) is orthogonal to K5(S). A coorder7
injective graphlift has label h in K5(S). For its support S_h,
K4(S_h) is contained in K4(S) and K5(S_h) in K5(S), under the natural
identification. Thus cross-orthogonality is inherited.

To prove4-closedness is inherited, let (y,t) be outside S_h. If y is
outside S, a base degree4 separator works. Otherwise y in S and
 t=h(y)+1. A hypothetical degree4 column relation for (y,t) against
S_h gives a in K4(S) after adding the unit vector at y to its base
coefficients. Its constant-new-coordinate moment forces

    <a,h> = t+h(y)=1,

contradicting K4 orthogonal K5. This proves the inheritance lemma for
ALL iterated graphlifts, not only one step.

IMPORTANT: one Gaussian solution h per P is NOT enough here. Unlike
exceptional E256, the quadratic-graph quotient has K5 dimension17 for
the star pencil and13 for the rank4 pencil, versus affine dimension11.
Thus each star P needs64 inequivalent h choices modulo affine graph
coordinate changes, and each rank4 P needs4. Agent1 executed the FULL
1824-case enumeration in agent1_T288_quadgraph_ALLh.py/.json:

 star24 P times64 h =1536:
   96 cases (K4,K5)=(63,14),1440 cases(60,13);
 rank4-pencil72 P times4 h =288:
   192 cases(63,14),48 cases(60,13),48 cases(57,12).

EVERY cross Gram is zero. This additional enumeration is essential for
completeness; the original96-seed calculation alone did not prove it.
All1824 initial lifts are quartic on11-space, hence4-closed. The checker
agent4_T288_quadgraph_crossGram.py constructs BOTH complete kernels
and checks EVERY basis pair. It obtains

    72 cases: dimK4=63, dimK5=14, cross Gram ZERO;
    24 cases: dimK4=60, dimK5=13, cross Gram ZERO.

The96-seed cross-Gram calculation is a redundant subset; the ALLh
checker above supplies the required full statement. Consequently all
iterated lifts of this last family remain4-closed.
Together with agent3's k8 and contained-E families, this completes the
needed assertion that ALL coorder7 supports of weight288 are4-closed.
The low irreducible dimension<=10 families need no further enumeration:
any graph label, zero-extended on its original d<=10 coordinates, has
degree<=d-6<=4; its graph equations and the original indicator (degree
<=d-7) separate all outside points by degree<=4.

The global main no-fixed-list claim is NOT proved here. This is a
rigorous low-fringe obstruction used in the292/294 reduction.
