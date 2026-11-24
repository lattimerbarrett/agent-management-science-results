import mpmath as mp
import numpy as np
import sympy as S
mp.mp.dps=100

def ev(c,x):return sum(a*x**j for j,a in enumerate(c))
def op(x,p,s):
 M=mp.matrix([[sum(p[i]*x[i]**(j+k)for i in range(len(x)))for k in range(s)]for j in range(s)])
 rhs=mp.matrix([-sum(p[i]*x[i]**(s+j)for i in range(len(x)))for j in range(s)])
 f=list(mp.lu_solve(M,rhs))+[mp.mpf(1)]
 N=sum(p[i]*ev(f,x[i])**2 for i in range(len(x)))
 return f,N

def dual(x,p,s):
 d=[mp.fprod(x[i]-x[j]for j in range(len(x))if i!=j)for i in range(len(x))]
 q=[1/(d[i]**2*p[i])for i in range(len(x))]
 return op(x,q,len(x)-s-1)[0]

def orbit(x,p,s,m):
 fs=[];Ns=[];Hs=[];ps=[]
 for k in range(m):
  f,N=op(x,p,s);H=dual(x,p,s)
  fs.append(f);Ns.append(N);Hs.append(H);ps.append(p)
  p=[p[i]*ev(f,x[i])**2/N for i in range(len(x))]
 return fs,Ns,Hs,ps

x=list(map(mp.mpf,[-3,-1,1,2,3,0,mp.mpf('2.5')]))
base=x[:5];th=mp.mpf('1.5');d=[mp.fprod(a-b for b in base if b!=a)for a in base]
p=[11*(a-th)/(dd*(a**3-7*a+5))for a,dd in zip(base,d)]
p=[a*(1-mp.mpf('2e-25'))for a in p]+[mp.mpf('1e-25')]*2
z=mp.mpf('-2.05');m=18
f,N,H,ps=orbit(x,p,3,m)
beta=[]
for k in range(m-1):
 roots=np.roots(np.array([float(c)for c in H[k]])[::-1]);assert max(abs(roots.imag))<1e-8 and min(roots.real)>float(z)
 beta.append(ev(f[k],z)*ev(f[k+1],z)/N[k+1]*ev(H[k],z)/ev(H[k+1],z))
assert min(beta)>0
assert all(beta[k+1]<=beta[k]+mp.mpf('1e-80')for k in range(len(beta)-1))
print('original virtual beta min/max',mp.nstr(min(beta),12),mp.nstr(max(beta),12))

# Independently insert an actual tiny spectral weight and recover the root
# displacement directly, rather than merely printing the predicted beta.
eps=mp.mpf('1e-35');xx=x+[z];pp=[a*(1-eps)for a in p]+[eps]
ff,NN,HH,pps=orbit(xx,pp,3,6)
a=[]
for k in range(6):
 h=HH[k]
 rt=mp.findroot(lambda u:ev(h,u),(z-mp.mpf('1e-25'),z+mp.mpf('1e-25')))
 a.append((rt-z)/eps)
for k in range(4):
 assert a[k+2]<=a[k+1]**2/a[k]+mp.mpf('1e-25')
 assert abs(a[k+1]/a[k]-beta[k])<mp.mpf('1e-25')
print('actual epsilon-root displacement beta identity errors',mp.nstr(max(abs(a[k+1]/a[k]-beta[k])for k in range(4)),8))

# Check finite-triple Rayleigh expansion exactly in formal symbols.
e,u,v,h,C=S.symbols('e u v h C',nonzero=True)
J=C*u*h*h
num=J-C*u*u*h*h/v
den=C*u*u*h*h/(e*v*v)
assert S.simplify(v+num/(e*den)-v*v/u)==0
print('formal Rayleigh first-variation algebra PASS')

# Opposite signed displacement: verify convex log amplitudes directly.
x2=list(map(mp.mpf,[1,2,4]));p2=list(map(mp.mpf,['.2','.3','.5']));z2=mp.mpf('1.001')
f2,n2,h2,_=orbit(x2,p2,1,12)
beta2=[ev(f2[k],z2)*ev(f2[k+1],z2)/n2[k+1]*ev(h2[k],z2)/ev(h2[k+1],z2)for k in range(11)]
assert min(beta2)>0
assert all(beta2[k+1]>=beta2[k]-mp.mpf('1e-80')for k in range(10))
ff2,nn2,hh2,_=orbit(x2+[z2],[a*(1-eps)for a in p2]+[eps],1,5)
aa2=[(mp.findroot(lambda u:ev(h,u),(z2-mp.mpf('1e-25'),z2+mp.mpf('1e-25')))-z2)/eps for h in hh2]
assert max(aa2)<0
assert max(abs(aa2[k+1]/aa2[k]-beta2[k])for k in range(4))<mp.mpf('1e-25')
assert all(aa2[k+2]<=aa2[k+1]**2/aa2[k]+mp.mpf('1e-25')for k in range(3))
print('negative-displacement logconvex test PASS')
