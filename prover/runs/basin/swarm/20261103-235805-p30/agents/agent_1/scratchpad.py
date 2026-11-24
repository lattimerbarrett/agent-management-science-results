from pathlib import Path
code='''from itertools import combinations
from math import comb
import sympy as S

def poly(roots):
    p = [1]
    for r in roots:
        q = [0]*(len(p)+1)
        for k,c in enumerate(p):
            q[k] -= r*c
            q[k+1] += c
        p = q
    return p

def check(s):
    assert s >= 3
    n = 2**(s-1); m = n//2; j = 2*n-2; d = 3*n-2
    # Upper Euler polynomial: verify every surviving coefficient.
    surviving = { (j+k,2*j-k) for k in range(j+1)
                  if j+k <= d and 2*j-k <= d and comb(j,k)%2 }
    assert surviving == {(d-2,d),(d,d-2)}
    roots = [2**r for r in range(2*m-2)]
    w = poly(roots)
    K = S.zeros(m); K[m-2,m-1]=1; K[m-1,m-2]=-1
    I = S.eye(n)
    forms = [I, S.zeros(m).row_join(-K).col_join(K.row_join(S.zeros(m)))]
    for k in range(2*m-2):
        C = S.Matrix(m,m,lambda a,b: int(a+b==k)-w[k]*int(a+b==2*m-2))
        Z = S.zeros(m)
        forms.extend([C.row_join(Z).col_join(Z.row_join(-C)),
                      Z.row_join(C).col_join(C.row_join(Z))])
    assert len(forms)==j
    # Check every form is symmetric; exact positive-definite shifts.
    for B in forms:
        assert B==B.T
        h=1+max(sum(abs(B[a,b]) for b in range(n)) for a in range(n))
        A=B+h*I
        assert all(A[a,a]>sum(abs(A[a,b]) for b in range(n) if a!=b) for a in range(n))
        assert A-h*I==B
    # Independently check the real matrix representation on integer inputs.
    for trial in range(3):
        u=[((a+1)*(trial+2)%7-3)+S.I*((a+2)*(trial+3)%5-2) for a in range(m)]
        v=[((a+3)*(trial+1)%5-2)+S.I*((a+1)*(trial+4)%7-3) for a in range(m)]
        ur=S.Matrix([S.re(z) for z in u]+[S.im(z) for z in u])
        vr=S.Matrix([S.re(z) for z in v]+[S.im(z) for z in v])
        c=[S.expand(sum(u[a]*v[k-a] for a in range(m) if 0<=k-a<m)) for k in range(2*m-1)]
        rem=[S.expand(c[k]-w[k]*c[-1]) for k in range(2*m-2)]
        expected=[S.re(sum(S.conjugate(u[a])*v[a] for a in range(m))),
                  S.re((S.Matrix(u).conjugate().T*(S.I*K)*S.Matrix(v))[0])]
        expected += [z for r in rem for z in (S.re(r),S.im(r))]
        assert [(ur.T*B*vr)[0] for B in forms]==expected
    count=0
    for A in combinations(range(2*m-2),m-1):
        A=set(A)
        p=poly([roots[a] for a in A]); q=poly([roots[a] for a in range(2*m-2) if a not in A])
        product=[sum(p[a]*q[k-a] for a in range(m) if 0<=k-a<m) for k in range(2*m-1)]
        assert product==w
        C=sum(a*b for a,b in zip(p,q)); D=p[-2]-q[-2]
        assert C>0 and D%2==1
        assert D==sum((-r if a in A else r) for a,r in enumerate(roots))
        count+=1
    return s,j,d,len(forms),count

if __name__=='__main__':
    for s in (3,4,5):
        print(check(s),flush=True)
'''
Path('workspace/agent1_full_certificate.py').write_text(code)
exec(compile(code,'workspace/agent1_full_certificate.py','exec'))
