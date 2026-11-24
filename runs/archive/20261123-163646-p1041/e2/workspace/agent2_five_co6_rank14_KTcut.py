import itertools,z3,time,json,pathlib
n=5;E=1<<n;NN=1<<(n+1);r=[z3.Int('r%d'%i) for i in range(NN)];s=z3.Solver();s.set(timeout=120000);s.add(r[0]==0,r[E]==1)
for x in r:s.add(x>=0,x<=15)
for i in range(n):s.add(r[1<<i]==8,r[(1<<i)|E]==9)
for A in range(NN):
 for B in range(A,NN):
  if A&B==A:s.add(r[A]<=r[B])
  s.add(r[A]+r[B]>=r[A|B]+r[A&B])
ing=0
for assign in itertools.product(range(6),repeat=n+1):
 parts=[sum(1<<i for i,a in enumerate(assign) if a==j) for j in range(5)]
 T,A,B,C,D=parts
 if not A or not B or not C or not D:continue
 s.add(r[A|B|T]+r[A|C|T]+r[A|D|T]+r[B|C|T]+r[B|D|T]>=r[A|T]+r[B|T]+r[C|D|T]+r[A|B|C|T]+r[A|B|D|T]);ing+=1
it=lambda S:15-r[S]
for ids in itertools.permutations(range(n)):
 a,b,c,d,e=[1<<i for i in ids];base=it(a|b)+it(a|c)+it(b|c)-it(a|b|c)
 for x,y in itertools.combinations([a,b,c],2):
  more=it(x|d)+it(y|d)-it(x|y|d)
  for u,v in itertools.combinations([a,b,c,d],2):s.add(base+more+it(u|e)+it(v|e)-it(u|v|e)<=20)
pairs=list(itertools.combinations(range(n),2))
for i,j in pairs:
 P=(1<<i)|(1<<j);s.add(z3.Implies(r[P|E]==r[P]+1,r[P|E]>=11))
def pw(d):return z3.Sum([z3.If(d==j,1<<j,0) for j in range(7)])
def weight(J):
 ans=64*len(J)
 for k in range(2,len(J)+1):
  for ids in itertools.combinations(J,k):
   P=sum(1<<i for i in ids);ans+=(-2)**(k-1)*z3.If(r[P|E]==r[P]+1,pw(15-r[P|E]),0)
 return ans
for k in [3,4]:
 for ids in itertools.combinations(range(n),k):
  v=weight(ids);s.add(z3.Or([v==w for w in [0,64,96,112,120,124,126]]+[v>=128]))
for ids in itertools.combinations(range(n),4):s.add(weight(ids)>=128)
w=weight(range(n));out=[]
for target in [152,154,156]:
 ss=z3.Solver();ss.add(s.assertions());ss.add(w==target);ss.set(timeout=60000);t=time.time();ans=ss.check();D={'target':target,'answer':str(ans),'seconds':time.time()-t}
 if ans==z3.sat:
  M=ss.model();D['ranks']={str(i):M.eval(r[i]).as_long() for i in range(NN)}
 out.append(D);print(D,flush=True)
json.dump(out,open('workspace/agent2_five_co6_rank14_KTcut.json','w'))
