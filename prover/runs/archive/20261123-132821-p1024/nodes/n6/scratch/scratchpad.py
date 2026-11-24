from sage.all import *
F=QQ
A=LaurentSeriesRing(F,'t',default_prec=180);t=A.gen()
def successive(bs,kind):
 g=4;k=2;h=6;N=12;n=N+1
 sq=(1-t**18).sqrt(); a=-F(1)/2*t**(-h)*sq
 phi=F(bs[0])*t**-7+F(bs[1])*t**-5;q=k*t**k*phi
 P=matrix(A,n,n)
 for j in range(n):
  co=F(1)
  for l in range((N-j)//k+1):
   if l:co*= (F(j)/k+l-1)/l
   P[j+l*k,j]=t**j*co*q**l
 D=identity_matrix(A,n);C=-t**-1*identity_matrix(A,n)
 for i in range(k,n):D[i,i-k]=-q;C[i,i-k]=-t**k*phi.derivative()
 if kind=='O':T=P;degrees=list(range(n))
 elif kind=='L':T=a*D*P;degrees=[i-h for i in range(n)]
 else:
  old=block_matrix([[a*P,zero_matrix(A,n,n)],[a*C*P,D*P]])
  order=sum(([i,n+i] for i in range(n)),[])
  T=old.matrix_from_rows_and_columns(order,order)
  degrees=sum(([i-h,i] for i in range(n)),[])
 # current columns are actual global sections, entries expansions of U coefficients.
 secs=matrix(A,0,0); hist=[];chi=0
 for row,deg in enumerate(degrees):
  dim=secs.ncols(); diag=T[row,row]
  cs=[sum((T[row,j]*secs[j,l] for j in range(row)),A(0))/diag for l in range(dim)]
  low=min([int(c.valuation()) for c in cs if c]+[0,-max(deg,0)])
  pole=max(0,-low)
  inds=[s for s in range(pole+1) if s%2==0 or s>=9]
  fs=[t**(-s)*(sq if s%2 else 1) for s in inds]
  vals=cs+fs
  lo=min(low,0);hi=-deg
  M=matrix(F,max(0,hi-lo),len(vals),lambda i,j:vals[j][lo+i])
  K=M.right_kernel().basis_matrix().transpose()
  ns=matrix(A,row+1,K.ncols())
  for i in range(row):
   for l in range(K.ncols()):ns[i,l]=sum((secs[i,j]*K[j,l] for j in range(dim)),A(0))
  for l in range(K.ncols()):ns[row,l]=sum((fs[j]*K[dim+j,l] for j in range(len(fs))),A(0))
  secs=ns;chi+=deg+1-g
  if kind!='S' or row%2==1:hist.append(secs.ncols()-chi)
 return secs.ncols()-chi,hist
for bs in [[1,0],[0,1]]:
 print('b=',bs,flush=True)
 results=[]
 for kind in ['O','S','L']:
  v,history=successive(bs,kind);results.append(v)
  print(kind,v,history,flush=True)
 print('delta=',results[0]-results[1]+results[2],flush=True)
