import z3 as Z
from itertools import combinations

def det(M):
 n=len(M)
 if n==1:return M[0][0]
 return sum((-1)**j*M[0][j]*det([row[:j]+row[j+1:] for row in M[1:]]) for j in range(n))

def problem(fixed=True,timeout=120000):
 S=Z.SolverFor('QF_NRA');S.set(timeout=timeout)
 def R(name):return Z.Real(name)
 h,p,r,c=map(R,['h','p','r','c'])
 a=p*p/3;s=1-r
 S.add(h*h==3,h>0,p>=Z.RealVal('1/2'),p<=h/3,r>0,r<=a,c>Z.RealVal('1/2'),c>4*p/3-2*p*p/3,c>2*p/h-p*p/3,c<=1)
 if fixed:S.add(p==Z.RealVal('13/25'),r==Z.RealVal('3/100'))
 theta=[R(f't{i}') for i in range(3)]
 S.add(sum(theta)==s,*[t>=0 for t in theta])
 db=[0]*3;qb=[0]*3;gb={(i,j):0 for i,j in combinations(range(3),2)}
 def moment(mass,ids,label):
  n=len(ids);means=[R(f'm{label}_{i}') for i in ids]
  G=[[None]*n for _ in range(n)]
  for i in range(n):
   S.add(means[i]>=0,means[i]<=mass)
   for j in range(i,n):
    G[i][j]=G[j][i]=R(f'g{label}_{ids[i]}{ids[j]}')
    S.add(G[i][j]>=0,G[i][j]<=means[i],G[i][j]<=means[j])
  M=[[mass]+means]+[[means[i]]+G[i] for i in range(n)]
  for k in range(2,n+2):
   for I in combinations(range(n+1),k):S.add(det([[M[i][j] for j in I] for i in I])>=0)
  return means,G
 for j in range(3):
  ids=[i for i in range(3) if i!=j];m,G=moment(theta[j],ids,f'b{j}')
  for pos,i in enumerate(ids):db[i]+=m[pos];qb[i]+=G[pos][pos]
  gb[tuple(ids)]=G[0][1]
 dr,GR=moment(r,list(range(3)),'R')
 for i in range(3):S.add(qb[i]+GR[i][i]-2*(db[i]+dr[i])+c<=0)
 for i,j in combinations(range(3),2):S.add(gb[i,j]+GR[i][j]<=a)
 S.add(sum(theta[i]*GR[i][i] for i in range(3))<=r*(a-r))
 return S
if __name__=='__main__':
 S=problem(True)
 print('constraints',len(S.assertions()),flush=True)
 print(S.check(),flush=True)
 if S.check()==Z.sat:print(S.model())
