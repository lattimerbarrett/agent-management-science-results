from sage.all import *
import pickle,time
R=PolynomialRing(QQ,'x');x=R.gen();G=x*(x*x-4);P=G*(x-3);Q=G*(x-4);C=QQ(1);D=P*Q-C;ff=(x+1)*(x-1)*(x-QQ(5)/2)
def integ(p):return (ff*Q*R(p)).mod(D)[7]
def gram(p):return matrix(QQ,4,4,lambda i,j:integ(p*x**(i+j)))
def mp(p):return vector(QQ,[integ(p*x**j) for j in range(4)])
def vp(v):return R(list(v))
M=gram(1);N=gram(P*P);Ni=N.inverse();Mi=M.inverse()
assert all(integ(P*x**j)==0 for j in range(4));assert all(integ(P*P*Q*x**j)==0 for j in range(4))
def jet(ws,ref):
 inv=gram(ws[0]).inverse();a=vp(-inv*mp(ws[1]*ref));b=vp(-inv*mp(ws[2]*ref+ws[1]*a));ps=[ref,a,b];raw=[]
 for j in range(3):
  z=R.zero()
  for k in range(j+1):
   for l in range(j-k+1):z+=(ws[k]*ps[l]*ps[j-k-l]).mod(D)
  raw.append(z.mod(D))
 den=list(map(integ,raw));out=[]
 for j in range(3):out.append(((raw[j]-sum(den[k]*out[j-k] for k in range(1,j+1)))/den[0]).mod(D))
 return out

def hidden_flow(lp):
 aa=(x-3)*lp;Z=vp(-Ni*M*vector(QQ,[aa[j] for j in range(4)]));u=(P*Z).mod(D);out=jet(jet([R.one(),u,R.zero()],P),Q);b=(out[1]-u).mod(D);assert b==0
 hd=Ni*mp((P*out[2]).mod(D));ad=vp(-Mi*N*hd);ld,rem=ad.quo_rem(x-3);assert rem==0
 return vector(QQ,[ld[j] for j in range(3)])
res={}
for i in range(3):res[(i,i)]=hidden_flow(x**i)
for i in range(3):
 for j in range(i+1,3):res[(i,j)]=hidden_flow(x**i+x**j)-res[(i,i)]-res[(j,j)]
print('HIDDEN Q',res,flush=True)
pickle.dump(dict(coeffs={ij:list(map(str,v)) for ij,v in res.items()},P=str(P),Q=str(Q),f=str(ff)),open('workspace/agent2_gcd3_hidden_Q.pkl','wb'))
