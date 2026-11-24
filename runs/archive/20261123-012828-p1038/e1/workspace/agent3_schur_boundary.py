"""Exact positive SOS factorization for the LOWER/UPPER Schur boundary lemma.
Input: the boundary norm-defect expression derived by agent_4.
This certificate fills its reverse-radii case; no global determinant assertion.
"""
import sympy as s

def exact_certificate():
    u,v,k,w=s.symbols('u v k w',real=True,nonzero=True)
    B=(u+1/u)/2; p=(u-1/u)/2
    r=(v+1/v)/2; q=(v-1/v)/2
    h=B-r; K=B*p+r*q; N=r*p+B*q
    co=(1-w*w)/(1+w*w); si=2*w/(1+w*w)
    boundary_squared=(K-k*N*co+k*h*si)**2-h*h*(p*p+r*r+k*k-2*r*k*B*co)
    F=(u*u+v*v)*(1+w*w)+2*k*u*v*(w*w-1)
    A=(u*v+1)*w+u-v
    C=u*v+1+(v-u)*w
    positive=(u*v-1)**2*F*((1+k)*A*A+(1-k)*C*C)/(8*u**3*v**3*(1+w*w)**2)
    assert s.factor(boundary_squared-positive)==0
    # Explicitly positive for u>1,v>=1,0<k<1.
    assert s.expand(F-((u-v)**2*(1+w*w)+2*u*v*((1-k)+(1+k)*w*w)))==0
    assert s.factor(A*A+C*C-((u*v+1)**2+(u-v)**2)*(1+w*w))==0
    # Establish the unsquared K - kN*cos + kh*sin is positive.
    assert s.factor(K*K-k*k*(N*N+h*h)-((1-k*k)*K*K+k*k*h*h*((B+r)**2-1)))==0
    # theta=pi is the w=infinity endpoint and has the positive limit below.
    endpoint=s.factor(s.limit(positive,w,s.oo))
    endpoint_claim=(u*v-1)**2*(u*u+v*v+2*k*u*v)*((1+k)*(u*v+1)**2+(1-k)*(u-v)**2)/(8*u**3*v**3)
    assert s.factor(endpoint-endpoint_claim)==0
    print('5 exact reverse-radii boundary/SOS identities passed')
    return positive

if __name__=='__main__': exact_certificate()
