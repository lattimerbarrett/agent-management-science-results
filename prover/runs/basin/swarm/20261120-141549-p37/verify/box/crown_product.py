exec(open('interval_product.py').read().split('S=list(')[0])
for m in [4,5,6,7]:
 S=list(itertools.product(range(2),range(m)))
 sl=lambda x,y:x==y or (x[0]==0 and y[0]==1 and x[1]!=y[1])
 for n in [4,5,6]:
  Q=list(itertools.product(range(2),range(n)))
  ql=lambda x,y:x==y or (x[0]==0 and y[0]==1 and y[1] in [x[1],(x[1]+1)%n])
  E=list(itertools.product(S,Q));print('m,n',m,n,flush=True)
  ans,rr=solve(E,lambda a,b:sl(a[0],b[0]) and ql(a[1],b[1]),m,5000)
