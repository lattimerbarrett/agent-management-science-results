import numpy as np
from scipy.sparse import csr_matrix
from scipy.optimize._highspy import _core

class PersistentLP:
 def __init__(self,n,Aub=()):
  self.H=_core._Highs();self.n=n
  for k,v in [('output_flag',False),('threads',1),('primal_feasibility_tolerance',1e-9),('dual_feasibility_tolerance',1e-9),('solver','simplex')]:self.H.setOptionValue(k,v)
  self.H.addVars(n,np.zeros(n),np.full(n,np.inf))
  self.H.addRow(1.,1.,n,np.arange(n,dtype=np.int32),np.ones(n))
  self.rows=[];self.scales=[]
  if len(Aub):self.add(Aub)
 def add(self,Aub):
  original=np.asarray(Aub)
  scale=1/np.maximum(np.max(np.abs(original),axis=1),1e-300)
  A=csr_matrix(original*scale[:,None]);m=A.shape[0]
  self.scales.extend(scale.tolist())
  self.H.addRows(m,np.full(m,-np.inf),np.zeros(m),A.nnz,A.indptr.astype(np.int32),A.indices.astype(np.int32),A.data)
  self.rows.extend(list(np.asarray(Aub)))
 def run(self):
  self.H.run();status=self.H.getModelStatus()
  if status==_core.HighsModelStatus.kOptimal:
   return True,np.array(self.H.getSolution().col_value)
  if status==_core.HighsModelStatus.kInfeasible:
   return False,None
  raise RuntimeError(self.H.modelStatusToString(status))
 def ray(self):
  status,ok,ray=self.H.getDualRay()
  if ok:ray=ray*np.array([1.]+self.scales)
  return status,ok,ray
