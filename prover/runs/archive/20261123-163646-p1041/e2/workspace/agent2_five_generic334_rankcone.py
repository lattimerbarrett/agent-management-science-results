import itertools,z3,time,json,pathlib
n=5;E=1<<n;NN=1<<(n+1);r=[z3.Int('r%d'%i) for i in range(NN)];s=z3.Solver();s.set(timeout=120000);s.add(r[0]==0,r[E]==1)
for x in r:s.add(x>=0,x<=16)
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
it=lambda S:16-r[S]
for ids in itertools.permutations(range(n)):
 a,b,c,d,e=[1<<i for i in ids];base=it(a|b)+it(a|c)+it(b|c)-it(a|b|c)
 for x,y in itertools.combinations([a,b,c],2):
  more=it(x|d)+it(y|d)-it(x|y|d)
  for u,v in itertools.combinations([a,b,c,d],2):s.add(base+more+it(u|e)+it(v|e)-it(u|v|e)<=24)
pairs=list(itertools.combinations(range(n),2));edge={}
for i,j in pairs:
 P=(1<<i)|(1<<j);s.add(z3.Implies(r[P|E]==r[P]+1,r[P|E]>=11));edge[i,j]=r[P|E]==16
s.add(z3.Sum([z3.If(e,1,0) for e in edge.values()])>=2)
# Forbid exact3-edge triangles and four-vertex paths, established Q-normal constraints.
for es in itertools.combinations(pairs,3):
 deg=[sum(i in e for e in es) for i in range(n)];pattern=sorted(deg)
 if pattern not in [[0,0,2,2,2],[0,1,1,2,2]]:continue
 s.add(z3.Not(z3.And([edge[e] if e in es else z3.Not(edge[e]) for e in pairs])))
def pw(d):return z3.Sum([z3.If(d==j,1<<j,0) for j in range(8)])
w=640
for k in range(2,n+1):
 for ids in itertools.combinations(range(n),k):
  P=sum(1<<i for i in ids);card=z3.If(r[P|E]==r[P]+1,pw(16-r[P|E]),0);w+=(-2)**(k-1)*card
s.add(w==334);t=time.time();print('built constraints',len(s.assertions()),'Ingleton',ing,flush=True);ans=s.check();print('RESULT',ans,'seconds',time.time()-t,flush=True)
D={'answer':str(ans),'seconds':time.time()-t,'constraints':len(s.assertions()),'Ingleton':ing}
if ans==z3.sat:
 M=s.model();D['ranks']={str(i):M.eval(r[i]).as_long() for i in range(NN)};D['Qedges']=[e for e,v in edge.items() if z3.is_true(M.eval(v))];print(D,flush=True)
json.dump(D,open('workspace/agent2_five_generic334_rankcone.json','w'));pathlib.Path('workspace/agent2_five_generic334_rankcone.py').write_text(pathlib.Path(__file__).read_text())
