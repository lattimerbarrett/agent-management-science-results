from pathlib import Path
src=Path('workspace/fullR_jets_agent4.py').read_text();prefix=src[:src.index('H=K(R(')]
prefix=prefix.replace("K,m,A,B,q,ell,k,T=field('m,A,B,q,ell,k,T',QQ);N=3","K,m,A,B,v,d,H=field('m,A,B,v,d,H',QQ);N=2")
exec(prefix)
u=K(1);bb=K(0);S=u+v;T=u*v+d;L=u*d;C0=-H

def mp(state,bu,b0,bv,b1):
 mm,hh,zz=state;M=[J(1),mm,bu*mm-b0+hh];M.append(bu*M[2]-b0*mm+zz)
 for kk in range(4,8):M.append(S*M[-1]-T*M[-2]+L*M[-3]-C0*M[-4])
 a=(M[3]-mm*M[2])/(M[2]-mm*mm);b=M[2]-a*mm;Q=[b*b,2*a*b,a*a-2*b,-2*a,J(1)]
 nums=[sum((Q[r]*M[jj+r] for r in range(5)),J(0)) for jj in range(4)];norm=nums[0];ms=[nums[jj]/norm for jj in range(1,4)]
 return [ms[0],ms[1]-bv*ms[0]+b1,ms[2]-bv*ms[1]+b1*ms[0]]
e=J([zero,one,zero]);aa=mp([J(m),A*e,B*e],u,bb,v,d);zz=mp(aa,v,d,u,bb)
import sympy as s,pickle
conn=[(zz[i].a[2]/zz[0].a[1]).as_expr() for i in [1,2]];sm,sA,sB,sv,sd,sH=s.symbols('m A B v d H');Mat=s.Matrix([[s.factor(s.diff(c,j)) for j in[sA,sB]] for c in conn]);print(Mat,flush=True)
pickle.dump(Mat,open('workspace/generic_connection_agent4.pkl','wb'))
Path('workspace/generic_connection_agent4.py').write_text(Path('scratchpad.py').read_text())
