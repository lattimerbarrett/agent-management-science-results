import numpy as np
import sympy as sp
from pathlib import Path

p=sp.symbols('p', positive=True)
q=p/(p-1)
a=lambda t: 1+1/(t*(t-1))
assert sp.simplify(a(q)/(p-1)-a(p))==0
assert sp.simplify(a(p)-(1+1/(p-1)-1/p))==0

def power(A,t):
    vals, vecs=np.linalg.eigh(A)
    assert np.min(vals)>0
    return (vecs*vals**t)@vecs.conj().T

def characteristic_root(As, prob, p):
    # As = W^(1/p). Atomic exact version of the question's double integral.
    q=p/(p-1)
    inverses=[np.linalg.inv(A) for A in As]
    return sum(prob[i]*sum(prob[j]*np.linalg.norm(A@B,2)**q
        for j,B in enumerate(inverses))**(p/q)
        for i,A in enumerate(As))**(1/p)

rng=np.random.default_rng(17429)
rows=[]
for p0 in [1.2,1.5,1.9,2.,2.5,3.,5.,10.]:
    ratios=[]
    for trial in range(50):
        As=[]
        for k in range(6):
            U,_=np.linalg.qr(rng.normal(size=(2,2))+1j*rng.normal(size=(2,2)))
            As.append((U*np.exp(rng.uniform(-2,2,2)))@U.conj().T)
        prob=rng.dirichlet(np.ones(6))
        F=characteristic_root(As,prob,p0)
        G=characteristic_root([np.linalg.inv(A) for A in As],prob,p0/(p0-1))
        ratios.append(G/F)
        assert 1/32 <= G/F <= 32
    rows.append((p0,min(ratios),max(ratios)))

# Scalar matrices must give exact duality, not just comparability.
for p0 in [1.2,1.5,2.,3.,5.]:
    As=[np.eye(2)*z for z in [0.1,0.7,1.,3.,10.]]
    prob=np.array([.1,.15,.3,.25,.2])
    F=characteristic_root(As,prob,p0)
    G=characteristic_root([np.linalg.inv(A) for A in As],prob,p0/(p0-1))
    assert np.isclose(F,G,rtol=1e-11)
print('Symbolic exponent and duality checks passed.')
assert sp.simplify(a(q)-(p-1)*a(p))==0
print('p, min dual/primal root, max dual/primal root (50 random tests)')
for row in rows: print(row)
Path('workspace').mkdir(exist_ok=True)
Path('workspace/agent4_duality_checks.py').write_text(Path(__file__).read_text())
Path('workspace/agent4_duality.md').write_text(r'''# Dual characteristic and norm lemma (complete)

Let p>1, q=p/(p-1), A=W^(1/p), and V=W^(-1/(p-1)).
For a fixed interval I normalize Lebesgue measure to probability. Put
F=(E_x (E_y ||A(x)A(y)^(-1)||^q)^(p/q))^(1/p).
Define G by replacing A by A^(-1) and p by q. Then

    F/32 <= G <= 32 F.

Consequently [V]_{A_q}^{1/q} is within a factor 32 of
[W]_{A_p}^{1/p}. Constants are deliberately nonoptimal.

Proof. Finite F and a suitable fixed x imply E||A^(-1)||^q<infinity;
E||A||^p<infinity follows from local integrability of W. Thus
n_+(v)=(E|Av|^p)^(1/p), n_-(v)=(E|A^(-1)v|^q)^(1/q)
are genuine finite-dimensional complex norms.
For any complex norm n on C^2, choose a pair u_1,u_2 in its closed
unit ball maximizing |det(u_1,u_2)|. The maximum exists, is positive,
and both vectors have norm one. If v=a_1u_1+a_2u_2 has n(v)<=1,
replacing u_j by v and using determinant maximality proves |a_j|<=1.
Thus for general v, max|a_j|<=n(v)<=|a_1|+|a_2|.
Let R be the positive definite matrix with |Rv|^2=|a_1|^2+|a_2|^2.
We obtain |Rv|/sqrt(2)<=n(v)<=sqrt(2)|Rv|.
Choose B,C as such reducing matrices for n_+,n_- respectively.

The following elementary observation is used twice. If
n(v)=(E|M v|^r)^(1/r) is reduced by R as above, and T is fixed, then

  (1/2)||RT|| <= (E||MT||^r)^(1/r) <= 2sqrt(2)||RT||.

Indeed the middle quantity is >=max_j n(Te_j), giving the lower bound,
and is <=n(Te_1)+n(Te_2) by Minkowski, giving the upper bound.
Apply this first with M=A(y)^(-1), T=A(x), r=q, and use that
||A(x)A(y)^(-1)||=||A(y)^(-1)A(x)|| (adjoints).
The inner norm is between ||CA(x)||/2 and 2sqrt(2)||CA(x)||.
Since ||CA(x)||=||A(x)C||, apply the observation a second time with
M=A(x), T=C, r=p. It follows that

  ||BC||/4 <= F <= 8||BC||.

For G exchange A with A^(-1), B with C, and p with q; obtain
||CB||/4 <= G <= 8||CB||. Since B,C are Hermitian,
||BC||=||(BC)^*||=||CB||. This proves the claimed factor 32.
Taking suprema over intervals proves the characteristic statement.

The Banach dual of L^p(W), under the unweighted integral pairing, is
L^q(V): this follows isometrically by conjugation with A, because
V^(1/q)=A^(-1). Smooth compactly supported functions are dense (truncate,
then use regularity of the finite measures defined by the locally
integrable matrix entries). H is skew-adjoint on smooth test functions.
Therefore its bounded extension on the two dual weighted spaces has
the same operator norm. Combining this with characteristic comparability
in both directions gives the exact relation between optimal powers:

    beta(q)=(p-1) beta(p).

This duality statement does not determine beta(p) from beta(2).
''')
