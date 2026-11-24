"""Exact birational/Dirac identities linking axes and fixed cross spectral curve."""
import sympy as s

def check():
    r,R,x,y,z,d,eta,t=s.symbols("r R x y z d eta t",nonzero=True)
    d_axis=(r*(x-1/x)-R*(y-1/y))/2
    eta_axis=(r*(x+1/x)-R*(y+1/y))/2
    z_axis=y/x
    H=s.Matrix([[d,r-R/z],[r-R*z,-d]])
    L=d*d+r*r+R*R-r*R*(z+1/z)
    assert (H*H-L*s.eye(2)).applyfunc(s.factor)==s.zeros(2)
    A=H.subs({d:d_axis,z:z_axis})
    assert (A*s.Matrix([x,1])-eta_axis*s.Matrix([x,1])).applyfunc(s.factor)==s.zeros(2,1)
    assert s.factor(eta_axis**2-L.subs({d:d_axis,z:z_axis}))==0
    assert s.factor(z_axis.subs({x:-1/x,y:-1/y},simultaneous=True)-1/z_axis)==0
    assert s.factor(eta_axis.subs({x:-1/x,y:-1/y},simultaneous=True)+eta_axis)==0
    c=(R/z-r)/(d+t)
    negative=(H*s.Matrix([c,1])+t*s.Matrix([c,1])).applyfunc(s.factor)
    assert negative[0]==0
    assert s.factor(negative[1]-(t*t-L)/(d+t))==0
    # Inverse coordinate formula on the curve.
    assert s.factor((eta_axis+d_axis)/(r-R*z_axis)-x)==0
    return {"exact_identities":8,"all_passed":True}

if __name__=="__main__":print(check())
