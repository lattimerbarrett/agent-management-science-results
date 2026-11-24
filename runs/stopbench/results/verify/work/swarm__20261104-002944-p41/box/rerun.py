import sys,runpy,time
sys.path.insert(0,'/mnt/workspace')
sys.path.insert(0,'workspace')
t=time.time()
runpy.run_path('workspace/agent1_complete_proof.py',run_name='__main__')
print('elapsed',time.time()-t)
