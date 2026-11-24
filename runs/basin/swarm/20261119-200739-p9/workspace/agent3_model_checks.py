import numpy as np
from pathlib import Path
code=r'''import numpy as np

def hp(A,r):
    lam,U=np.linalg.eigh(A)
    return (U*lam**r)@U.conj().T

def verify(seed=9347):
    rng=np.random.default_rng(seed)
    err_pair=err_vector=0.
    for p in [1.2,1.5,1.9,2.,2.5,3.,5.,10.]:
        for _ in range(50):
            mats=[]
            for k in range(2):
                A=rng.normal(size=(2,2))+1j*rng.normal(size=(2,2))
                A+=2*np.eye(2)
                mats.append(A)
            M,N=mats
            # W=(M* M)^(p/2); W^(1/p)=(M* M)^(1/2).
            W=hp(M.conj().T@M,p/2)
            V=hp(N.conj().T@N,p/2)
            lhs=np.linalg.norm(hp(W,1/p)@hp(V,-1/p),2)
            rhs=np.linalg.norm(M@np.linalg.inv(N),2)
            err_pair=max(err_pair,abs(lhs-rhs)/rhs)
            z=rng.normal(size=2)+1j*rng.normal(size=2)
            lhs=np.linalg.norm(hp(W,1/p)@z)
            rhs=np.linalg.norm(M@z)
            err_vector=max(err_vector,abs(lhs-rhs)/rhs)
    # Finite matrix operators verify triangular conjugation exactly numerically.
    n=7
    a=np.exp(rng.normal(size=n)); d=np.exp(rng.normal(size=n)); b=rng.normal(size=n)
    A=np.diag(a); D=np.diag(d); B=np.diag(b)
    I=np.eye(n); O=np.zeros((n,n))
    M=np.block([[A,A@B],[O,D]])
    H=rng.normal(size=(n,n))
    HH=np.block([[H,O],[O,H]])
    expected=np.block([[A@H@np.linalg.inv(A), A@(B@H-H@B)@np.linalg.inv(D)], [O,D@H@np.linalg.inv(D)]])
    err_tri=np.linalg.norm(M@HH@np.linalg.inv(M)-expected)
    assert err_pair<2e-4,err_pair
    assert err_vector<2e-4,err_vector
    assert err_tri<1e-10,err_tri
    return err_pair,err_vector,err_tri

if __name__=='__main__':
    print('max relative pair / vector errors and absolute triangular error:',verify())
'''
Path('workspace/agent3_polar_checks.py').write_text(code)
exec(compile(code,'workspace/agent3_polar_checks.py','exec'))
import sympy as s
D,Q,eps=s.symbols('D Q eps', positive=True)
k=s.Rational(3,8)-eps**2/2
r=2*eps**2-1
B=Q**(s.Rational(3,2)-2*eps**2)/(2*k*r)
F=1/k-B+B*D**r-s.sqrt(D)/k
L=lambda f:s.Rational(1,2)*D**2*s.diff(f,D,2)+(1-eps**2)*D*s.diff(f,D)
assert s.simplify(L(F)+s.sqrt(D))==0
assert s.simplify(F.subs(D,1))==0
assert s.simplify(s.diff(F,D).subs(D,Q))==0
print('Reflected diffusion occupancy ODE / absorbing / Neumann conditions: checked exactly')
Path('workspace/agent3_occupancy_formula.txt').write_text(str(F))
from scipy.optimize import differential_evolution

def ratio(params,p,ret=False):
    sig,z=params; kap=sig/2; q=p/(p-1); m=sig-sig**2/2-z
    def root(beta,v):
        mu=m+beta*sig; disc=mu*mu-2*sig*sig*v
        if disc<0 or (v>0 and mu>=0): return None
        return (-mu-np.sqrt(disc))/(sig*sig)
    ra=root(-q,q*(q-1)/2)
    rc=root(q*(kap-1),q*(q-1)*(kap-1)**2/2)
    if ra is None or rc is None:return 1e3
    nu=2/sig-.5-2*z/sig**2
    C=max((p-1)*ra,p/2+(p-1)*rc)
    value=nu/C
    if ret:return value,nu,C,ra,rc
    return -value
def ratio2(params,p,ret=False):
    sig,kap,z=params; q=p/(p-1); m=sig-sig**2/2-z
    def root(beta,v):
        mu=m+beta*sig; disc=mu*mu-2*sig*sig*v
        if disc<0 or (v>0 and mu>=0): return None
        return (-mu-np.sqrt(disc))/(sig*sig)
    ra=root(-q,q*(q-1)/2)
    rc=root(q*(kap-1),q*(q-1)*(kap-1)**2/2)
    chi=sig**2*(p-2)/4+sig-z-p*kap*sig+(p+1)*kap**2-2*kap
    if ra is None or rc is None or chi>=0:return 1e3
    nu=2/sig-.5-2*z/sig**2
    C=max((p-1)*ra,p/2+(p-1)*rc)
    value=nu/C
    if ret:return value,nu,C,ra,rc,chi
    return -value
pp=s.symbols('p',positive=True)
qq=pp/(pp-1);kap=1/pp;alp=1/(pp*(pp-1))
lam=alp*qq*(kap-s.Rational(1,2))-qq*kap**2/2+qq**2*(alp-kap)**2/2
print('dual angular exponential drift:',s.factor(lam))
note=r'''# Obstruction for the asymmetric canonical-pair model

Let p>2, q=p/(p-1), and let a,c be positive terminal random variables with E_P a=1. Set dmu=a dP, R=c/a, and let

M=[[a^(1/p), a^(1/p) h],[0,a^(1/p)/c]].

Direct triangular inversion shows the off-diagonal entry of M(x)M(y)^(-1) equals a(x)^(1/p)c(y)a(y)^(-1/p)(h(x)-h(y)). Consequently the characteristic is at least

C=E_mu,x (E_mu,y R(y)^q |h(x)-h(y)|^q)^(p/q).

Suppose E_mu[R^q h]=0, e.g. the stopping rule depends only on B1, R depends only on B1, and h is a centered Gaussian conditional on B1 (driven by an independent B2).
Writing Z=E_mu R^q, weighted Jensen gives
E_mu,y R(y)^q |h(x)-h(y)|^q >= Z |h(x)|^q.
Therefore

C >= Z^(p/q) E_mu |h|^p.

Thus the dual-ratio penalty and primal angular moment multiply in the actual characteristic. They cannot be removed merely by improving a triangle-inequality estimate.

Gaussian centering is not essential. For general h with E_mu h=0, write b=E_mu[R^q h]/Z. Weighted Jensen yields C>=Z^(p/q) E_mu|h-b|^p. Since |b|<=||h-b||_p and ||h||_p<=2||h-b||_p, one has the universal bound C>=2^(-p) Z^(p/q) E_mu|h|^p. Thus common-noise correlation cannot erase this product cost in a closed canonical martingale pair.

A further Ito obstruction: for scalar stretch noises da=a sa dB1, dc=c sc dB1 and dh=u dB1+v dB2+b dt, requiring both ah and ch to be martingales forces b=-sa u=-sc u. Hence when sa!=sc one must have u=b=0. In higher noise dimension the necessary condition is (sa-sc).eta=0 and drift_h=-sa.eta.
'''
Path('workspace/agent3_canonical_obstruction.md').write_text(note)
rng=np.random.default_rng(848)
for pp in [2.1,2.5,3.,4.,8.]:
    qq=pp/(pp-1)
    for _ in range(100):
        # Each R atom has an independent symmetric +/- h pair, so weighted mean vanishes exactly.
        RR=np.repeat(np.exp(rng.normal(size=6)),2)
        HH=np.column_stack([np.exp(rng.normal(size=6)),-np.exp(rng.normal(size=6))])
        hh=np.repeat(np.exp(rng.normal(size=6)),2)*np.tile([1.,-1.],6)
        mu=np.repeat(rng.dirichlet(np.ones(6))/2,2)
        inner=np.sum(mu[None,:]*RR[None,:]**qq*abs(hh[:,None]-hh[None,:])**qq,axis=1)
        C=np.dot(mu,inner**(pp/qq))
        lower=np.dot(mu,RR**qq)**(pp/qq)*np.dot(mu,abs(hh)**pp)
        assert C>=lower*(1-1e-12)
print('500 genuinely evaluated atomic canonical no-cancellation inequalities: passed')
for pp in [2.1,2.5,3.,4.,8.]:
    qq=pp/(pp-1)
    for _ in range(100):
        mu=rng.dirichlet(np.ones(9))
        RR=np.exp(rng.normal(size=9))
        hh=rng.normal(size=9); hh-=np.dot(mu,hh)
        inner=np.sum(mu[None,:]*RR[None,:]**qq*abs(hh[:,None]-hh[None,:])**qq,axis=1)
        C=np.dot(mu,inner**(pp/qq))
        lower=2**(-pp)*np.dot(mu,RR**qq)**(pp/qq)*np.dot(mu,abs(hh)**pp)
        assert C>=lower*(1-1e-12)
print('500 arbitrary-correlated mean-zero atomic canonical inequalities: passed')
finite_note=r'''# Finite-valued root lemma

Suppose M:R->GL(2,C) takes exactly K essential values M_1,...,M_K. Let A be its matrix A_p characteristic (equivalently use W=(M* M)^(p/2)). Then

||M H M^(-1)||_(Lp->Lp) <= C_p K^2 (2K)^(K-1) A^((K-1)/p).

Proof. Put an undirected edge ij when some interval I has both proportions |I cap E_i|/|I| and |I cap E_j|/|I| at least 1/(2K). This graph is connected: for any nontrivial cut of the colors, the union E of one side and its complement both have density points. Translate a sufficiently short interval between two such points. Its E-density is continuous in the translation parameter and crosses 1/2. At that interval some color from each side has proportion >=1/(2K).

For an edge ij, the characteristic on its witnessing interval is at least alpha_i alpha_j^(p-1) ||M_i M_j^(-1)||^p. Thus both directed matrix norms on this edge are <=2K A^(1/p). A path of length <=K-1 and submultiplicativity yield the same pair bound with exponent K-1 for arbitrary i,j (A>=1).

Finally M H M^(-1)=sum_(i,j) M_i M_j^(-1) 1_(E_i) H 1_(E_j). Multiplication by an indicator is contractive on unweighted Lp and the componentwise Hilbert transform is bounded there with a p-dependent constant. Sum the K^2 bounds.

Consequences: K=2 gives exponent1/p; K=3 gives exponent2/p, hence linear for p=2. No three-fixed-root-value construction can yield the sharp A2 exponent3/2. The lemma does NOT cover finitely many eigenvector directions with continuously varying eigenvalues.
'''
Path('workspace/agent3_finite_state.md').write_text(finite_note)
for K in [2,3,4,6]:
    for pp in [1.5,2.,3.,5.]:
        qq=pp/(pp-1)
        mats=[rng.normal(size=(2,2))+2*np.eye(2) for _ in range(K)]
        pair=np.array([[np.linalg.norm(mats[i]@np.linalg.inv(mats[j]),2) for j in range(K)] for i in range(K)])
        # All consecutive color boundaries admit intervals containing exactly equal portions.
        A=1.
        for j in range(K-1):
            inds=[j,j+1]
            F=pair[np.ix_(inds,inds)]
            A=max(A,np.mean(np.mean(F**qq,axis=1)**(pp-1)))
        bound=(2*K*A**(1/pp))**(K-1)
        assert np.max(pair)<=bound*(1+1e-12)
print('finite-state adjacency/pair bounds: 16 computed cases passed')
Path('workspace/agent3_model_checks.py').write_text(Path('scratchpad.py').read_text())
