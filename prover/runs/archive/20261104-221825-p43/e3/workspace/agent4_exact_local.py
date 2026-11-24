import sympy as s
from pathlib import Path
rt=s.sqrt
x0=s.Matrix([-1,1,rt(3)])/rt(5);y0=s.Matrix([1,-1,rt(3)])/rt(5);r0=rt(s.Rational(12,5));U=rt(s.Rational(4,5));T=rt(s.Rational(3,20));Z=rt(s.Rational(1,20));B=5*s.pi/48;C=s.symbols('C',real=True);A=-(B+3*C)*r0*r0
E1=s.Matrix([1,1,0])/rt(2);Ex=E1.row_join(x0.cross(E1));Ey=E1.row_join(y0.cross(E1))
def qmat(U,T,Z):return s.Matrix([[1-2*Z**2,-2*U*Z,2*T*Z],[2*U*Z,1-2*(T*T+Z*Z),-2*U*T],[2*T*Z,2*U*T,1-2*T*T]])
AA=qmat(U,T,Z);BB=qmat(U,-T,Z)
v=s.Matrix(s.symbols('v0:3'));xx=s.Matrix(s.symbols('x0:3'));r=s.sqrt(v.dot(v));z=v[2];beta=A+B*r*r+3*C*z*z;theta=2*B*r*z;n=s.Matrix([0,0,1]);axis=v/r
# Differentiate composition before substitution: derivative wrt six original coords.
vars=list(s.symbols('q0:4'));q=s.Matrix(vars);x=x0+Ex*q[:2,0];y=y0+Ey*q[2:,0];vv=x+y
subsbase={v[i]:(x0+y0)[i] for i in range(3)};subsbase.update({xx[i]:x0[i] for i in range(3)})
rot=xx*s.cos(theta)+axis.cross(xx)*s.sin(theta)+axis*axis.dot(xx)*(1-s.cos(theta))
Rz=s.Matrix([[s.cos(beta),-s.sin(beta),0],[s.sin(beta),s.cos(beta),0],[0,0,1]])
F=Rz*rot
# Ambient derivative evaluated at base x and y separately, then chain with v=x+y
Jcols=[]
for iq in range(4):
 dx=Ex[:,iq] if iq<2 else s.zeros(3,1);dy=Ey[:,iq-2] if iq>=2 else s.zeros(3,1);dv=dx+dy
 outputs=[]
 for base,Mat,E,dw in [(x0,AA,Ex,dx),(y0,BB,Ey,dy)]:
  sb={v[i]:(x0+y0)[i] for i in range(3)};sb.update({xx[i]:base[i] for i in range(3)})
  out=s.zeros(3,1)
  for j in range(3):out+=F.diff(v[j]).subs(sb)*dv[j]+F.diff(xx[j]).subs(sb)*dw[j]
  outputs.extend(E.T*(Mat.T*out-dw))
 Jcols.append(s.Matrix(outputs).applyfunc(s.simplify))
J=s.Matrix.hstack(*Jcols);print('J',J)
minor=s.factor(J[:3,:3].det());print('minor',minor);cs=s.solve(minor,C);print('Csol',cs)
for c in cs:print('rank',J.subs(C,c).rank(),'null',J.subs(C,c).nullspace())
# Exact quadratic reduction on kernel, including normalized sphere chart.
u,w=s.symbols('u w',real=True)
def tr(expr):
 return s.Add(*[cc*u**ij[0]*w**ij[1] for ij,cc in s.Poly(s.expand(expr),u,w).terms() if sum(ij)<=2])
def tv(M):return M.applyfunc(tr)
c=cs[0];J0=J.subs(C,c);NK=J0.nullspace();NL=J0.T.nullspace()
dx=Ex*s.Matrix(NK[0][:2]);dy=Ey*s.Matrix(NK[1][2:]);X=x0+dx*u-dx.dot(dx)*x0*u*u/2;Y=y0+dy*w-dy.dot(dy)*y0*w*w/2
S=X+Y;S1=dx*u+dy*w;S2=S-x0-y0-S1;r1=S1[2];r2=tr(S2[2]+(S1[0]**2+S1[1]**2)/(2*r0));rr=r0+r1+r2
inv=tr(1/r0-r1/r0**2-r2/r0**2+r1*r1/r0**3);axis2=tv(S*inv)
bet=tr(A.subs(C,c)+B*tr(rr*rr)+3*c*tr(S[2]*S[2]));th=tr(2*B*rr*S[2]-s.pi/2)
# cos(theta)=-th, sin(theta)=1-th^2/2
cost=-th;sint=tr(1-th*th/2);cosb=tr(1-bet*bet/2);sinb=bet
outs=[]
for Xb,Mat,E in [(X,AA,Ex),(Y,BB,Ey)]:
 rt2=tv(Xb*cost+tv(axis2.cross(Xb))*sint+tv(axis2*tr(axis2.dot(Xb)))*tr(1-cost))
 rz=tv(s.Matrix([cosb*rt2[0]-sinb*rt2[1],sinb*rt2[0]+cosb*rt2[1],rt2[2]]))
 outs.extend(tv(E.T*(Mat.T*rz-Xb)))
Out=s.Matrix(outs);Q=s.Matrix.hstack(*NL).T*Out
print('leftnull',NL);Q=Q.applyfunc(s.simplify);print('quadraticreduction',Q)
KD=s.Matrix.hstack(s.eye(4)[:,0],s.eye(4)[:,2],*NK);OD=s.Matrix.hstack(J0[:,0],J0[:,2],*NL)
print('orientation determinants',s.simplify(KD.det()),s.simplify(OD.det()))
ss,tt=s.symbols('ss tt',real=True)
Qnew=(Q.subs({u:(ss+tt)/2,w:(ss-tt)/2},simultaneous=True));print('sumdiff transformed',s.simplify(Qnew[0]+Qnew[1]),s.simplify(Qnew[0]-Qnew[1]))

# Certified symbolic checks of the corank-two and degree-two leading germ.
assert cs == [s.Rational(5,24)-5*s.pi/48]
assert J0.rank()==2
assert s.simplify(KD.det()+1)==0
assert s.simplify(OD.det()-s.Rational(4,3))==0
K=14-10*s.pi
assert s.simplify(Qnew[0]+Qnew[1]-s.sqrt(6)/60*2*K*ss*tt)==0
assert s.simplify(Qnew[0]-Qnew[1]-s.sqrt(6)/60*(K*ss**2+44*tt**2))==0
# K<0 follows already from pi>3. The two quadratic components have
# no simultaneous real zero away from the origin: ss*tt=0, then
# K*ss^2+44*tt^2=0 force ss=tt=0. Linear changes identify the map
# with an orientation reversal of complex squaring, degree -2.
print("All exact local-germ assertions passed.")
