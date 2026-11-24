import sympy as S
l=S.symbols('l1:5', positive=True)
w=S.symbols('w1:5', positive=True)
z=S.symbols('z')
# Spectral weights are squared residual coordinates.
# At s=2 solve sum_i w_i lambda_i^j p(lambda_i)=0, j=0,1.
m=[sum(wi*li**j for wi,li in zip(w,l)) for j in range(4)]
G=S.Matrix([[m[1],m[2]],[m[2],m[3]]]); h=S.Matrix(m[:2]);c=G.inv()*h
print('s=2 coefficients c0,c1 in p(z)=1-c0*z-c1*z**2:')
print('c0=(m0*m3-m1*m2)/(m1*m3-m2**2)')
print('c1=(m1**2-m0*m2)/(m1*m3-m2**2)')
# Verify explicit exact polynomial and updated directions, without convergence assumptions.
lam=[1,2,3,4,5];r=S.ones(5,1)
for k in range(4):
    mm=[sum(r[i]**2*S.Integer(lam[i])**j for i in range(5)) for j in range(4)]
    cc=S.Matrix([[mm[1],mm[2]],[mm[2],mm[3]]]).inv()*S.Matrix(mm[:2])
    pp=S.factor(1-cc[0]*z-cc[1]*z*z)
    rr=S.Matrix([r[i]*pp.subs(z,lam[i]) for i in range(5)])
    if k<2: print('block',k,'p=',pp,'r_next=',list(rr))
    print('block',k,'orthogonality checks:',[(sum(rr[i]*r[i]*lam[i]**j for i in range(5))).simplify() for j in range(2)])
    r=rr
# When exactly s+1 distinct active eigenvalues, inverse-coordinate form gives two-step return.
for s in [1,2,3]:
    lam=list(range(1,s+2));r=S.Matrix(list(range(1,s+2)))
    start=r
    for k in range(2):
        K=S.Matrix.hstack(*[S.diag(*lam)**j*r for j in range(s)])
        r=r-S.diag(*lam)*K*(K.T*S.diag(*lam)*K).inv()*K.T*r
    print('s=',s,'active s+1; coordinate ratios after two blocks:',[S.factor(r[i]/start[i]) for i in range(s+1)])
