import pathlib,json
p=pathlib.Path('workspace/agent3_E256_threeflat382_obstruction.md')
p.write_text(r'''# Exceptional 256 plus a three-minimum-flat full-Q 382 support cannot yield a critical weight

This is a **constructor obstruction only**, not the main no-fixed-list theorem.
The five critical targets considered are 310,322,326,330,334.

Let E be any exceptional 256 support. By the previously audited boundary classification,
E is an affine image of B x F_2^3 in an intrinsic affine 10-space C, where B is
one of the three 32-point presentations stored in agent3_T280_P12_allorbits.json.
Let A_1,A_2,A_3 be affine 7-flats, with directions U_i, such that
U_1 intersect U_2 = U_2 intersect U_3 = 0, U_1 intersect U_3 != 0,
and their two cross-pair parity hyperplanes have the same normal n and opposite cosets.
Equivalently their XOR T has full pair parity Q=1 and weight382.
All U_i lie in H=ker n; A_1,A_3 occupy opposite H cosets. Relabel leaves so A_2
is in the same H coset as A_3. Then A_1 intersect A_2 and A_1 intersect A_3 are empty,
while A_2 intersect A_3 is a singleton p. Hence

    |E intersect T| = e1+e2+e3 - 2 delta,
    ei=|E intersect Ai|, delta=1_{p in E},
    |E XOR T| = 638 - 2 |E intersect T|.

The desired intersections are respectively 164,158,156,154,152.

## Exact finite data

agent3_E256_threeflat382_spectra.py enumerates **every** affine flat of F_2^7
of dimensions0 through6, by unique reduced-row-echelon direction bases and canonical
coset representatives. Counts by dimension are
128,8128,85344,188976,94488,10668,254, summing387986.
For each of the three B and every nonzero n in F_2^7 it records the complete
intersection-count spectrum for each half n(x)=epsilon, in each dimension.
The data file is agent3_E256_threeflat382_spectra.json.

In particular every half has base intersection maxima at most
1,2,4,8,12,16,24 in dimensions0..6. Half sizes are at most24.
If a d-flat in the product half B_epsilon x F_2^3 projects to an r-flat,
its intersection count is 2^(d-r) times the corresponding base count,
where 0 <= d-r <=3. This formula gives **all possible counts** (no direction
compatibility is claimed or needed for this upper-bound argument).
Consequently its maxima for d<=7 are bounded by
1,2,4,8,16,32,64,96. Every 7-flat count >64 must have d-r=3,r=4,
so its direction contains the entire free F_2^3 and the count is80 or96.
(The base4-flat counts are even, also follows from cubic degree.)

## H cases

If n annihilates the direction of C, E lies entirely in one H coset.
The untouched T slice has weight128 or254. In the first case the other slice
would have weight182,194,198,202,206; all are strict-KT gaps for coorder7.
In the second case it would have weight56,68,72,76,80, below minimum128.
Thus no target is obtained.

If n has a nonzero component on E's free F_2^3 factor, both halves normalize
to B x F_2^2 in a9-space. Their d-flat maxima are at most
1,2,4,8,16,32,48,64. Since U_2 is disjoint from each leaf direction,
the dimensions of the two intersections with the9-space sum to at most9.
Thus e2+e3<=68 and e1<=64, so total <=132, too small.

It remains that n is nonzero only on B. Each half has hull contained in a9-space
V parallel to ker(n|C). For each center/leaf pair, its direction intersections
with V are disjoint and their dimensions sum to at most9.
If all ei<=64, the product maxima above give e2+ei<=72 for each leaf,
so e1+e2+e3<=144. If e2>64, the center's direction contains the full free3-space
and projects to a base4-space; each leaf's direction intersection with V projects
injectively and disjointly from this4-space in a6-space, so each leaf count<=4.
Then total<=104. Otherwise some **leaf** has count80 or96. The identical argument
bounds center e2<=4.

agent3_E256_threeflat382_discretechecks.py exhausts all actual other-leaf counts
from the complete product spectra, both choices of high-leaf side, e2=0..4,
and delta=0..min(e2,1). No possibilities remain for322,326,330,334.
There are90 possible numerical tuples for310 across the three B presentations:
all require center e2=4, delta=0. In84 tuples the other leaf meets V in dimension7.
The center meets V in dimension2 (it must be exactly2 by dimension and the high-leaf
constraint), so the center and other-leaf intersections have complementary directions
in V and necessarily meet at a point in V. Since all four center points belong to E,
this point is in E, forcing delta=1, contradiction.

In the remaining6 tuples the other leaf intersection has dimension6 and count64,
and the entire opposite base half is an affine3-flat of size8 (explicitly checked).
Thus the other-leaf intersection is the **entire** affine6-flat E-half. All center
intersection points belong to this same affine6-flat. Their affine2-flat direction
therefore meets the other-leaf direction, contradicting U_2 intersect U_3=0.

This proves the stated constructor obstruction. It supplies no missing low weight
and no absence result in dimension14.
''')
# Append independently rerunnable final assertions to the discrete checker.
f=pathlib.Path('workspace/agent3_E256_threeflat382_discretechecks.py')
s=f.read_text()
s+='''\n# Final geometric-residual numerical checks.\nfor obj,dat in zip(raw,res):\n for t in dat['candidates']:\n  assert list(t[5:8])==[4,0,310]\n  if t[3]==6:\n   h,ep=t[:2];half=[v for v in obj['base'] if (v&h).bit_count()%2==1-ep]\n   assert len(half)==8\n   D={v^half[0] for v in half}\n   assert all(a^b in D for a in D for b in D)\n  else:assert t[3]==7\nprint('All90residual310tuplesgeometricallyexcluded')\n'''
f.write_text(s)
print('Saved',p)
