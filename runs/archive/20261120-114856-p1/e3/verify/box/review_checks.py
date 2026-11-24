from pathlib import Path
for name in ('agent_1','agent_2','agent_3','agent_4'):
    p=Path('record/transcripts')/(name+'.md')
    lines=p.read_text().splitlines()
    print('\n===',name,'lines',len(lines),'LAST 35 LINES ===')
    print('\n'.join(f'{i+1}\t{lines[i]}' for i in range(max(0,len(lines)-35),len(lines))))
print('\n=== RERUN s1 EXACT CHECKS (output write omitted) ===')
p=Path('workspace/s1_check_agent2.py')
source=p.read_text().split("Path('workspace/s1_check_agent2.py').write_text")[0]
exec(compile(source,str(p),'exec'),{})
