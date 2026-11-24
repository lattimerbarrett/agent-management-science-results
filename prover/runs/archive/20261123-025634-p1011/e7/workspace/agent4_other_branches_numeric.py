import numpy as np
from scipy.special import gammaln
from pathlib import Path

def ratios(n,N=200000):
 k=np.arange(N+1,dtype=float); l=k+2
 logh=gammaln(k+n+2)-gammaln(k+1)-np.log(k+(n+2)/2)
 logD=np.log(l-1)+gammaln(l/2)+gammaln((l+n+1)/2)-gammaln((l+1)/2)-gammaln((l+n)/2)
 logw=2*np.log(l-1)+2*np.log(l+n-1)-logD-logh
 w=np.exp(logw-logw[0]); R=2*(k+1)*(k+n+1)/(n-1)-1
 ws1=w*(R+1); R1=(n-1)/(n-3)*R+(n+3)/(n-3)
 ws0=w*(R+1)*(R+3); R0=(n-1)/(n-5)*R+2*(n+3)/(n-5)
 corr=lambda wt,r:np.sum(wt*r)**2/(np.sum(wt)*np.sum(wt*r*r))
 return corr(w,R),corr(ws1,R1),corr(ws0,R0)
for n in range(13,61):
 vals=ratios(n)
 print(n,*[round(v,10) for v in vals], 'pass',vals[0]>.75,vals[1]>8/9,vals[2]>15/16)
Path('workspace/agent4_other_branches_numeric.py').write_text(Path(__file__).read_text())
