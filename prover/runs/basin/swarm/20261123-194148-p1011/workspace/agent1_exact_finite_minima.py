from pathlib import Path
import sympy as s
exec(Path('workspace/agent1_all_exact_spd.py').read_text().split("if __name__=='__main__':")[0])
z=s.symbols('z')
p=[s.Integer(1),-s.Rational('0.46283557'),s.Rational('0.05655270'),-s.Rational('0.00140805')]
def interval_poly(poly,wl,wh,zl,zh):
 lo=hi=0
 for (i,j),c in s.Poly(s.expand(poly),w,z).terms():
  a,b=wl**i*zl**j,wh**i*zh**j
  lo+=c*(a if c>=0 else b);hi+=c*(b if c>=0 else a)
 return lo,hi
for n in range(19,33):
 m=n-1;C2=universal_C(n,2,3);C1=universal_C(n,1,3);C3=universal_C(n,3,2)/4
 assert s.simplify(C1[0,0]-2*(C2[0,1]+C2[0,0])/(n-1))==0
 assert s.simplify(C3[0,0]-((n-1)*C2[0,1]-(n+3)*C2[0,0])/2)==0
 wl,wh=w_interval(n);P=s.Matrix([p[q]*z**q for q in range(4)])
 D=s.expand(sum((i+j+1)*C2[i,j]*p[i]*p[j]*z**(i+j) for i in range(4) for j in range(4)))
 roots=s.nroots(D.subs(w,(wl+wh)/2),maxsteps=200)
 root=next(float(s.re(r)) for r in roots if abs(float(s.im(r)))<1e-9 and float(s.re(r))>0 and float(s.diff(D,z).subs(w,(wl+wh)/2).subs(z,s.re(r)))<0)
 zl=s.Rational(int(root*10**8),10**8);zh=zl+s.Rational(1,10**8)
 assert interval_poly(D,wl,wh,zl,zl)[0]>0
 assert interval_poly(D,wl,wh,zh,zh)[1]<0
 assert interval_poly(s.diff(D,z),wl,wh,zl,zh)[1]<0
 R1=s.Matrix([P[q]*(2+s.Rational(4*q,m+2)) for q in range(1,4)])
 R3=s.Matrix([2*q*P[q] for q in range(1,4)])
 bounds=[]
 for rho in [0,1]:
  R2=s.Matrix([q*P[q]*((2+8*rho)+s.Rational(4*(1+4*rho)*(q-1),m+4)) for q in range(1,4)])
  H=-(s.Rational(m+2,2)*rho*(R1.T*C1*R1)[0]+s.Rational(1,m+4)*(1+s.Rational(2*m*rho,m+2))*(R3.T*C3*R3)[0]+(P.T*C2[:,:3]*R2)[0])
  hlo=interval_poly(H,wl,wh,zl,zh)[0];assert hlo>0;bounds.append(float(hlo))
 print(n,'EXACT full minimum z in',zl,zh,'H0,H1 lower',bounds)
