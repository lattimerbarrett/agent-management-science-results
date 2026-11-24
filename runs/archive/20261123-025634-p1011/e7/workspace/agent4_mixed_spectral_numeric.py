import numpy as np
from scipy.special import gammaln
from pathlib import Path

def ratio(n,N=100000):
 j=np.arange(N+1,dtype=float); l=j+2
 a=(n+2)/2
 logh=gammaln(j+n+2)-gammaln(j+1)-np.log(j+a) # ignore common constant
 logD=np.log(l-1)+gammaln(l/2)+gammaln((l+n+1)/2)-gammaln((l+1)/2)-gammaln((l+n)/2)
 logw=2*np.log(l-1)+2*np.log(l+n-1)-logD-logh
 w=np.exp(logw-logw[0]); R=2*(j+1)*(j+n+1)/(n-1)-1
 A=np.sum(w); B=np.sum(w*R); C=np.sum(w*R*R)
 return A,B,C,B*B/(A*C)
for n in list(range(29,36))+[40,50,100,200]:
 A,B,C,R=ratio(n)
 print(n,'ratio=',R,'A,B,C=',A,B,C)
Path('workspace/agent4_mixed_spectral_numeric.py').write_text(Path(__file__).read_text())
