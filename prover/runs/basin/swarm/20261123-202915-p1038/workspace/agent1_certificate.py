import mpmath as mp, math
from fractions import Fraction
mp.mp.dps=80

def mul(a,b):
 c=[mp.mpc(0)]*(len(a)+len(b)-1)
 for i,x in enumerate(a):
  for j,y in enumerate(b):c[i+j]+=x*y
 return c

def ev(a,t):
 return sum(x*t**i for i,x in enumerate(a))

def constants(m):
 alpha=eps=mp.mpf('.5'); beta=100/(mp.mpf('.75')+mp.sqrt(10000+mp.mpf(9)/16));delta=1/(75+mp.sqrt(5626))
 GA=[mp.mpc(1)];GB=GA.copy()
 for j in range(1,m):
  f=[1,mp.j*mp.exp(-mp.j*mp.pi*j/m)];GA=mul(GA,f);GB=mul(GB,f)
 for j in range(m):
  z=mp.exp(2*mp.j*mp.pi*j/m);D=mp.sqrt(10001-200*z.real)
  GA=mul(GA,[1,-mp.conj((100*z-1)/D)]);GB=mul(GB,[(100-z)/D,1])
 GA=[z.real for z in GA];GB=[z.real for z in GB]
 UA=lambda t:(t+alpha)*(1+delta*t)
 UB=lambda t:(t+beta)*(1+eps*t)
 t=1/beta; s=mp.sqrt(alpha/delta);eta=t*UA(s)/s
 Cfourier=sum(abs(ev(GA,t*mp.exp(2*mp.j*mp.pi*j/m))) for j in range(1,m))/m
 r=max([abs(UA(t*mp.exp(2*mp.j*mp.pi*j/m)))/UA(t) for j in range(1,m)]+[mp.mpf(0)])
 Ctail=ev(list(map(abs,GA)),s);c=abs(ev(GA,t))/(2*m)
 CA=ev(list(map(abs,GA)),2);CB=ev(GB,t);g0=GB[0]
 growth=UA(2)*UB(t)/(UA(t)*2*(1+mp.sqrt(beta*eps))**2)
 for K in range(1,100000):
  k=m*K
  cond1=Cfourier*r**k+Ctail*(eta/UA(t))**k<c
  cond2=(k+1)*CA*CB/(c*g0)*growth**k<1
  if cond1 and cond2:return K,k,mp.nstr(growth,12)
 raise RuntimeError

if __name__=='__main__':
 assert Fraction(507,200)*Fraction(199*149,99**2)<8<Fraction(867,100)
 for m in [1,2,3,4,5,7,10,20]:print(m,constants(m),flush=True)
 with open('workspace/agent1_certificate.py','w') as f:f.write(open('scratchpad.py').read())
