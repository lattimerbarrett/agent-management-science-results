"""High precision rejection of a proposed (false) global entropy lemma.
Checks that log-product-weights curvature can be positive near a fixed cycle.
"""
import json,numpy as np,mpmath as m
from pathlib import Path
D=json.loads(Path('workspace/uniform_entropy_possible_counter_agent4.json').read_text());m.mp.dps=90
s=D['s'];qc=list(map(m.mpf,D['qc']));pc=list(map(m.mpf,D['pc']));B2=m.mpf(D['B2'])
def pq(t):return m.polyval(qc,t)*m.polyval(pc,t)-B2
pp=np.polymul(D['qc'],D['pc']);pp[-1]-=D['B2'];starts=sorted(np.roots(pp).real)
l=[m.findroot(pq,(m.mpf(t)-m.mpf('1e-6'),m.mpf(t)+m.mpf('1e-6'))) for t in starts];n=len(l)
Q=[m.polyval(qc,t)/m.sqrt(B2) for t in l];P=[1/t for t in Q]
rr=[l[i]+m.mpf(t)*(l[i+1]-l[i]) for i,t in zip(D['gaps'],D['tt'])]
pd=[m.fprod(l[i]-l[j] for j in range(n) if j!=i) for i in range(n)]
h=[m.fprod(t-r for r in rr) for t in l];raw=[P[i]*h[i]/pd[i] for i in range(n)];w=[t/sum(raw) for t in raw]
assert min(w)>0
x=[m.sqrt(t) for t in w];y=[Q[i]*x[i] for i in range(n)]
U=m.matrix([[l[i]**j*x[i] for j in range(s+1)] for i in range(n)]);V=m.matrix([[l[i]**j*y[i] for j in range(s+1)] for i in range(n)])
PU=U*(U.T*U)**-1*U.T;PV=V*(V.T*V)**-1*V.T;L=PV+m.diag(P)*PU*m.diag(Q)
coeff=-2*m.diag([1/t for t in x])*(L.T*m.matrix([1/t for t in x]))
E=m.matrix([[x[i]*l[i]**j/h[i] for j in range(n-s-1)] for i in range(n)])
assert m.norm(V.T*E)<m.mpf('1e-70')
K=E.T*m.diag(list(coeff))*E;G=E.T*E;R=m.cholesky(G);KK=R**-1*K*(R.T)**-1
eigs=m.eigsy((KK+KK.T)/2,eigvals_only=True)
assert max(abs(pq(t)) for t in l)<m.mpf('1e-80')
assert max(eigs)>3
print('High precision entropy-curvature eigenvalues:',list(map(lambda t:m.nstr(t,18),eigs)))
