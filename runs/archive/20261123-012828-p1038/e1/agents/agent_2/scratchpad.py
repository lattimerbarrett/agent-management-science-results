import mpmath as mp
mp.mp.dps=50
r=mp.mpf(1);R=mp.mpf(2);d=mp.mpf(1);c=(R-r)/(d+mp.sqrt(d*d+(R-r)**2))
f=lambda r,z:r/(mp.sqrt(z*z+r*r)+z)
def vals(z):
 x=f(r,z);y=f(R,z+d);w2=(y-c)*(1+c*x)/((x-c)*(1+c*y));U=(1+x*x)*(1+y*y)
 t=(x-y)**2/U*w2/(1-w2)
 return x,y,mp.sqrt(w2),t,U

def D(xs,ys):
 k=len(xs);A=[mp.mpf(1)];B=[mp.mpf(1)]
 def mul(p,q):
  out=[mp.mpf(0)]*(len(p)+len(q)-1)
  for i,a in enumerate(p):
   for j,b in enumerate(q):out[i+j]+=a*b
  return out
 for x in xs:A=mul(A,[x,1])
 for y in ys:B=mul(B,[y,1])
 A=mul(A,[1,-c]);B=mul(B,[c,1]);M=mp.matrix(k+2)
 for i,(x,y) in enumerate(zip(xs,ys)):
  M[i,i]=1;M[i,i+1]=-x-y;M[i,i+2]=x*y
 for j,v in enumerate(A):M[k,j]=v
 for j,v in enumerate(B):M[k+1,j]=v
 return mp.det(M)
for zs in [(3,1.2),(1.1,.3),(10,.1)]:
 v0,v1=[vals(mp.mpf(z)) for z in zs];x0,y0,w0,t0,U0=v0;x1,y1,w1,t1,U1=v1
 rat=D([x0,x1],[y0,y1])/((1+c*c)*U0*U1)
 print('oneaxis',mp.nstr(D([x0],[y0])/((1+c*c)*U0),12),mp.nstr(1+t0,12),'t0,1',mp.nstr(t0,8),mp.nstr(t1,8))
 P00=(1-w0*w0)/(2*zs[0]);P11=(1-w1*w1)/(2*zs[1]);P01=(1-w0*w1)/(sum(zs));g2=P01**2/(P00*P11)
 rho=(rat-1-t0)/(t1*(1+t0*(1-g2)))
 rho1=(1+x0*y1)**2/((1+x0*x0)*(1+y1*y1))
 rho2=(1+x1*y0)**2/((1+x1*x1)*(1+y0*y0))
 rho3=((1+x0*y1)*(1+x1*y0))/((1+x0*x1)*(1+y0*y1))
 print('zs',zs,'R',mp.nstr(rat,12),'rho_required',mp.nstr(rho,12),'rho1,2,3',*[mp.nstr(q,12) for q in [rho1,rho2,rho3]],'g2',mp.nstr(g2,12))
