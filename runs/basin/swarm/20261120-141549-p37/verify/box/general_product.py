exec(open('random_product.py').read().split('count=0')[0])
count=0
for trial in range(1000):
 n=12
 ranks=[]
 for k in range(4):
  order=list(range(n));random.shuffle(order);ranks.append([order.index(i) for i in range(n)])
 mat=[[all(row[i]<=row[j] for row in ranks) for j in range(n)] for i in range(n)]
 ans,_=solve(mat,3)
 if ans!='unsat':continue
 count+=1
 E=list(itertools.product(range(6),range(n)))
 pm=[[ (a==c or (a<3 and c>=3 and a!=c-3)) and mat[b][d] for c,d in E] for a,b in E]
 ans,rr=solve(pm,4,10000)
 print(trial,count,ans,flush=True)
 if ans=='sat':
  json.dump({'mat':mat,'ranks':rr},open('counterexample.json','w'));break
 if count>=50:break
print('finished',count)
