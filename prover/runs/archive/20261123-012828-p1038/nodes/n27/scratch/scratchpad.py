import sys,numpy as np
sys.path.insert(0,'experiments/e1')
from agent2_blocks import configuration,matrix
for m in [1,2,3,7]:
 pts=configuration(m,[-2.,-.4],0.,.5,1.,1.2,[1.4,3.])
 M=matrix(pts);target=np.zeros((len(pts)+1,len(pts)+1),complex);target[0,0]=1;target[1:,1:]=M
 print('m =',m)
 for H in [1e2,1e4,1e6]:
  ext=matrix([(-H,0j)]+pts)
  print('distance',H,'max entry discrepancy',np.max(np.abs(ext-target)),'determinant ratio',np.linalg.det(ext)/np.linalg.det(M))
