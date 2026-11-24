import runpy, sys
sys.dont_write_bytecode=True
runpy.run_path('experiments/e3/boundary_yamabe_verified/verify_all.py',run_name='__main__')
