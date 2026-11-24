import os,sys,runpy
os.chdir('experiments/e3/boundary_yamabe_verified')
sys.path.insert(0,os.path.abspath('workspace'))
for f in ['agent2_finite_maxima_certificates.py','agent4_all_n_certificate.py','agent4_translation_ge40.py']:
 print('\nRUN',f,flush=True)
 runpy.run_path('workspace/'+f,run_name='__main__')
