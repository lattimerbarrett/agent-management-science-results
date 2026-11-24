from sage.all import *
import pickle,time
F=QuadraticField(286,'b',embedding=AA(286).sqrt());b=F.gen();R=PolynomialRing(F,'x');x=R.gen();ga=x*(x*x-4);ra=(161-6*b)/25;rb=(161+6*b)/25;A=x-ra;B=x-rb;P=ga*A;Q=ga*B;E=F(1);D=P*Q-1;ff=(x+1)*(x-1)*(x-(2+ra)/2)
ll=QQ(121)/3330*x*x+QQ(35)/333*x+QQ(1)/5;kk=(A*B*ll*ll-1)//ga;assert A*B*ll*ll-ga*kk==1
p1=A*ll;q1=-B*ll
p2=R.lagrange_polynomial([(r,kk(r)/(2*B(r))) for r in [-2,0,2]]+[(ra,-1/Q(ra))])
q2=R.lagrange_polynomial([(r,kk(r)/(2*A(r))) for r in [-2,0,2]]+[(rb,-1/P(rb))])
assert Q*p1+P*q1==0 and Q*p2+P*q2+p1*q1==-1
mom=[(ff*Q*x**j).mod(D)[7] for j in range(8)]
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
def mm(w):return [matrix(F,4,4,lambda a,b:integ(w[i]*Vpow[a+b])) for i in range(3)]
def iv(M):
 B=[M[0].inverse()]
 for i in range(1,3):B.append(-B[0]*sum((M[j]*B[i-j] for j in range(1,i+1)),zero_matrix(F,4)))
 return B
def mv(A,b):return [sum((A[j]*b[i-j] for j in range(i+1)),vector(F,4)) for i in range(3)]
def mp(a):return [vector(F,[integ(p*x**j) for j in range(4)]) for p in a]
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
w=[R.one(),(P*q1).mod(D),(P*q2).mod(D)];pq=[P,p1,p2];qq=[Q,q1,q2];Ginv=iv(mm(mul(w,mul(pq,pq))))
assert all(v==0 for v in mp(mul(w,pq)))
def flow(z):
 eta=[(P*z).mod(D),R.zero(),(-P*z).mod(D)];out=fitjet(fitjet([w,eta,zero],pq),qq);dr=add(out[1],neg(eta));corr=add(out[2],neg(mul(dr,mul(pq,[z,R.zero(),R.zero()]))));hd=mv(Ginv,mp(mul(pq,corr)));assert hd[0]==vector(F,4);return hd
res={}
for i in range(3):res[(i,i)]=flow(-B*x**i)
for i in range(3):
 for j in range(i+1,3):
  val=flow(-B*(x**i+x**j));res[(i,j)]=[val[k]-res[(i,i)][k]-res[(j,j)][k] for k in range(3)]
print('Q1HIDDEN')
for ij,v in res.items():
 pp=R(list(v[1]));ld,rem=pp.quo_rem(-B);print(ij,'hd1',v[1],'hidden ldot',ld,'remainder',rem)
pickle.dump(dict(coeffs={ij:[[str(c) for c in v[k]] for k in range(3)] for ij,v in res.items()},P=str(P),Q=str(Q),f=str(ff),l=str(ll),k=str(kk),p2=str(p2),q2=str(q2)),open('workspace/agent2_gcd3_fold_transverse.pkl','wb'))
