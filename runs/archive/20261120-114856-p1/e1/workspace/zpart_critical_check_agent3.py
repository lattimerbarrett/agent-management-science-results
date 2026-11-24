from pathlib import Path
code=Path('workspace/zpart_counter_check_agent3.py').read_text().replace('zpart_highdegree_agent3.json','zpart_critical_agent3.json')
code=code.replace("vec=m.matrix([1]*(2*s))", "ii=D['subset'];N=m.matrix([[N[i,j] for j in ii] for i in ii]);vec=m.matrix([1]*len(ii))")
code=code.replace("rat=[(N*vec)[i]/vec[i] for i in range(2*s)]", "rat=[(N*vec)[i]/vec[i] for i in range(len(ii))]")
exec(code)
from scipy.optimize import linprog
CC=np.array([[C[i,j] for j in ii] for i in ii],float);nn=len(ii);res=linprog(np.zeros(nn),A_ub=-CC.T,b_ub=-np.ones(nn),bounds=[(1e-8,None)]*nn,method='highs');print('PRINCIPAL E',res.success)
