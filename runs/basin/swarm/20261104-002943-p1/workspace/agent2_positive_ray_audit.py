import sys,numpy as np
sys.path.insert(0,'workspace')
import agent4_positive_ray_projective as f
import agent2_fourminus_ode as m
m.x=f.x;m.p=f.p;m.q=f.q;m.C=f.C;m.w0=f.w0;m.V=f.V;m.n=8;m.na=6;m.nm=2;m.s=4
D=np.load('workspace/agent4_positive_ray_audit.npz');h=D['h'];A=D['A'];kap=float(D['kap']);z=np.r_[f.w0,h,A];out=m.ode(0,z);res=np.r_[out[:8],out[8:12]+kap*h,out[12:]+kap*A]
relative=np.linalg.norm(res)/(kap*np.linalg.norm(z[8:]));assert relative<1e-9
assert np.linalg.norm(f.projective(f.eq))<1e-9
for eps in [1e-6,1e-7]:
    J=np.column_stack([(f.projective(f.eq+eps*np.eye(6)[j])-f.projective(f.eq-eps*np.eye(6)[j]))/(2*eps) for j in range(6)])
    assert np.linalg.norm(J-f.J)<2e-6
    ev=np.linalg.eigvals(J);assert min(ev.real)>0.15 and sum(abs(ev.imag)>0.5)==4
print('Independent 3rd-jet and Jacobian checks confirm the decaying ray and repelling projective focus; this is NOT a counterexample.')
