from pathlib import Path
checks=['agent3_transall.py','agent3_flat_base.py','agent3_pohozaev_identity.py','agent3_mass_rim.py','agent1_linear_stress_rim.py','agent2_dilation_rim.py','agent1_exact_finite_minima.py']
for file in checks:
 p=Path('workspace')/file
 print('\n===',file,flush=True)
 exec(compile(p.read_text(),str(p),'exec'),{'__name__':'__main__','__file__':str(p)})
