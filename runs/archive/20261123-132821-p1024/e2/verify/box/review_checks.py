import runpy, sys, time
sys.path.insert(0,'workspace')
for f in ['workspace/agent1_final_check.py','workspace/agent2_resonance_check.py','workspace/agent3_log_tangent_check.py','workspace/agent4_exact_cech.py']:
    t=time.time(); print('\nRUN',f,flush=True)
    runpy.run_path(f, run_name='__main__')
    print('elapsed',round(time.time()-t,3),flush=True)
