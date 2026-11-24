from pathlib import Path
files=['agent4_lower_checks.py','agent4_exact3_checks.py','agent2_planar_merger.py','agent3_annular_merger_checks.py','agent3_finite_chart_checks.py','agent3_analytic_bound_checks.py']
for name in files:
 p=Path('workspace')/name
 print('\nRUN',name)
 code='\n'.join(line for line in p.read_text().splitlines() if '.write_text(' not in line)
 exec(compile(code,str(p),'exec'),{'__name__':'__main__','__file__':str(p)})
print('\nALL SIX CHECK SCRIPTS PASSED')