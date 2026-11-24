from pathlib import Path
root=Path('workspace') if Path('workspace').exists() else Path('../workspace')
for name in ['agent1_checks.py','agent2_upper_checks.py','agent2_bridge_checks.py','agent3_bridge_checks.py','agent4_sign_checks.py']:
    text=(root/name).read_text()
    text='\n'.join(line for line in text.splitlines() if '.write_text(' not in line and "code=Path('scratchpad.py').read_text()" not in line)
    print('RUN',name)
    exec(compile(text,name,'exec'),{})
print('ALL RERUNS PASSED')
