from fractions import Fraction
import sympy as s
import json, os

def check_egf(r):
    x=s.symbols('x:'+str(r))
    B=s.ones(r)-s.eye(r)
    X=s.diag(*x)
    F=B*(s.eye(r)-X*B).inv()
    D=1-s.Add(*(z/(1+z) for z in x))
    for a in range(r):
        for b in range(r):
            rhs=1/((1+x[a])*(1+x[b])*D)-(1/(1+x[a]) if a==b else 0)
            assert s.cancel(F[a,b]-rhs)==0
    return True

def covariance_check(r):
    # Color-chain count covariance per unit time on the zero-sum space.
    P=(s.ones(r)-s.eye(r))/(r-1)
    Pi=s.ones(r)/r
    C0=s.eye(r)/r-s.ones(r)/r**2
    # sum lag covariance via geometric inverse restricted off stationary mode
    S=C0*(2*(s.eye(r)-P+Pi).inv()-s.eye(r))
    target=s.Rational(r-2,r**2)*(s.eye(r)-Pi)
    assert S==target
    # factorial label multiplier subtracts r/2 from Gaussian coefficient
    A=s.Rational(r*r,2*(r-2))-s.Rational(r,2)
    assert A==s.Rational(r,r-2)
    B=s.Rational(2*r,r-1)
    assert 2*A>B
    return {'imbalance_coefficient':str(A),'edge_marginal':str(B)}

if __name__=='__main__':
    ans={'egf_checks':{},'covariances':{}}
    for r in (3,4):
        ans['egf_checks'][r]=check_egf(r)
    for r in range(3,21):
        ans['covariances'][r]=covariance_check(r)
    os.makedirs('workspace',exist_ok=True)
    with open('workspace/agent1_symbolic_checks.json','w') as f:json.dump(ans,f,indent=2)
    with open('workspace/agent1_symbolic_checks.py','w') as f:f.write(open(__file__).read())
    print(json.dumps(ans,indent=2))
