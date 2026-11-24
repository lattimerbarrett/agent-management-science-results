from pathlib import Path
code='''"""Exact rational checks of the block minimizer and spectral dynamics.
This file verifies structural lemmas only; it is not an s=2 counterexample.
"""
import sympy as S

def gal_step(A,r,s):
    K=S.Matrix.hstack(*[A**j*r for j in range(s)])
    inds=K.rref()[1]
    K=K[:,list(inds)]
    alpha=(K.T*A*K).inv()*K.T*r
    out=r-A*K*alpha
    assert K.T*out==S.zeros(K.cols,1)
    # Error e=A^-1 r; Pythagorean identity for its Galerkin correction.
    e=A.inv()*r; en=A.inv()*out; corr=K*alpha
    assert S.simplify((e.T*A*e-en.T*A*en-corr.T*A*corr)[0])==0
    return out

def monic_op(nodes,w,s):
    G=S.Matrix([[sum(wi*x**(i+j) for wi,x in zip(w,nodes))
                 for j in range(s)] for i in range(s)])
    rhs=S.Matrix([-sum(wi*x**(i+s) for wi,x in zip(w,nodes))
                  for i in range(s)])
    c=G.inv()*rhs
    return [sum(c[j]*x**j for j in range(s))+x**s for x in nodes],c

def check():
    total=0
    for n in range(3,8):
      nodes=list(map(S.Integer,range(1,n+1))); A=S.diag(*nodes)
      for s in range(1,min(n,4)):
        r=S.Matrix([(-1)**i*(i+1) for i in range(n)])
        w=[x*x/(r.dot(r)) for x in r]
        q,c=monic_op(nodes,w,s)
        # q(0) is nonzero for the positive spectrum.
        rp=gal_step(A,r,s)
        assert rp==S.Matrix([qi*ri/c[0] for qi,ri in zip(q,r)])
        H=sum(wi*qi**2 for wi,qi in zip(w,q))
        wp=[wi*qi**2/H for wi,qi in zip(w,q)]
        q2,c2=monic_op(nodes,wp,s)
        H2=sum(wi*qi**2 for wi,qi in zip(wp,q2))
        defect=sum(wi*(qi*qj-H)**2 for wi,qi,qj in zip(w,q,q2))/H
        assert S.simplify(H2-H-defect)==0
        assert H2>=H>0
        total+=1
    print('Exact Galerkin/polynomial/Lyapunov test cases passed:',total)

if __name__=='__main__':check()
'''
Path('workspace/residual_checks_agent1.py').write_text(code)
exec(compile(code,'workspace/residual_checks_agent1.py','exec'))
