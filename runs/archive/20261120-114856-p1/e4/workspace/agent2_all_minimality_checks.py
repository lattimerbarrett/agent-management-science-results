from pathlib import Path
files=['agent2_s1_checks.py', 'agent2_s2_pole_checks.py', 'agent2_s2_entropy_checks.py', 'agent2_s2_external_coefficient.py']
for name in files:
    p=Path('workspace')/name
    exec(compile(p.read_text(),str(p),'exec'),{'__name__':'__main__'})
print('ALL agent2 minimality s1/s2 exact checks PASS')
