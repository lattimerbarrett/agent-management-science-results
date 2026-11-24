import sympy as s
from pathlib import Path
import json
h,H,B,C,c,z,b,d=s.symbols('h H B C c z b d')
R=s.groebner([H**2-h*H+h**2,h**3],H,h,domain=s.QQ.frac_field(B,C,c,z,b,d))
def red(poly): return s.expand(R.reduce(s.expand(poly))[1])
# Three distinct consecutive line degrees 0,-1,-2.
roots=[B*H,-h+C*H,-2*h-(B+C)*H]
c2=red(sum(roots[i]*roots[j] for i in range(3) for j in range(i+1,3)))
c3=red(s.prod(roots))
q=B**2+B*C+C**2+2*B+C
assert s.expand(c2-((B**2+B*C+C**2+2)*h**2-q*h*H))==0
assert s.expand(c3-B*(B-C+2)*h**2*H)==0
# Exhaustive symbolic solution: c3 gives B=0 or C=B+2.
assert s.factor(q.subs(B,0))==C*(C+1)
assert s.expand(q.subs(C,B+2)-3*(B+1)*(B+2))==0
solutions=s.solve([q,B*(B-C+2)],[B,C])
assert set(solutions)=={(0,0),(0,-1),(-1,1),(-2,0)}
# In the unique nondecomposable case, the second fundamental map to
# the last graded line has negative q-fiber degree; the map to the middle
# graded line takes values in the trivial line bundle.
omega_p=h-2*H
sf_last=s.expand(roots[2]+omega_p-roots[0])
sf_middle=s.expand(roots[1]+omega_p-roots[0])
assert sf_last.coeff(h)==-1
assert sf_middle.subs({B:-2,C:0})==0
# Repeated case: type (0,-1,-1), line O(bH), rank2 quotient
# q*W tensor O(-h), where c1(W)=-bH, c2(W)=zH^2.
line=b*H
quot_c1=-2*h-b*H
quot_c2=h*h+b*h*H+z*H*H
rep_c2=red(quot_c2+line*quot_c1)
rep_c3=red(line*quot_c2)
assert s.expand(rep_c2-((1-z+b*b)*h*h+(z-b-b*b)*h*H))==0
assert s.expand(rep_c3-b*(b+1)*h*h*H)==0
assert s.solve(b*(b+1),b)==[-1,0]
assert (b*b+b).subs(b,-1)==0
# Symmetric square of rank2 normalized tangent dual: roots alpha,beta
# produce 2alpha, alpha+beta, 2beta, so c1=-3 and c2=6.
a1,a2=s.symbols('alpha beta')
sym2roots=[2*a1,a1+a2,2*a2]
sym2c1=s.expand(sum(sym2roots))
sym2c2=s.symmetrize(sum(sym2roots[i]*sym2roots[j] for i in range(3) for j in range(i+1,3)),[a1,a2],formal=True)
assert s.expand(sym2c1-3*(a1+a2))==0
assert s.expand(sum(sym2roots[i]*sym2roots[j] for i in range(3) for j in range(i+1,3))-(2*(a1+a2)**2+4*a1*a2))==0
results={'distinct_c2':str(c2),'distinct_c3':str(s.factor(c3)),'distinct_solutions':[list(map(str,x)) for x in solutions],'repeated_c2':str(rep_c2),'repeated_c3':str(s.factor(rep_c3)),'SF_middle':str(sf_middle),'SF_last':str(sf_last)}
Path('workspace').mkdir(exist_ok=True)
Path('workspace/agent2_rank3_checks.json').write_text(json.dumps(results,indent=2))
source=Path(__file__); target=Path('workspace/agent2_rank3_checks.py')
if source.resolve()!=target.resolve(): target.write_text(source.read_text())
print(json.dumps(results,indent=2))
proof=r'''# Uniform bundles of rank at most three on P^2

All varieties are complex. Write X={(x,L): x in L} with p:X->P^2 and q:X->(P^2)^dual. Put h=p*c1(O(1)), H=q*c1(O(1)). Then Pic(X)=Zh+ZH,
A*(X)=Z[h,H]/(h^3,H^2-hH+h^2), and Omega^1_{X/P^2}=O(h-2H).
For any uniform bundle E, relative evaluation constructs its q-relative splitting filtration; each graded piece of q-fiber degree a is q*V tensor O(ah), with V a bundle on the dual plane. The construction follows from cohomology/base change, taking the top degree first.

## Descent and the gap argument
The second fundamental form of a subbundle F of p*E along p takes values in Hom(F,p*E/F) tensor Omega_p. If the corresponding consecutive splitting degrees have a gap at least two, its restriction to every q-fiber is a sum of negative line bundles, so it vanishes. Consequently, the Grassmannian map on each p-fiber has derivative zero. In characteristic zero it is constant. Thus F descends to a subbundle A of E, and the quotient B is a uniform bundle with the remaining splitting degrees.

A bundle trivial on every line is trivial: blow up a point, use the P^1 bundle structure of the blowup over P^1, and cohomology/base change. Its pullback is pulled back from P^1; restriction to the exceptional section, where the original blowdown is constant, shows that bundle is trivial. Push down.

## Rank two
Twist the splitting type to (0,-d), d>=0. If d=0 use the preceding lemma. Otherwise the top relative subline is O(bH) and the quotient is O(-dh-bH). Chern comparison gives c2(E)=b^2 and b(b+d)=0. If b=0, descent gives O as subbundle and E splits by H^1(O(d))=0. If b=-d, the second fundamental form is a section of O((d-1)(-h+2H)). When d>1 it vanishes by restriction to q-fibers, forcing descent, impossible since O(-dH) restricts to O(-d) on each p-fiber. Thus d=1. Dualizing yields
0 -> O(h-H) -> p*E^dual -> O(H) -> 0.
All p-fiber cohomology of O(h-H) vanishes. Since p_*O(H)=Q=T(-1), pushing down identifies E^dual=Q, E=Omega^1(1). This proves the rank-two classification, including all twists.

## Rank three: eliminating gaps
If a gap exists, descend as above. Both pieces have rank at most two and are classified. An extension of line bundles splits since H^1(O(k))=0. The other possibilities are one line and a twist Omega^1(t). If the line is the upper block O(a), the lower block is Omega^1(b+1), of splitting type (b,b-1), with a>b. The extension space is H^1(T(a-b-1))=0. If the line is the lower block O(c), the upper block is Omega^1(a+1), with c<a-1. The extension space is H^1(Omega^1(a+1-c))=0. These vanishings follow immediately from the Euler sequences (all twists here are positive). Thus any splitting gap gives a decomposable, hence homogeneous bundle.

The remaining normalized types are (0,0,0), (0,-1,-1), (0,0,-1), and (0,-1,-2). The first is trivial; the third is the dual/twist of the second.

## Type (0,-1,-1)
The relative filtration is
0 -> O(bH) -> p*E -> q*W tensor O(-h) -> 0,
where rank(W)=2, c1(W)=-b and c2(W)=z. Chern comparison yields z=b^2+b and b(b+1)=0. If b=0, restriction to p-fibers shows W is trivial on every line of the dual plane; hence W is trivial. Pushing down gives an extension of O(-1)^2 by O, which splits.
If b=-1, restriction to p-fibers gives the Euler-type quotient O^3/O(-1), so W restricts to O(1) plus O on every dual line. Its Chern classes are c1=1,c2=0. The rank-two classification forces W=O(1) plus O. Push the displayed sequence along p. O(-H) has zero cohomology on p-fibers, so
E = (p_*O(H) tensor O(-1)) plus O(-1)
  = T(-2) plus O(-1) = Omega^1(1) plus O(-1).
Thus this type, and its dual/twist, is homogeneous.

## Type (0,-1,-2)
The three relative line factors have classes
BH, -h+CH, -2h-(B+C)H.
Since c2(E) is a multiple of h^2 and c3(E)=0, comparison gives
B^2+BC+C^2+2B+C=0,   B(B-C+2)=0.
The solutions are (B,C)=(0,0),(0,-1),(-1,1),(-2,0): indeed B=0 gives C(C+1)=0, and C=B+2 gives 3(B+1)(B+2)=0.

In the first two cases, the top O descends; the rank-two quotient has type (-1,-2). It is split or Omega^1. The relevant Ext groups vanish by the Euler sequence, so E is decomposable. In the third case the bottom quotient O(-2h) descends. The kernel is rank two of type (0,-1), and the extension again splits since H^1(Omega^1(3))=0 (or by line-bundle cohomology if the kernel splits).

For (B,C)=(-2,0), write F1 subset F2 subset p*E for the filtration. Here
F1=O(-2H), F2/F1=O(-h), p*E/F2=O(-2h+2H).
The second fundamental form F1 -> (p*E/F1) tensor Omega_p has zero composition to (p*E/F2) tensor Omega_p: the corresponding Hom line has q-fiber degree -1. Hence it factors through (F2/F1) tensor Omega_p. The latter Hom line is O_X. The section is nonzero, since otherwise F1 would descend, contradicting its degree -2 on p-fibers. Thus it is nowhere zero.
On every p-fiber this says the degree-two morphism P^1 -> P(E_x) defined by F1 is unramified. Its image cannot be a line, since a degree-two map P^1 -> P^1 ramifies. Thus its three defining sections of O(2) are linearly independent. The adjunction map
E^dual -> p_*O(2H) = Sym^2 Q
is therefore an isomorphism at every point. We obtain E=Sym^2(Omega^1(1)), which is homogeneous.

We have proved: every uniform rank-three bundle on P^2 is split, a direct sum Omega^1(t) plus O(s), or a twist of Sym^2 Omega^1. Together with ranks one and two, this proves the problem's assertion for n=2. The exact Chern identities and all polynomial solution steps are checked by agent2_rank2_checks.py and agent2_rank3_checks.py. General dimensions in ranks n<=r<2n are not proved here.
'''
Path('workspace/agent2_P2_proof.md').write_text(proof)
