import os,sys,runpy
print('cwd',os.getcwd()); print(os.listdir('.'))
print('workspace',os.path.exists('workspace'))
runpy.run_path('workspace/run_final_checks.py',run_name='__main__')
