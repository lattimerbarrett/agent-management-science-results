import json,z3,time
markers=json.load(open('workspace/agent2_orbit_shelling.json'))['markers']
N=8
m=z3.Int('m');a=[z3.Int('a%d'%i) for i in range(N)];b=[z3.Int('b%d'%i) for i in range(N)]
# Rank marker, same support triangular roots chosen by first eligible marker.
def rank(vec):
 out=z3.IntVal(999)
 for p,M in reversed(list(enumerate(markers))):
  supp=M[1:] if M[0]=='e' else M[1:4]
  cond=z3.And(*[(vec[i]>0 if i in supp else vec[i]==0) for i in range(N)])
  if M[0]=='t':cond=z3.And(cond,vec[M[4]]>=2)
  out=z3.If(cond,p,out)
 return out

def markedcount(vec,r):
 out=z3.IntVal(0)
 for p,M in reversed(list(enumerate(markers))):
  if M[0]=='t':out=z3.If(r==p,vec[M[4]],out)
 return out

def lexearlier(x,y):
 return z3.Or(*[z3.And(*[x[j]==y[j] for j in range(i)],x[i]>y[i]) for i in range(N)])

def earlier(x,y,rx=None,ry=None):
 if rx is None:rx=rank(x)
 if ry is None:ry=rank(y)
 cx=markedcount(x,rx);cy=markedcount(y,ry)
 return z3.Or(rx<ry,z3.And(rx==ry,z3.Or(cx>cy,z3.And(cx==cy,lexearlier(x,y)))))
ra=rank(a);rb=rank(b)
s=z3.Solver();s.set(timeout=300000)
s.add(m>=2,*[z3.And(x>=0,x<=m) for x in a+b],z3.Sum(a)==m+2,z3.Sum(b)==m+2,ra<999,rb<999,earlier(b,a,rb,ra))
flags=[]
for c in range(N):
 disj=[]
 for h in range(N):
  if h==c:continue
  v=[a[i]+(1 if i==h else 0)-(1 if i==c else 0) for i in range(N)]
  rv=rank(v)
  disj.append(z3.And(a[c]>0,a[h]<m,rv<999,earlier(v,a,rv,ra)))
 flag=z3.Or(*disj);flags.append(flag)
 s.add(z3.Implies(flag,b[c]>=a[c]))
print('built',flush=True);t=time.time();ans=s.check();print(ans,time.time()-t,flush=True)
if ans==z3.sat:
 model=s.model();print('m',model.eval(m),'a',[model.eval(x) for x in a],'b',[model.eval(x) for x in b],'ra',model.eval(ra),'rb',model.eval(rb),'flags',[model.eval(f) for f in flags],flush=True)
with open('scratchpad.py') as src,open('workspace/agent3_symbolic_marker.py','w') as dst:dst.write(src.read())
json.dump({'result':str(ans),'seconds':time.time()-t},open('workspace/agent3_symbolic_marker_result.json','w'))
