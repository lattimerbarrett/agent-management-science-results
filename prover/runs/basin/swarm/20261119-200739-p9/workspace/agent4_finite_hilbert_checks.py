from pathlib import Path
import numpy as np
from scipy.integrate import quad

for d in range(1,21):
    xlog=lambda x: 0. if x==0 else x*np.log(x)
    exact=(xlog(d+1)-2*xlog(d)+xlog(d-1))/np.pi
    a=quad(lambda t:(t-d+1)/t if t else 1., d-1,d,epsabs=1e-12)[0]
    b=quad(lambda t:(d+1-t)/t,d,d+1,epsabs=1e-12)[0]
    assert abs(exact-(a+b)/np.pi)<1e-12

def root(A,t):
    w,U=np.linalg.eigh(A)
    return (U*w**t)@U.T

def cp(Ws,weights,p):
    q=p/(p-1)
    A=[root(W,1/p) for W in Ws]
    inv=[np.linalg.inv(B) for B in A]
    K=np.array([[np.linalg.norm(X@Y,2)**q for Y in inv] for X in A])
    return np.dot(weights,(K@weights)**(p-1))

def probs_interval(a,b,N):
    out=np.zeros(N)
    for k in range(int(np.floor(a)),int(np.ceil(b))):
        out[k%N]+=max(0.,min(b,k+1)-max(a,k))
    return out/(b-a)

rng=np.random.default_rng(84117)
maxscaled=0.
for trial in range(30):
    N=5
    Ws=[]
    for k in range(N):
        t=rng.uniform(0,6.28); Q=np.array([[np.cos(t),-np.sin(t)],[np.sin(t),np.cos(t)]])
        Ws.append((Q*np.exp(rng.uniform(-3,3,2)))@Q.T)
    for p in [1.5,2.,3.,5.]:
        M=max(cp(Ws,probs_interval(i,i+k,N),p) for i in range(N) for k in range(1,N+3))
        for rep in range(40):
            a=rng.uniform(-10,10); length=np.exp(rng.uniform(-5,5))
            C=cp(Ws,probs_interval(a,a+length,N),p)
            assert C<=3**p*M*(1+1e-9)
            maxscaled=max(maxscaled,C/M)
print('20 Hilbert cell-average coefficients verified by actual numerical quadrature.')
print('4800 random non-aligned periodic intervals verified against aligned bound.')
print('Largest nonaligned/aligned ratio:',maxscaled)
Path('workspace/agent4_finite_hilbert_checks.py').write_text(Path(__file__).read_text())
Path('workspace/agent4_finite_hilbert.md').write_text(r'''# Rigorous finite discretization for searching lower bounds

Let I_i=[i,i+1), i=0,...,N-1, and let f have constant value f_i on I_i
and vanish outside [0,N]. Let the positive matrix weight have constant
value W_i on I_i. Jensen on each output cell gives

 ||Hf||Lp(W;[0,N])^p >= sum_i |W_i^(1/p) sum_j T_ij f_j|^p,

where T_ii=0 and for d=i-j!=0,
T_ij=sgn(d)/pi[(|d|+1)log(|d|+1)-2|d|log|d|+(|d|-1)log(|d|-1)],
with 0log0=0. This is the EXACT cell average of the Hilbert kernel,
not the rough sampling1/(i-j). The code verifies20coefficients by
independent quadrature of the triangular difference distribution.
Thus a finite-dimensional norm lower is a true continuum lower.

Extend the N-cell weight periodically. Let C be the largest exact
mixed characteristic on aligned intervals of integer lengths1,...,N+2
and any initial cell (cyclic). Then global[W]Ap<=3^p C.
Indeed for an interval length>=N, cover by a union of whole periods,
with length ratio<=3; its normalized weight distribution is exactly
the period distribution. For lengths1<=|I|<N, the smallest aligned
cover has length<|I|+2<=3|I| and integer length<=N+2. Increasing both
integrations from I to its cover changes the characteristic by at
most(length ratio)^p. Finally intervals length<1 contain at mosttwo
matrix values, with arbitrary probabilities. Each probability is at
most2times the equal-probability distribution on the adjacent pair;
the mixed integral therefore costs at most2^p, and the equal pair is
included in C. This gives a global upper independent ofN.

The finite-valued periodic weight is bounded above and below by fixed
positive constants. Step f can therefore be approximated by smooth
compactly supported f in both input and output weighted norms using
ordinary unweighted Hilbert Lp boundedness. Hence these lower models
are admissible for the question's smooth-input formulation.
''')
