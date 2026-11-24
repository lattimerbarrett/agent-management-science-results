import sympy as S, itertools, random, json
x,y,z=S.symbols('x y z')
I=S.eye(2);X=S.Matrix([[0,1],[1,0]]);Z=S.diag(1,-1)
G=[S.kronecker_product(X,I),S.kronecker_product(Z,X),S.kronecker_product(Z,Z)]
random.seed(123)
for trial in range(1000):
 mats=[]
 for k in range(4):
  D=S.zeros(4)
  for i in range(4):
   for j in range(i,4):D[i,j]=D[j,i]=random.randint(-2,2)
  D-=S.eye(4)*S.trace(D)/4
  mats.append(D)
 M=mats[3]+x*mats[0]+y*mats[1]+z*mats[2]
 polys=list(set(S.expand(M.extract(r,c).det()) for r in itertools.combinations(range(4),3) for c in itertools.combinations(range(4),3)))
 print('trial',trial,flush=True)
 g=S.groebner(polys,x,y,z)
 ints=S.polys.polytools.intervals(g.polys[-1].as_expr(),eps=S.Rational(1,1000))
 print('real count',len(ints),'degree',g.polys[-1].total_degree(),flush=True)
 if not ints:
  print('MATS',mats,flush=True)
  print(g,flush=True)
  for p in g.polys:print(p.as_expr(),flush=True)
  import pickle
  with open('workspace/no_rank2_agent3.pkl','wb') as f:pickle.dump((mats,g),f)
  break
