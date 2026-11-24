import pickle,sympy as S,time,itertools
D=pickle.load(open('workspace/agent3_ch232_general.pkl','rb'))
us=D['vars'];a,b,c,d,e=us
p=32003
polys=[]
for eq in D['equations']:
 P=S.Poly(eq,*us).clear_denoms()[1]
 polys.append((P.total_degree(),{m:int(co)%p for m,co in P.terms()}))
def mons(deg,n=5):
 if n==1:
  for j in range(deg+1):yield (j,)
 else:
  for j in range(deg+1):
   for tail in mons(deg-j,n-1):yield (j,)+tail

def key(m):return (sum(m),m)

def reduce(row,basis):
 while row:
  m=max(row,key=key)
  if m not in basis:return row
  f=row[m]
  for n,v in basis[m].items():
   z=(row.get(n,0)-f*v)%p
   if z:row[n]=z
   elif n in row:del row[n]
 return row
for bound in range(6,12):
 start=time.time();basis={};nr=0
 for degree,poly in polys:
  for mon in mons(bound-degree):
   row={tuple(x+y for x,y in zip(m,mon)):co for m,co in poly.items()}
   row=reduce(row,basis)
   if row:
    m=max(row,key=key);iv=pow(row[m],-1,p)
    basis[m]={n:co*iv%p for n,co in row.items()}
   nr+=1
  target={(2,0,0,0,0):1,(1,0,0,1,0):1}
  rem=reduce(target,basis)
  if not rem:break
 print('bound',bound,'rows',nr,'rank',len(basis),'target remainder',rem,'time',time.time()-start,flush=True)
 if not rem:
  pickle.dump((bound,basis),open('workspace/agent4_232_macmod.pkl','wb'));break
