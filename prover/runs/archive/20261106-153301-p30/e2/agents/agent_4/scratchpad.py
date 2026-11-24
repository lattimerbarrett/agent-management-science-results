import runpy
for fn in ['workspace/agent4_upper_parity.py','workspace/agent3_explicit_separator.py','workspace/agent2_gaussian_lower.py']:
 print('\nINDEPENDENT RERUN',fn,flush=True)
 runpy.run_path(fn,run_name='__main__')
