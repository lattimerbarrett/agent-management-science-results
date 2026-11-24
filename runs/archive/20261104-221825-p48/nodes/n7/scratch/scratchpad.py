import sympy as s
e=s.symbols('e', integer=True, nonnegative=True)
k=s.symbols('k', integer=True)
print('Ext^1(B,A) dimension =',s.summation(12*e+5+k*e,(k,0,6)))
print('Ext^1(A,B) dimension =',s.summation((13+k)*e+7,(k,0,4)))
print('Total off-diagonal dimension =', s.summation(12*e+5+k*e,(k,0,6))+s.summation((13+k)*e+7,(k,0,4)))
# intersections in the basis (S,f)
def dot(x,y):
    a,b=x;c,d=y
    return s.expand(-e*a*c+a*d+b*c)
A=(5,-1);B=(-1,12*e+5);P=(4,12*e+3)
print('P slopes:',dot(A,P),dot(B,P),'mean',s.simplify((dot(A,P)+dot(B,P))/2))
print('Degrees on S:',dot(A,(1,0)),dot(B,(1,0)))
print('Degrees on f:',dot(A,(0,1)),dot(B,(0,1)))
# Check the convexity-index convention in the positive normal-bundle model.
# psi=exp(|z1|^2+|z2|^2)/(|v1|^2+|v2|^2).
# At z=0 and v=(rho,0), its complex Hessian is diagonal.
rho=s.symbols('rho',positive=True)
model_levi=s.diag(rho**-2,rho**-2,rho**-4,-rho**-4)
print('Model Levi eigenvalues:',model_levi.diagonal())
print('Positive eigenvalues = 3, hence q = 5-3 = 2')
