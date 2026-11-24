"""Exact algebra checks for agent4_fullmode_schur.md.
All-count analytic inequalities are proved in the accompanying note, not inferred from sampling.
"""
import sympy as S

def check():
    B,r,R,t,v,q,T,u,E=S.symbols('B r R t v q T u E', real=True)
    K=B*v+r*q
    J=(r*v/B+q)**2+t**2*(B-r)**2/B**2
    f=S.expand(K*K-B*B*J-(B-r)**2*((B+r)**2-t*t))
    f=S.rem(S.Poly(f,v),S.Poly(v*v-(B*B-t*t),v)).as_expr()
    f=S.rem(S.Poly(f,q),S.Poly(q*q-(r*r-t*t),q)).as_expr()
    assert S.expand(f)==0
    f=S.expand((B+T)*(B*(B-T)+r*R)**2-2*B*r*r*R*R
       -(B-T)*(-r*r*R*R+2*B*(B+T)*r*R+B*B*(B-T)*(B+T)))
    assert f==0
    f=S.expand((v/B*(B*B-u*E))**2-(r*R*v/B)**2-(r*R*(B-T)/B)**2
       -(B-T)/B**2*((B+T)*(B*B-u*E)**2-2*B*r*r*R*R))
    f=S.rem(S.Poly(f,v),S.Poly(v*v-(B*B-T*T),v)).as_expr()
    assert S.expand(f)==0
    # Derive the single-spinor norm formula underlying equation (1).
    s,d,Ax,Bx,cp,sp,C,H=S.symbols('s d Ax Bx cp sp C H', real=True)
    p=(s-d)/(s+d)
    # r/rho=Bx+Ax and r*rho=Bx-Ax;
    # cp=cos(phi), sp=sin(phi), C=cos(theta), H=sin(theta).
    direct=((Bx+Ax)+p*(Bx-Ax)+2*r*((R*C-r)*cp+R*H*sp)/(s+d))/(1+p)
    formula=Bx+d*Ax/s+r*((R*C-r)*cp+R*H*sp)/s
    assert S.factor(direct-formula)==0
    # p is exactly the squared cross-root modulus.
    f=S.factor(((R*C-r)**2+(R*H)**2)/(s+d)**2-p)
    num=S.together(f).as_numer_denom()[0]
    num=S.rem(S.Poly(num,H),S.Poly(H*H-(1-C*C),H)).as_expr()
    num=S.rem(S.Poly(num,s),S.Poly(s*s-(d*d+r*r+R*R-2*r*R*C),s)).as_expr()
    assert S.expand(num)==0
    x,y,c,b,dd=S.symbols('x y c b dd', nonzero=True)
    Cxy=r*y*(x*x-1)-R*x*(y*y-1)-2*dd*x*y
    Ccb=r*b*(c*c-1)-R*c*(b*b-1)-2*dd*c*b
    F=r*y*b*(x-c)*(1+x*c)-R*x*c*(y-b)*(1+y*b)
    assert S.expand(F-(c*b*Cxy-x*y*Ccb))==0
    return 6

if __name__=='__main__':
    print('verified',check(),'exact symbolic identities')
