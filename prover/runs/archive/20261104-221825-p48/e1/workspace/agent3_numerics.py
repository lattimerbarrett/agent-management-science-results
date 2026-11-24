import os,runpy
for f in sorted(os.listdir('workspace')):
 if f.startswith(('agent2_','agent3_','agent4_')) and f.endswith('.py'):
  print('\nRUN',f); runpy.run_path('workspace/'+f)
