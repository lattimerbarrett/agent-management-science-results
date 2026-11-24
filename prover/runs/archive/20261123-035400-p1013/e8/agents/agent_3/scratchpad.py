import runpy,time
for f in ['agent3_tensor_checks.py','agent3_r2_realizer.py','agent3_r2_cycles.py','agent3_edge_optimization_checks.py']:
 print('\nRUN',f,flush=True);runpy.run_path('workspace/'+f,run_name='__main__')
print('ALL AGENT3 SHARED SCRIPTS RERUN AND PASSED')