import os,runpy,time
files=['agent3_s1_checks.py','agent3_support_splus2_check.py','agent3_reciprocal_duality_check.py','agent3_extreme_root_check.py','agent2_jacobi_middle_check.py','agent2_shear_check.py','agent3_cycle_jacobian_check.py','agent2_normalform_check.py','agent3_cubic_normal_check.py','agent4_maximal_jet_check.py','agent4_nonmax_normal_check.py','agent2_fuel_check.py','agent2_root_accel_check.py','agent4_boundary_dual_check.py','agent4_flip_logbarrier_check.py','agent2_logbarrier_check.py','agent3_fullsupport_barrier_check.py','agent4_minus_force_check.py','agent3_flip_reduce_check.py','agent4_flip_physical_check.py','agent2_s3_m5_check.py']
start=time.time()
for file in files:
 path='workspace/'+file
 if not os.path.exists(path):print('MISSING',file,flush=True);continue
 now=time.time();runpy.run_path(path,run_name='__main__');print('CHECKED',file,'time',time.time()-now,flush=True)
print('TOTAL',time.time()-start,flush=True)
