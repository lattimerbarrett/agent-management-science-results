from scipy.optimize import linprog
import numpy as np
for L in [8,10,12,14]:
 A=[]
 for i in range(L):
  row=[0]*L;row[(i-1)%L]=-1;row[(i+1)%L]=-1;A.append(row)
 c=np.zeros(L);c[0]=c[L//2]=-1
 r=linprog(c,A_ub=A,b_ub=[-.2]*L,A_eq=[[1]*L],b_eq=[1],bounds=(0,None),method='highs')
 print(L,r.success, -r.fun if r.success else None,r.x if r.success else None)
