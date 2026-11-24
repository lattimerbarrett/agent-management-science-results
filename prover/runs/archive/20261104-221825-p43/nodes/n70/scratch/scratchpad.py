import sympy as s
u,v,ss,t,ep,A,Ap,d,dp=s.symbols('u v s t ep A Ap d dp',real=True)
b=1+ep*Ap*dp
Yh=s.expand((-ep*A*dp)*(Ap*v)+(b*v)*A+(ss/2)*t+(t/2)*ss)
YD=s.expand((-ep*A*dp)*dp+2*v*b*v+ss**2+t**2)
print('Formal normal-form identity Yh-h:',s.simplify(Yh-(A*v+ss*t)))
print('Formal YD:',YD)
# Exact collar requirement for a radial cone F=psi(r)g(theta):
print('At critical theta of g, outward derivative of F has sign(g), since psi\'(1)>0.')
print('Boundary equality alone does not check this sign for the original h.')
