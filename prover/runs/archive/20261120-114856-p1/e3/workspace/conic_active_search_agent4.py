from pathlib import Path
src=Path('workspace/conic_search_agent4.py').read_text()
old=" if good.any():\n"
new=""" # active modes must grow incoming and decay outgoing
 for before,after,rr in [(X,Y,refs[0]),(FY,W,refs[1])]:
  active=np.array([(before@el>1e-10)&(after@el< -1e-10) for RR,bb,el in rr]).T
  slopes=np.array([bb[1]/bb[0]for RR,bb,el in rr]);slmin=np.min(np.where(active,slopes[None,:],np.inf),axis=1);slmax=np.max(np.where(active,slopes[None,:],-np.inf),axis=1)
  ds=(after[:,1]-before[:,1])/(after[:,0]-before[:,0]);good&=(active.sum(1)>=2)&(ds>slmin)&(ds<slmax)
 if good.any():
"""
src=src.replace(old,new).replace('conic_found_agent4.pkl','conic_active_found_agent4.pkl').replace('conic_search_agent4.py','conic_active_search_agent4.py')
exec(compile(src,'active','exec'))
