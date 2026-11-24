from pathlib import Path
orig=Path('workspace/agent3_maxpell_Q2_generate.py').read_text()
start=orig.index('def integ');end=orig.index('w=[R.one()');body=orig[start:end].replace('matrix(QQ,','matrix(F,').replace('zero_matrix(QQ,','zero_matrix(F,').replace('vector(QQ,','vector(F,')
header=r'''from sage.all import *
import pickle,time
F=QuadraticField(286,'b',embedding=AA(286).sqrt());b=F.gen();R=PolynomialRing(F,'x');x=R.gen();ga=x*(x*x-4);ra=(161-6*b)/25;rb=(161+6*b)/25;A=x-ra;B=x-rb;P=ga*A;Q=ga*B;E=F(1);D=P*Q-1;ff=(x+1)*(x-1)*(x-(2+ra)/2)
ll=QQ(121)/3330*x*x+QQ(35)/333*x+QQ(1)/5;kk=(A*B*ll*ll-1)//ga;assert A*B*ll*ll-ga*kk==1
p1=A*ll;q1=-B*ll
p2=R.lagrange_polynomial([(r,kk(r)/(2*B(r))) for r in [-2,0,2]]+[(ra,-1/Q(ra))])
q2=R.lagrange_polynomial([(r,kk(r)/(2*A(r))) for r in [-2,0,2]]+[(rb,-1/P(rb))])
assert Q*p1+P*q1==0 and Q*p2+P*q2+p1*q1==-1
mom=[(ff*Q*x**j).mod(D)[7] for j in range(8)]
'''
tail=r'''w=[R.one(),(P*q1).mod(D),(P*q2).mod(D)];pq=[P,p1,p2];qq=[Q,q1,q2];Ginv=iv(mm(mul(w,mul(pq,pq))))
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
'''
src=header+body+tail
Path('workspace/agent2_gcd3_fold_transverse_generate.py').write_text(src)
exec(src)
