import mpmath as mp
mp.mp.dps=120
u=mp.mpf(1);v=mp.mpf(4);xi=mp.mpf(9)/8;H=-xi*xi*(xi-u)*(xi-v)
roots=sorted(mp.polyroots([1,-5,4,0,-H],maxsteps=1000))
neg=mp.polyroots([1,-5,4,0,H],maxsteps=1000)
eta=max(mp.re(t)for t in neg if abs(mp.im(t))<mp.mpf('1e-100'))
V=mp.matrix([[x**j for x in roots]for j in range(4)]);iv=V**-1
r=mp.mpf('1e-14')
def step(m,h,z,w1,w2):
 MM=[mp.mpf(1),m,m+h,m+h+z]
 for k in range(4,8):MM.append(5*MM[k-1]-4*MM[k-2]+H*MM[k-4]-2*H*(w1*xi**(k-4)+w2*eta**(k-4)))
 aa=(MM[1]*MM[2]-MM[3])/(MM[2]-MM[1]**2);bb=-MM[2]-aa*MM[1]
 C=[bb*bb,2*aa*bb,aa*aa+2*bb,2*aa,mp.mpf(1)]
 nums=[sum(C[j]*MM[k+j]for j in range(5))for k in range(4)]
 hh=nums[0];n=[t/hh for t in nums]
 return n[1],n[2]-n[1],n[3]-n[2],w1*(xi*xi+aa*xi+bb)**2/hh,w2*(eta*eta+aa*eta+bb)**2/hh

def coeff(endpoint,T,U,Z,W1=0,W2=0):
 missing=2 if endpoint==0 else 1;m0=1-roots[missing]
 am=iv[missing,1]+iv[missing,2]+iv[missing,3];ah=iv[missing,2]+iv[missing,3]
 M=(U-ah*T)/am;m=m0+r*M;h=r*T;z=r*r*Z;w1=r**5*W1;w2=r**5*W2
 o=step(*step(m,h,z,w1,w2))
 L1=mp.log(o[3]/w1)/r**2 if W1 else mp.nan
 L2=mp.log(o[4]/w2)/r**2 if W2 else mp.nan
 return [(o[0]-m)/r**3,(o[1]-h)/r**4,(o[2]-z)/r**5,L1,L2]
if __name__=='__main__':
 for e in [0,1]:
  for T,U,Z in [(1,1,0),(1,2,0),(1,0,0),(-1,1,0),(2,1,0),(1,1,1),(1,1,2),(1,1,-1)]:
   print(e,T,U,Z,[float(q)for q in coeff(e,T,U,Z,1,1)])
