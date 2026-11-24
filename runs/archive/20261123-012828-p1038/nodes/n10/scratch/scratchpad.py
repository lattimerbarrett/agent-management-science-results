import importlib.util
import numpy as np
spec=importlib.util.spec_from_file_location('blocks','experiments/e1/agent2_blocks.py')
b=importlib.util.module_from_spec(spec);spec.loader.exec_module(b)
for m in [1,2,3,4,7]:
 Q=b.configuration(m,[-3.,-1.],0.,0.7,1.2,1.8,[2.5,4.])
 old=np.linalg.det(b.matrix(Q))
 print('m',m,'old determinant',old)
 for H in [10.,100.,1000.,10000.]:
  Qnew=[(-H,0j)]+Q
  new=np.linalg.det(b.matrix(Qnew))
  print('H',H,'relative change',new/old-1)
 M0=b.matrix(Q);M1=b.matrix([(-1e8,0j)]+Q)
 target=np.zeros_like(M1);target[0,0]=1;target[1:,1:]=M0
 print('max relative matrix error at H=1e8',np.max(np.abs(M1-target))/np.max(np.abs(target)))
