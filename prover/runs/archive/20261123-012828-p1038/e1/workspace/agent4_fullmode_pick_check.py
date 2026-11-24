"""Supplemental complex analytic checks. Proof is in agent4_fullmode_schur.md."""
import mpmath as mp
import random

def check(trials=40,dps=90):
    mp.mp.dps=dps; rng=random.Random(429)
    worstnorm=mp.mpf(0); worstpick=mp.inf
    for it in range(trials):
        r=mp.exp(rng.uniform(-3,3)); R=mp.exp(rng.uniform(-3,3))
        d=mp.exp(rng.uniform(-3,3));theta=mp.mpf(rng.uniform(-mp.pi,mp.pi))
        s=mp.sqrt(d*d+r*r+R*R-2*r*R*mp.cos(theta))
        c=(R*mp.exp(-1j*theta)-r)/(d+s);b=mp.exp(1j*theta)*c
        def g(t,z):
            root=mp.sqrt(z*z+t*t)
            # RHP nontangential boundary branch at negative imaginary arguments.
            if mp.re(z)==0 and mp.im(z)<-t:root=-root
            return t/(z+root)
        def lower(z):
            x=g(r,z);y=g(R,z+d)
            return mp.sqrt(r*y/(R*x))*(1+x*c)/(1+y*b)
        def upper(z):
            a=g(r,z+d);be=g(R,z)
            return mp.sqrt(r*be/(R*a))*(a+c)/(be+b)
        # Boundary identity (1), independently from moduli.
        tt=mp.mpf(rng.uniform(-5,5))*max(r,R,d)
        z=1j*tt;x=g(r,z);y=g(R,z+d)
        rho=abs(x);sig=abs(y);phi=mp.arg(x);psi=mp.arg(y)
        Ax=r*(1/rho-rho)/2;Bx=r*(1/rho+rho)/2
        Ay=R*(1/sig-sig)/2;By=R*(1/sig+sig)/2
        delta=(R/abs(y)*abs(1+y*b)**2-r/abs(x)*abs(1+x*c)**2)/(1+abs(c)**2)
        formula=s*(By-Bx)+d*(Ay-Ax)+R*R*mp.cos(psi)+r*r*mp.cos(phi)-r*R*mp.cos(theta)*(mp.cos(psi)+mp.cos(phi))+r*R*mp.sin(theta)*(mp.sin(psi)-mp.sin(phi))
        assert abs(s*delta-formula)<mp.mpf('1e-70')*max(1,abs(formula))
        assert delta>0
        nodes=[mp.exp(rng.uniform(-4,4))+1j*mp.mpf(rng.uniform(-5,5)) for _ in range(5)]
        for fun in (lower,upper):
            vals=[fun(z) for z in nodes]
            worstnorm=max(worstnorm,max(map(abs,vals)))
            assert all(abs(v)<1 for v in vals)
            P=mp.matrix([[(1-vals[i]*mp.conj(vals[j]))/(nodes[i]+mp.conj(nodes[j])) for j in range(5)] for i in range(5)])
            eig=mp.eighe(P,eigvals_only=True)
            assert eig[0]>0
            worstpick=min(worstpick,eig[0])
    return dict(geometries=trials,pick_matrices=trials*2,largest_modulus=str(worstnorm),smallest_eigenvalue=str(worstpick))

if __name__=='__main__':print(check())
