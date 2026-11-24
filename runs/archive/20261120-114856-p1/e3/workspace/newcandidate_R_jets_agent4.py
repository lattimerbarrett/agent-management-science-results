from pathlib import Path
src=Path('workspace/fullR_jets_agent4.py').read_text();prefix=src[:src.index('H=K(R(')]
prefix=prefix.replace("K,m,A,B,q,ell,k,T=field('m,A,B,q,ell,k,T',QQ)","K,m,A,B,q,x,y=field('m,A,B,q,x,y',QQ)")
exec(prefix)
u=K(1);bb=K(0);v=K(3);bd=K(R(44,25));H=K(R(3,500));xis=[x,y]
S=u+v;T=u*v+bb+bd;L=u*bd+v*bb;C0=bb*bd-H

def mp(state,bu,b0,bv,b1):
 mm,hh,zz,w1,w2=state;ws=[w1,w2]
 M=[J(1),mm,bu*mm-b0+hh];M.append(bu*M[2]-b0*mm+zz)
 for kk in range(4,8):M.append(S*M[-1]-T*M[-2]+L*M[-3]-C0*M[-4]-2*H*sum((xis[i]**(kk-4)*ws[i] for i in range(2)),J(0)))
 a=(M[3]-mm*M[2])/(M[2]-mm*mm);b=M[2]-a*mm;Q=[b*b,2*a*b,a*a-2*b,-2*a,J(1)]
 nums=[sum((Q[r]*M[jj+r] for r in range(5)),J(0)) for jj in range(4)];norm=nums[0];ms=[nums[jj]/norm for jj in range(1,4)]
 return [ms[0],ms[1]-bv*ms[0]+b1,ms[2]-bv*ms[1]+b1*ms[0]]+[ws[i]*(xis[i]**2-a*xis[i]-b)**2/norm for i in range(2)]
e=J([zero,one,zero,zero]);t0=time.time();aa=mp([J(m),A*e,B*e,q*e**2,(1-q)*e**2],u,bb,v,bd);zz=mp(aa,v,bd,u,bb);print('jets',time.time()-t0,flush=True)
import sympy as sy
sm,sA,sB,sq,sx,syy=sy.symbols('m A B q x y');Qx=sx*(sx-1)*(sx-sy.Rational(4,5))*(sx-sy.Rational(11,5))+sy.Rational(3,500);Qy=Qx.subs(sx,syy)
def reduce(expr):
 num,den=sy.fraction(expr.as_expr());num=sy.rem(num,Qx,sx);num=sy.rem(num,Qy,syy);return sy.cancel(num/den)
a=[reduce(zz[i].a[2]) for i in [1,2]];w=[reduce(zz[i].a[3]) for i in [3,4]]
gamma=sy.cancel(sum(w)/2);F=[reduce(zz[0].a[1]),sy.cancel(a[0]-sA*gamma),sy.cancel(a[1]-sB*gamma),sy.cancel(w[0]-2*sq*gamma)]
pickle.dump((F,gamma),open('workspace/newcandidate_R_ode_agent4.pkl','wb'));print('saved',time.time()-t0,flush=True)
Path('workspace/newcandidate_R_jets_agent4.py').write_text(Path('scratchpad.py').read_text())
