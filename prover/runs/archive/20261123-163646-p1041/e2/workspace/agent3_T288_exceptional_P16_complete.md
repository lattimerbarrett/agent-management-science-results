# Complete exceptional-256/P16 branch of the weight-288 classification

Let S=B32×F2^3⊂F2^10 be one of the three exceptional terminal
weight-256 supports. The explicit base constants and relative-code
certificates are in `agent3_T280_P12_allorbits.py/.json`. This note
classifies all outside sets P of size sixteen with ν5(P) in spanν5(S),
and checks stable degree-four closure of every resulting 288 lift.

All changes of coordinates below are affine. Such transformations
preserve code membership, polynomial degree, closure, and the kernel
inner-product properties in the conclusion.

## Part I: P contained in the degree-two closure

Write E=cl2(B32)\B32, |E|=16. The exact relative base codes R5,R4,R3,R2
have dimensions 0,1,7,16; R4={0,all16}; R3 has minimum four and exactly
eight words of weight four. These complete enumerators were checked
separately for all three bases.

For P⊂E×F2^3 of weight sixteen, fibre parity is in R5 and hence zero.
First-free-coordinate moments have support≤8 and belong to R4, hence
zero. Thus each nonempty fibre is a 1-even subset of F2^3, of weight
four or eight; a four-point fibre is an affine plane. The possible
partitions of sixteen are 8+8, 8+4+4, or 4+4+4+4.

The 8+4+4 case is impossible: the two four-point planes have nonzero
second-moment vectors, so some second moment would be a nonzero R3
word supported on only one or two base points. The minimum is four.
In the four-plane case every second-moment support has either zero
or all four points. Thus the four planes have a common normal, and
the four base points form one of the eight weight-four R3 supports.
The third free moment is unrestricted because R2=F2^16.

Consequently the complete candidate list is:
* any two full eight-point fibres: C(16,2)=120;
* one of eight R3 supports, a common nonzero normal (seven choices),
  and four independently chosen offsets (sixteen choices): 896.
Total 1016 per base, 3048 over all three. The exact checker
`agent3_T288_E256_P16_contained.py` builds every candidate, solves its
actual ν5 relation, constructs the full 288 support, verifies ν6 sum
zero, and computes BOTH full kernels K4 and K5.

## Part II: P not contained in the degree-two closure

Choose a polynomial L of degree≤2 zero on S but nonzero somewhere
on P. The original relation multiplied by L and every degree≤3
monomial shows P∩{L=1} is a nonempty 3-even subset. Such a set has
size at least sixteen, so it equals ALL of P and is a minimum word:
P is an affine 4-flat. This is the boundary exception that would be
missed by incorrectly using a strict separator inequality at equality.

Project P to the seven base coordinates. Its image Q is an affine
d-flat with d∈{1,2,3,4}; its free-direction kernel has dimension 4−d.
The product automorphisms u→Au+Mx+b preserve S. Choose A to straighten
the kernel, then extend the graph map Q→F2^3/kernel to an affine map
on the base, and use M,b to kill that graph. Thus every P is equivalent
to Q×F2^(4−d), with the remaining free coordinates zero. It is disjoint
from S exactly when Q∩B32 is empty. The ν5 relation becomes exactly
  ν_(d+1)(Q)∈span ν_(d+1)(B32).

`agent3_T288_E256_P16_affflats.py` enumerates ALL affine d-flats in
F2^7 by unique RREF direction basis plus canonical coset representative.
For EACH of the three bases it checks:
  d1: 8128 flats, 304 valid;
  d2: 85344 flats, zero valid;
  d3: 188976 flats, zero valid;
  d4: 94488 flats, zero valid.
The total is 376936 actual checks per base. It constructs all 912
valid lifts and again checks ν6 sum zero and both complete kernels.
Some flat cases overlap Part I; harmless redundancy is retained.

## Stable closure certificate for all lifts

All supports constructed in both parts have weight 288, affine rank
at most eleven, and a quartic indicator, hence are degree-four closed.
For every one the exact checker finds K4 orthogonal to K5. The
contained-closure histogram is:
  2904 cases: dimK4=57, dimK5=12;
  144 cases:  dimK4=60, dimK5=13.
The affine-flat histogram is:
  768 cases: dimK4=57, dimK5=12;
  144 cases: dimK4=60, dimK5=13.
All cross-inner-products are zero, with no exceptions.

Choosing one ν5 solution for each P loses no affine-equivalence class:
two solutions differ by a K5(S) word, and S is terminal with K5(S)
exactly its affine evaluation space. An affine shear of the new graph
coordinate realizes this difference, while preserving double fibres P.

Finally, if T is degree-four closed and K4(T)⊥K5(T), every graph lift
with a legal label ℓ∈K5(T) is still degree-four closed. A putative new
closure point cannot project outside T; an opposite point above s∈T
would require a k∈K4(T) with k·ℓ=1, impossible. The new K4 and K5
identify with subspaces of the old respective kernels, so their mutual
orthogonality persists. Induction covers every iterated graph lift.

Therefore the ENTIRE exceptional-256/P16 branch is stably degree-four
closed. The quadratic-graph-256/P16 branch is separate and is not
claimed resolved in this note. No main no-fixed-list theorem is claimed.
