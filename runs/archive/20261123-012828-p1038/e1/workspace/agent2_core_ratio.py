"""High precision diagnostic for base-core coefficient-ratio ordering.
This verifies samples, not a theorem.
"""
import mpmath as mp
from random import Random
import json

def conv(a,b):
    out=[mp.mpf(0)]*(len(a)+len(b)-1)
    for i,x in enumerate(a):
        for j,y in enumerate(b):out[i+j]+=x*y
    return out

def cores(m,r,R,d,include_H=True):
    H=[mp.mpf(1)]
    for j in range(1,m):H.append(H[-1]*mp.cot(j*mp.pi/(2*m)))
    c0=(R-r)/(d+mp.sqrt(d*d+(R-r)**2))
    A=[mp.mpf(1),-c0];B=[c0,mp.mpf(1)]
    for k in range(1,(m+1)//2):
        z=mp.exp(2j*mp.pi*k/m)
        delta=R*z-r;D=d+mp.sqrt(d*d+abs(delta)**2)
        c=mp.conj(delta)/D;b=(R-r*z)/D
        A=conv(A,[1,-2*mp.re(c),abs(c)**2])
        B=conv(B,[abs(b)**2,2*mp.re(b),1])
    if m%2==0:
        c=-(R+r)/(d+mp.sqrt(d*d+(R+r)**2))
        A=conv(A,[1,-c]);B=conv(B,[-c,1])
    return (conv(H,A),conv(H,B)) if include_H else (A,B)

def run(max_m=50,trials=20,dps=800,seed=2217):
    mp.mp.dps=dps;rng=Random(seed);count=0;worst=None
    for m in range(1,max_m+1):
        for trial in range(trials):
            r=mp.exp(mp.mpf(str(rng.uniform(-15,-.000001))))
            d=mp.exp(mp.mpf(str(rng.uniform(-15,15))))
            A,B=cores(m,r,mp.mpf(1),d)
            assert min(B)>0
            for e in range(2*m-1):
                left=A[e]*B[e+1];right=A[e+1]*B[e]
                minor=left-right
                margin=minor/(abs(left)+abs(right))
                assert minor>0,(m,str(r),str(d),e,str(minor),str(margin))
                row={"m":m,"r":str(r),"d":str(d),"e":e,"relative_margin":str(margin)}
                if worst is None or margin<mp.mpf(worst["relative_margin"]):worst=row
                count+=1
    return {"cases":max_m*trials,"adjacent_minors_checked":count,"dps":dps,"worst":worst}

if __name__=="__main__":
    result=run();print(result)
    with open("workspace/agent2_core_ratio_results.json","w") as f:json.dump(result,f,indent=2)
