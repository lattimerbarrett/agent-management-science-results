# Complete q224/P32 cubic-lift lemma (agent_2)

Let q=z0*z1+z2*z3+z4*z5 on F2^6 and Q={q=0}, |Q|=36.
Let t=(t0,t1,t2). Every cubic h(z,t) for which its restriction to
Q x F2^3 has weight32 yields F(z,t,y)=y*q(z)+h(z,t), a cubic
weight288 word on10 variables. We prove EVERY such support S has
cl3(S)=S and K3(S) perpendicular K5(S). This includes ALL h choices,
not one arbitrary Gaussian solution per outside set.
Here Kd(S)={labels on S orthogonal to all monomial evaluations degree<=d}.

## Finite linear algebra inputs, actually computed
`agent2_Q6_quadsmall.py/.json`:
* restriction RM(2,6)|Q has dimension21; all2^21 words enumerated.
* its minimum positive weight6, with336 words weight6 and945 weight8.
* restriction RM(3,6)|Q is the entire even-weight space (dimension35).
* restriction affine functions has positive weights16,20,36. The63
  weight16 words are L_v(z)=B(v,z)+q(v), v nonzero, B polar form of q.
  This last bullet also follows immediately from the quadratic Gauss sum.
`agent2_T288_cubic10_k32_remaining.py/.json`:
* on Z={q=0,z0=0} (20 points), degree2 evaluation rank15 and degree3
  evaluation rank20. Their vanishing spaces are respectively
  z0*RM(1,6)+<q> (dimension7), and z0*RM(2,6)+q*RM(1,6) (dimension22).
  The script computes the ranks AND the ranks of these proposed generators.

## Reduction by radical degree
Write h=h0(z)+sum_i t_i a_i(z)+sum_{i<j}t_i*t_j L_ij(z)+c*t0*t1*t2,
where h0 cubic, ai quadratic, Lij affine.
If c=1 every one of36 fibres has odd positive weight, contradiction.

If some Lij is nonzero as a function on Q, every fibre in its support
has weight>=2, so |supp Lij|<=16 and hence equals16. All those fibres
have weight2 and all remaining fibres vanish. Any other Lkl is supported
in the same16-set, hence equals0 or Lij by the affine minimum16.
The rank2 alternating form in3 radical variables can be sent to t0*t1.
All weight16 affine functions L_v are equivalent under affine q-isometries:
A_u(z)=z+(B(z,u)+q(u)+1)u preserves q, and its linear part is the
symplectic transvection with vector u. These generate Sp(6,2), transitive
on nonzero v. Thus take L=z0.

Now h vanishes on Z x F2^3. The t2 coefficient vanishes on all Q
(otherwise a rank2 quadratic fibre has weight4 rather than2), so is a
multiple of q. By the computed vanishing ideals, modulo q*affine,
h=z0*(t0*t1+a(z)*t0+b(z)*t1+d(z)), a,b affine,d quadratic.
Weight2 on every fibre over Q with z0=1 forces d=a*b there. Thus
z0*(d+a*b) is cubic vanishing on Q, so belongs q*RM(1,6).
Radical shears and replacing y by y+affine reduce F to
  y*q+z0*t0*t1.
Its support is directly checked to have K3 dimension144, K5 dimension11,
zero mixed Gram, and cl3 closed. Hence ALL radical-degree2 cases done.

If all Lij=0, put A={z in Q: some ai(z)!=0}. A nonconstant affine fibre
has weight4, so |A|<=8. Each nonzero ai restriction has weight6 or8.
Two different such restrictions cannot both have union of supports <=8:
their nonzero difference would have weight<=4, contradicting minimum6.
A GL(3,2) radical change therefore leaves either all ai=0, or just t0*a
with wt(a)=6 or8. In the latter case, counting fibre weights gives
  4*wt(a)+8*|supp(h0) outside supp(a)|=32.
Since h0|Q is even, the complete choices are exactly:
* wt(a)=6: one outside point (30 choices), odd subset inside (32 choices);
  336*30*32=322560 cases.
* wt(a)=8: no outside point, even subset inside (128 choices);
  945*128=120960 cases.
Every one of these443520 cases was built as a72-point core on8 variables,
with the two unused radical variables factored off. `..._radlinear.py`
checks K3(core) dimension9 and self-orthogonality in EVERY case. Full
support is core x F2^2. It is 6-even, so core is4-even. K4(core)=<1>:
a proper nonzero4-even subset and its complement would have weights
32 and40, but40 is absent below twice minimum32 (strict KT theorem).
Also K5(core)=0, since the whole72-point core is not5-even (KT again).
These facts imply mixed Gram zero for the full product as below.

If all ai=0, h0 has exactly four points on Q: all C(36,4)=58905 choices.
Full support is a36-point core on7 variables x F2^3. Every case was built
and K3(core)=<1>, K4(core)=0, K2(core) perpendicular K3(core) checked.
Counts by dimK2: 8:7560, 9:45360, 10:5040, 11:945. These also follow
qualitatively from strict KT: a proper nonzero3-even subset of the36-core
would have weight16, leaving20 (impossible). Full mixed Gram zero follows.

## Product identity used above
For C x F2^r, write a label as sum_J t_J h_J. Then
  h in Kd(C x F2^r) iff h_J in K_(d-r+|J|)(C) for EVERY J.
For negative index K is the full label space. Proof: sum moments over
the radical variables, then descend through J by inclusion.
Inner products of two label monomials vanish unless J union L=[r].
Consequently for r=2, K3 perpendicular K5 follows from
K1 perpendicular K5, K2 perpendicular K4, K3 perpendicular itself on C.
For r=3 it follows from K0 perpendicular K5, K1 perpendicular K4,
and K2 perpendicular K3 on C (all larger-index pairs follow by nesting).
These are exactly the verified core conditions above.

Finally every S considered has cubic indicator on10 variables. Any outside
point is separated by 1+F, of degree3, so cl3(S)=S. The already-proved
mixed-Gram graph-lift inheritance lemma now shows all iterated K5 graph
lifts remain cl3 closed. This completes the q224/P32 branch.
