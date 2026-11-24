import sys,json
from pathlib import Path
import numpy as np
from scipy.linalg import null_space
sys.path.insert(0,str(Path('experiments/e1').resolve()))
from agent2_core_ratio import cores
import mpmath as mp

# Search for an explicit dependency in the exact cyclic blocks, retaining
# the geometric coupling y-1/y = r*(x-1/x)-2*d (R=1).
def convnorm(p,f):
    p=np.convolve(p,np.array(f,dtype=np.longdouble));return p/np.max(abs(p))
def corefloat(m,r,d):
    H=np.ones(m,dtype=np.longdouble)
    for j in range(1,m):H[j]=H[j-1]/np.tan(np.longdouble(j)*np.pi/(2*m))
    H/=max(H)
    c0=(1-r)/(d+np.hypot(d,1-r))
    A=np.array([1,-c0],dtype=np.longdouble);B=np.array([c0,1],dtype=np.longdouble)
    for k in range(1,(m+1)//2):
        th=2*np.pi*k/m
        re=np.cos(th)-r;im=-np.sin(th)
        D=d+np.sqrt(d*d+re*re+im*im)
        cr=re/D;ci=im/D
        br=(1-r*np.cos(th))/D;bi=-r*np.sin(th)/D
        A=convnorm(A,[1,-2*cr,cr*cr+ci*ci]);B=convnorm(B,[br*br+bi*bi,2*br,1])
    if m%2==0:
        c=(1+r)/(d+np.hypot(d,1+r))
        A=convnorm(A,[1,c]);B=convnorm(B,[c,1])
    return convnorm(A,H),convnorm(B,H)
def blocksfloat(m,r,d,heights):
    v=np.array(heights,dtype=np.longdouble)/r
    x=np.where(v>=0,np.hypot(v,1)+v,1/(np.hypot(v,1)-v))
    v=np.array(heights,dtype=np.longdouble)-d
    y=np.where(v>=0,np.hypot(v,1)+v,1/(np.hypot(v,1)-v))
    A,B=corefloat(m,r,d)
    for xi,yi in zip(x,y):A=convnorm(A,[xi,1]);B=convnorm(B,[yi,1])
    c=len(x);n=c+2*m
    vals=[]
    for q in range(m):
        inds=list(range(q,c,m));cols=list(range(q,n,m));k=len(inds)
        Q=np.zeros((k+2,k+2))
        for j,i in enumerate(inds):
            u=x[i]**m;v=y[i]**m
            row=np.array([1,-u-v,u*v],dtype=np.longdouble)
            Q[j,j:j+3]=row/max(abs(row))
        ar=np.asarray(A[cols],float);br=np.asarray(B[cols],float)
        # Positive column rescaling balances all rows before determinant.
        Q[-2]=ar/max(abs(ar));Q[-1]=br/max(abs(br))
        for _ in range(4):
            Q/=np.maximum(np.linalg.norm(Q,axis=0),1e-300)
            Q/=np.maximum(np.linalg.norm(Q,axis=1)[:,None],1e-300)
        sign,ld=np.linalg.slogdet(Q)
        sv=np.linalg.svd(Q,compute_uv=False)[-1]
        vals.append((sign,sv,ld))
    return vals

def search():
    rng=np.random.default_rng(918322)
    counts=0;neg=[];small=[]
    for it in range(1800):
        m=int(rng.integers(1,25));a=int(rng.integers(1,45));b=int(rng.integers(1,45))
        r=np.exp(rng.uniform(-5,-.01));d=np.exp(rng.uniform(-5,5))
        low=-np.sort(np.exp(rng.uniform(-5,5,a)))[::-1]
        high=d+np.sort(np.exp(rng.uniform(-5,5,b)))
        h=np.r_[low,high]
        vals=blocksfloat(m,r,d,h)
        for q,(sg,sv,ld) in enumerate(vals):
            counts+=1
            if sg<=0:
                neg.append(dict(m=m,r=r,d=d,a=a,b=b,h=h.tolist(),q=q,sv=sv,sign=sg))
        if len(neg)>10:break
    print('blocks examined:',counts,'floating negative candidates:',len(neg))
    Path('relation_search.json').write_text(json.dumps(neg))
    if neg:print(neg[0])
if __name__=='__main__':search()
