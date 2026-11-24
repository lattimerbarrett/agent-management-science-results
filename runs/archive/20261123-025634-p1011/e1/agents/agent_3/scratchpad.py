from pathlib import Path
for name in ['agent3_harmonic_translation_checks.py','agent3_critical_exponent_checks.py','agent3_boundary_graph_check.py','agent3_translation_hessian.py']:
 print('\nRUN',name)
 p=Path('workspace')/name
 exec(compile(p.read_text(),str(p),'exec'),{'__name__':'__main__','__file__':str(p)})