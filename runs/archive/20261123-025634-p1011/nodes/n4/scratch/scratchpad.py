import math
from scipy.special import gammaln

def a(l,n):
 if l<2:return 0.
 return (l-1)**2*(l+n-1)**2*.5*math.exp(gammaln((l-1)/2)+gammaln((l+n)/2)-gammaln((l+n+1)/2)-gammaln(l/2))
def bracket(l,n):
 m=n-1
 km=l*(l+m)**2/(2*l+m-1)
 kp=(l-1)**2*(l+m-1)/(2*l+m-1)
 return (km*a(l-1,n)+kp*a(l+1,n))/a(l,n)+n-l*(l+m-1)
import numpy as np
for n in range(9,41):
 k=np.arange(20000,dtype=float); b=(n+1)/2
 L=k+2
 aa=(L-1)**2*(L+n-1)**2*.5*np.exp(gammaln((L-1)/2)+gammaln((L+n)/2)-gammaln((L+n+1)/2)-gammaln(L/2))
 logI=(2*b)*math.log(2)+gammaln(b+k+1)+gammaln(b)-gammaln(2*b+k+1)
 logh=(2*b+1)*math.log(2)-np.log(2*k+2*b+1)+2*gammaln(k+b+1)-gammaln(k+1)-gammaln(k+2*b+1)
 wt=aa*np.exp(2*logI-logh)
 t=(k+1)*(2*b+k)/(b-1)-1
 A=sum(wt); B=sum(wt*t); C=sum(wt*t*t)
 print(n,B*B/(A*C))
