# A checked relative-collision gap for the exceptional weight-256 supports

For each of the three explicit 32-point sets B in the data file
`agent3_T280_P12_allorbits.json`, let S=B×F_2^3 in F_2^10.
The standalone checker `agent3_T280_P12_allorbits.py` embeds all three B
as numerical constants. It uses only exact binary integer elimination;
there is no SAT timeout or probabilistic claim.

## Claim
If P is disjoint from S, 0<|P|<16, and
sum_{p∈P} ν_5(p) belongs to span{ν_5(s):s∈S}, then
P={b}×F_2^3 for one of the 16 points b in cl_2(B)\B.
In particular no such P has size 12.

Here ν_d contains all squarefree monomials of degree at most d,
including the constant. The following proof works separately for all
three numerical B; affine equivalence between them is not assumed.

## Separator reduction
If p∉cl_2(S), choose a polynomial L of degree≤2 zero on S but L(p)=1.
For a hypothetical relation supported on S∪P, multiplying by L and
all monomials of degree≤3 shows P∩{L=1} is 3-even. A nonempty 3-even
point set has size at least 16 by the usual Reed–Muller minimum-distance
induction. Thus |P|<16 implies P⊂cl_2(S)\S.

The degree-two product closure is
cl_2(B×F_2^3)=cl_2(B)×F_2^3:
base polynomials separate any base point outside cl_2(B), while a
point whose base belongs to cl_2(B) satisfies every quadratic relation
on the product by expanding that polynomial in the free coordinates.
Therefore P⊂E×F_2^3, E=cl_2(B)\B, |E|=16.

## Exact base computations
For d=3,4,5 define
R_d={a∈F_2^E : sum_e a_e ν_d(e)∈span ν_d(B)}.
The checker computes cl_2(B) at all 128 points, obtains E, reduces
all 16 outside columns by the ENTIRE Gaussian basis (canonical
remainder, not an early-return membership reducer), computes a kernel,
and enumerates its full 2^dim code. For EACH of the three B it finds:

* R_5 has dimension zero.
* R_4 has dimension one, consisting of 0 and the all-one length-16 word.
* R_3 has dimension seven and weight enumerator
  1+8z^4+16z^6+78z^8+16z^10+8z^12+z^16.

Only 128 words need enumeration in the largest of these codes. Bases,
point lists and complete histograms are saved in the JSON certificate.

## Fibre argument
Write P_e={u:(e,u)∈P}. For each free-coordinate monomial u_J,
the vector M_J(e)=sum_{u∈P_e}u_J belongs to R_{5−|J|}.
Indeed, take any degree-(5−|J|) base monomial in the original ν_5
relation. The unknown contribution supported on B supplies exactly
the linear combination of ν_{5−|J|}(B) required in this assertion.

For J empty, R_5=0 implies every fibre is even. Therefore any first
moment vector M_{j} has support≤|P|/2≤7. Since R_4 has nonzero
weight 16, all three first moments vanish. Each fibre is now 1-even,
so every nonempty fibre has at least four points. Every second-moment
vector M_{jk} consequently has support≤|P|/4≤3. The minimum weight
of R_3 is four, so these moments also vanish. Each fibre is 2-even
inside F_2^3. The only such subsets are empty and the entire cube:
this follows either from minimum distance eight or from the checker,
which also exhausts all 256 subsets and confirms it directly.

Thus P is a union of full eight-point fibres. Under 0<|P|<16 it is
exactly one fibre, as claimed. Conversely each of the 16 fibres is
valid: its ν_5 relation reduces to the degree-two base closure relation.

This proves only the stated relative-collision theorem. The reduction
of arbitrary weight-280 Reed–Muller words to this exceptional branch,
and all other branches, belongs to the separate team classification.
It is NOT a proof of the requested no-fixed-list assertion.
