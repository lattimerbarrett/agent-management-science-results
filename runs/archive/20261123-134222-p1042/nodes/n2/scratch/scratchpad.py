import pickle,heapq,time

def rank_mod(mat,nrows,p):
 cols=[{i:v%p for i,v in c.items() if v%p} for c in mat]
 rows=[set() for _ in range(nrows)]
 heap=[]
 for j,c in enumerate(cols):
  for i in c:rows[i].add(j)
  if c:heapq.heappush(heap,(len(c),j))
 count=0
 while heap:
  _,j=heapq.heappop(heap);c=cols[j]
  if not c:continue
  i=min(c,key=lambda x:len(rows[x]));iv=pow(c[i],-1,p)
  for jj in list(rows[i]):
   if jj==j:continue
   cc=cols[jj];fac=cc[i]*iv%p
   for ii,w in c.items():
    z=(cc.get(ii,0)-fac*w)%p
    if z:
     if ii not in cc:rows[ii].add(jj)
     cc[ii]=z
    elif ii in cc:
     del cc[ii];rows[ii].discard(jj)
   if cc:heapq.heappush(heap,(len(cc),jj))
  for ii in c:rows[ii].discard(j)
  c.clear();count+=1
 return count
if __name__=='__main__':
 dims,mats=pickle.load(open('original7.pkl','rb'))
 for p in [2,3,5,101]:
  rr=[0]
  for q in range(1,8):
   t=time.time();r=rank_mod(mats[q],dims[q-1],p);rr.append(r)
   print('p,q,rank,time',p,q,r,round(time.time()-t,2),flush=True)
  rr.append(0)
  print('REDUCED BETTI',p,[dims[q]-rr[q]-rr[q+1] for q in range(8)],flush=True)
