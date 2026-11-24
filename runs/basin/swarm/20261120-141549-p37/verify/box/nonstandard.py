exec(open('random_product.py').read().split('count=0')[0])
count=0
for trial in range(2000):
 n=6
 p=random.uniform(.3,.8)
 adj=[[random.random()<p for j in range(n)] for i in range(n)]
 # exclude standard4 induced: choose 4 rows, 4 columns with exactly one 0 in each, distinct
 contains=False
 for rows in itertools.combinations(range(n),4):
  masks=[tuple(i for i in rows if not adj[i][j]) for j in range(n)]
  if all((i,) in masks for i in rows):contains=True;break
 if contains:continue
 mat=[[i==j or (i<n and j>=n and adj[i][j-n]) for j in range(2*n)] for i in range(2*n)]
 ans,_=solve(mat,3)
 if ans!='unsat':continue
 d4,_=solve(mat,4)
 if d4!='sat':continue
 count+=1
 E=list(itertools.product(range(6),range(2*n)))
 pm=[[ (a==c or (a<3 and c>=3 and a!=c-3)) and mat[b][d] for c,d in E] for a,b in E]
 ans,rr=solve(pm,4,10000)
 print(trial,count,ans,flush=True)
 if ans=='sat':
  json.dump({'mat':mat,'ranks':rr},open('counterexample.json','w'));break
 if count>=50:break
print('finished',count)
