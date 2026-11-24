import z3 as z,time,json
u,t,ss=z.Reals('u sqrt3 s')
x=z.Reals('x0 x1 x2');q=z.Reals('q0 q1 q2')
p=[[z.Real('p%d%d'%(i,j)) if i!=j else z.RealVal(0) for j in range(3)] for i in range(3)]
a=u*u;b=1+2*a-4*u*t/3
S=z.SolverFor('QF_NRA');S.set(timeout=170000)
S.add(t>0,t*t==3,u>=t/6,u<=4*t/3-2,ss>=0,ss<=a,sum(x)+ss==1)
S.add(*[xx>=0 for xx in x]);S.add(*[z.And(qq>=0,qq<=1) for qq in q]);S.add(*[z.And(p[i][j]>=0,p[i][j]<=1) for i in range(3) for j in range(3) if i!=j])
S.add(ss+sum(x[i]*q[i]*q[i] for i in range(3))<=a)
for i in range(3):
 S.add(sum(x[k]*(1-p[i][k])**2 for k in range(3))+ss*(1-q[i])**2<b)
 for j in range(i):S.add(sum(x[k]*p[i][k]*p[j][k] for k in range(3))+ss*q[i]*q[j]<=a)
start=time.time();ans=S.check();print('ANSWER',ans,'time',time.time()-start,flush=True)
if ans==z.sat:print(S.model())
else:print(S.reason_unknown())
