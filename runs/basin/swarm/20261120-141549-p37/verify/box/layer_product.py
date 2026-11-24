exec(open('interval_product.py').read().split('S=list(')[0])
import random
random.seed(483)
S=list(itertools.product(range(2),range(3)))
sl=lambda x,y:x==y or (x[0]==0 and y[0]==1 and x[1]!=y[1])
count=0
for trial in range(300):
 n=15;p=random.uniform(.2,.6)
 M=[[i==j or (i//5<j//5 and random.random()<p) for j in range(n)] for i in range(n)]
 for k in range(n):
  for i in range(n):
   for j in range(n):M[i][j]|=M[i][k] and M[k][j]
 Q=list(range(n));ql=lambda x,y:M[x][y]
 # quiet solve dim3
 cp,cover,lo,up=data(Q,ql)
 so=z3.Solver();so.set(timeout=1000);rr=[[z3.Int(f'z{k}_{i}') for i in range(n)] for k in range(3)]
 for row in rr:so.add([row[i]<row[j] for i,j in cover])
 for i,j in cp:so.add(z3.Or([row[i]>row[j] for row in rr]))
 if so.check()!=z3.unsat:continue
 count+=1;print('trial',trial,'number',count,flush=True)
 a,r=solve(Q,ql,4,1000)
 if a!='sat':continue
 E=list(itertools.product(S,Q));ans,rr=solve(E,lambda a,b:sl(a[0],b[0]) and ql(a[1],b[1]),4,5000)
 if ans=='sat':
  json.dump({'mat':M,'ranks':rr},open('layer_counterexample.json','w'));break
 if count>=30:break
