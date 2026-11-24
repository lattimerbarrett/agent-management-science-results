from sage.all import *
B=PolynomialRing(QQ,'y');y=B.gen();K=NumberField(y**4-5*y*y+5,'a');a=K.gen()
import pickle,time
R=PolynomialRing(K,'x');x=R.gen();P=x**4-5*x*x+4;hh=-x**3-2*x*x+x+8;kk=x*x+4*x+7;E=K(36);D=P*P-1;assert hh*hh-P*kk==E
ff=x*(x+K(3)/2)*(x-a);mom=[((ff*P*x**j).mod(D))[7] for j in range(8)]
def integ(p):
 p=R(p).mod(D);return sum(p[j]*mom[j] for j in range(8))
def add(a,b):return [a[i]+b[i] for i in range(3)]
def neg(a):return [-v for v in a]
def smul(c,a):return [c*v for v in a]
def mul(a,b):return [sum((a[j]*b[i-j] for j in range(i+1)),R.zero()).mod(D) for i in range(3)]
def scalar(a,b):return [sum(a[j]*b[i-j] for j in range(i+1)) for i in range(3)]
def div(a,d):
 o=[]
 for i in range(3):o.append((a[i]-sum((d[j]*o[i-j] for j in range(1,i+1)),R.zero()))/d[0])
 return o
zero=[R.zero()]*3
Vpow=[x**j for j in range(7)]
def mm(w):return [matrix(K,4,4,lambda a,b:integ(w[i]*Vpow[a+b])) for i in range(3)]
def iv(M):
 B=[M[0].inverse()]
 for i in range(1,3):B.append(-B[0]*sum((M[j]*B[i-j] for j in range(1,i+1)),zero_matrix(K,4)))
 return B
def mv(A,b):return [sum((A[j]*b[i-j] for j in range(i+1)),vector(K,4)) for i in range(3)]
def mp(a):return [vector(K,[integ(p*x**j) for j in range(4)]) for p in a]
def vp(v):return [sum(vv[j]*x**j for j in range(4)) for vv in v]
def fitjet(ws,ref):
 inv=iv(mm(ws[0]));aa=vp([-v for v in mv(inv,mp(mul(ws[1],ref)))]);bb=vp([-v for v in mv(inv,mp(add(mul(ws[2],ref),mul(ws[1],aa))))]);ps=[ref,aa,bb];raw=[]
 for i in range(3):
  rr=zero.copy()
  for a in range(i+1):
   for b in range(i-a+1):rr=add(rr,mul(ws[a],mul(ps[b],ps[i-a-b])))
  raw.append(rr)
 den=[[integ(p) for p in rr] for rr in raw];out=[]
 for i in range(3):
  rr=raw[i]
  for j in range(1,i+1):rr=add(rr,neg([sum((den[j][a]*out[i-j][k-a] for a in range(k+1)),R.zero()) for k in range(3)]))
  out.append(div(rr,den[0]))
 return out
w=[R.one(),(-P*hh).mod(D),(P*kk/2).mod(D)];pq=[P,hh,kk/2];qq=[P,-hh,kk/2];Ginv=iv(mm(mul(w,mul(pq,pq))))
assert all(v==0 for v in mp(mul(w,pq)))
def flow(z):
 eta=[(P*z).mod(D),R.zero(),(-E*P*z).mod(D)];out=fitjet(fitjet([w,eta,zero],pq),qq);dr=add(out[1],neg(eta));corr=add(out[2],neg(mul(dr,mul(pq,[z,R.zero(),R.zero()]))));hd=mv(Ginv,mp(mul(pq,corr)));assert hd[0]==vector(K,4) and hd[1]==vector(K,4);return hd[2]
start=__import__('time').time();res={}
for i in range(4):res[(i,i)]=flow(x**i);print('diag',i,flush=True)
for i in range(4):
 for j in range(i+1,4):res[(i,j)]=flow(x**i+x**j)-res[(i,i)]-res[(j,j)];print('cross',i,j,flush=True)
print('Exact facet Q2 coefficient field generated; seconds',__import__('time').time()-start)
pickle.dump({'coeffs':res,'field':K,'a':a,'facetdual':ff},open('workspace/agent3_facet_Q2_exact.pkl','wb'))
