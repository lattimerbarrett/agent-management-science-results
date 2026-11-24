import sympy as s
from pathlib import Path
z,c,t,N=s.symbols('z c t N',nonzero=True);af,bf,cf,ag,bg,cg=s.symbols('af bf cf ag bg cg');f=z**3+af*z**2+bf*z+cf;g=z**3+ag*z**2+bg*z+cg;q=s.symbols('q');M=lambda x:s.Matrix([[g.subs(z,x),-q],[-q,f.subs(z,x)]]);D=s.diag(-ag-c-t,-af-c-t);Vc=M(c)/(t-c);Vt=-M(t)/(t-c);E=M(z)/((z-c)*(z-t));decomp=z*s.eye(2)-D-Vc/(z-c)-Vt/(z-t);assert all(s.factor(a)==0 for a in E-decomp);assert all(s.factor(a)==0 for a in Vt.diff(t)-(D-t*s.eye(2)+Vc/(t-c)))
a,b,d,e,u,v=s.symbols('a b d e u v');B=s.Matrix([[a,b],[d,e]]);bc=s.Matrix([u,v]);dd0,dd1=s.symbols('dd0 dd1');DD=s.diag(dd0,dd1);Vp=DD-t*s.eye(2)+bc*bc.T/(t-c);Bp=Vp*B.T.inv()/2;bcp=-bc/(2*(t-c));L=s.zeros(5);L[:2,:2]=DD;L[:2,2:3]=bc;L[2:3,:2]=bc.T;L[:2,3:5]=B;L[3:5,:2]=B.T;L[2,2]=c;L[3:5,3:5]=t*s.eye(2);K=s.zeros(5);K[:2,3:5]=-B.T.inv()/2;K[3:5,:2]=B.inv()/2;K[3:5,2:3]=B.inv()*bc/(2*(t-c));K[2:3,3:5]=-bc.T*B.T.inv()/(2*(t-c));Lp=s.zeros(5);Lp[:2,:2]=-s.eye(2);Lp[:2,2:3]=bcp;Lp[2:3,:2]=bcp.T;Lp[:2,3:5]=Bp;Lp[3:5,:2]=Bp.T;Lp[3:5,3:5]=s.eye(2)
assert all(s.factor(x)==0 for x in K*L-L*K-Lp)
print('Exact2x2Nevanlinna decomposition, residue derivative, generic5x5Laxcommutator PASS')
