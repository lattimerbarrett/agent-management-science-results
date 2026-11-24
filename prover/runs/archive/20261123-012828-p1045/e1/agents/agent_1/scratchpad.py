import runpy,time
start=time.time();runpy.run_path('workspace/agent1_elementary_complete_checks.py',run_name='__main__');print('elapsed',time.time()-start)
