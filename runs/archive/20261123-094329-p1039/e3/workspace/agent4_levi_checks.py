import sympy as S
import json
from pathlib import Path

def verify(n):
    # Formal independent coordinates z and zb implement Wirtinger differentiation.
    z=S.symbols('z0:'+str(n)); zb=S.symbols('zb0:'+str(n))
    t=z[-1]*zb[-1]
    rho=sum(z[j]*zb[j] for j in range(n-1))+(t-1)**2-4
    grad=S.Matrix([S.diff(rho,v) for v in z])
    levi=S.Matrix(n,n,lambda j,k:S.diff(rho,z[j],zb[k]))
    assert (levi-S.diag(*([1]*(n-1)+[4*t-2]))).applyfunc(S.expand)==S.zeros(n,n)
    q={**dict(zip(z,[S.sqrt(3)]+[0]*(n-1))),**dict(zip(zb,[S.sqrt(3)]+[0]*(n-1)))}
    assert rho.subs(q)==0
    assert grad[-1].subs(q)==0
    assert levi[-1,-1].subs(q)==-2
    # Explicit positive tangent vectors zbar_k e_j-zbar_j e_k.
    for j in range(n-1):
        for k in range(j+1,n-1):
            v=S.zeros(n,1); v[j]=zb[k]; v[k]=-zb[j]
            vb=S.zeros(n,1); vb[j]=z[k]; vb[k]=-z[j]
            assert S.expand((grad.T*v)[0])==0
            assert S.expand((v.T*levi*vb)[0]-(z[j]*zb[j]+z[k]*zb[k]))==0
    return {'n':n,'levi_diagonal':[str(levi[j,j]) for j in range(n)],'negative_tangent_value':-2}

results=[verify(n) for n in range(2,11)]
t=S.symbols('t',real=True)
assert S.solve((t-1)**2-4,t)==[-1,3]
# Critical gradient cases: z'=0 and (w=0 or |w|²=1).
assert ((t-1)**2-4).subs(t,0)==-3
assert ((t-1)**2-4).subs(t,1)==-4
# Positive fiber-radius on 0<=t<3: R²=(3-t)(1+t).
assert S.expand((3-t)*(1+t)-(4-(t-1)**2))==0
Path('workspace').mkdir(exist_ok=True)
Path('workspace/agent4_levi_checks.json').write_text(json.dumps(results,indent=2))
# Reusable standalone verifier: no self-copy or scratchpad access.
print(json.dumps(results,indent=2))
print('All symbolic differential, tangency, smoothness, and fiber-radius checks passed.')
Path('workspace/agent4_geometric_proof.txt').write_text('''For n>=3, write z=(zprime,w) in C^(n-1) x C and set rho=||zprime||^2+(|w|^2-1)^2-4. Let Omega={rho<0}, K={rho<=0}. For t=|w|^2, fiber radius squared is 4-(t-1)^2=(3-t)(1+t). Thus base is the disk |w|<sqrt(3); fibers are nonempty balls. Omega is bounded and connected: first contract zprime linearly to zero inside each fiber, then contract w radially to zero in the base disk. The gradient vanishes only if zprime=0 and either w=0 or |w|^2=1; these give rho=-3 and -4 respectively, so d rho never vanishes on rho=0. Every boundary point is in closure Omega by the regular-value theorem, so K=closure Omega and K is in the required class. The complex Hessian is diag(I_(n-1),4|w|^2-2). At q=(sqrt(3),0,...,0), the w direction is complex tangent and has Levi value -2; boundary is not pseudoconvex. At any point with zprime nonzero, the space {(vprime,0):sum conj(zprime_j)*vprime_j=0} has dimension n-2 and Levi form ||vprime||^2. If zprime=0 on boundary then |w|^2=3, so all zprime directions are tangent with Levi value ||vprime||^2. Consequently for n>=3 there is a positive Levi direction everywhere. THIS DOES NOT PROVE THAT THE EXTERIOR IS OKA: a genuine Oka theorem is still required. No such theorem has been established by this script or this agent.''')
