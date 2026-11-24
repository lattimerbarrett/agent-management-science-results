import sympy as S
lam=S.Matrix([-3,-2,-1,1,2,3]); sig=lam.applyfunc(lambda x:(x**3-7*x)/6)
V=S.Matrix([[1,x,x*x] for x in lam]);w=S.ones(6,1)/6
M=V.T*S.diag(*w)*V
assert V.T*S.diag(*w)*sig==S.zeros(3,1)
assert all(z*z==1 for z in sig)
def mul(a,b):return a.multiply_elementwise(b)
def expansion(a,b):
    # coefficients for squared-weight residual map at w+e*a+e^2*b
    M1=V.T*S.diag(*a)*V
    c1=-M.inv()*V.T*mul(a,sig)
    c2=-M.inv()*(V.T*mul(b,sig)+M1*c1)
    u=V*c1;v=V*c2
    D=(u.T*S.diag(*w)*u)[0]
    aout=a+2*mul(w,mul(sig,u))
    bout=b+2*mul(a,mul(sig,u))+mul(w,mul(u,u)+2*mul(sig,v)+S.ones(6,1)*D)
    return S.simplify(aout),S.simplify(bout),u
# exact rational perturbations, no floating point
for a in [S.Matrix([1,-2,3,-4,5,-3]),S.Matrix([2,1,-1,3,-2,-3]),S.Matrix([1,-1,0,0,-1,1])]:
    assert sum(a)==0
    a1,b1,u=expansion(a,S.zeros(6,1))
    a2,b2,_=expansion(a1,b1)
    assert S.simplify(a2-a)==S.zeros(6,1)
    D=(u.T*S.diag(*w)*u)[0]
    proj=V*M.inv()*V.T*S.diag(*w)*mul(sig,mul(u,u))
    K=2*mul(w,mul(sig,proj)-mul(u,u)+S.ones(6,1)*D)
    assert S.simplify(b2-K)==S.zeros(6,1)
    assert V.T*mul(sig,K)==S.zeros(3,1)
# symbolic tangent drift for any degree2 normal polynomial u
A,B,C=S.symbols('A B C');u=V*S.Matrix([C,B,A]);D=(u.T*S.diag(*w)*u)[0]
proj=V*M.inv()*V.T*S.diag(*w)*mul(sig,mul(u,u))
K=2*mul(w,mul(sig,proj)-mul(u,u)+S.ones(6,1)*D)
dm1=S.factor((lam.T*K)[0]);dm2=S.factor((lam.applyfunc(lambda x:x*x).T*K)[0])
assert S.simplify(dm1+800*B*(7*A+C)/147)==0
assert S.simplify(dm2+400*(7*A*A+2*A*C+B*B)/63)==0
print('All exact plateau/Taylor checks passed; dm1=',dm1,'dm2=',dm2)
