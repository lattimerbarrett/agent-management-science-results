from pathlib import Path
for agent in range(1,5):
    p=Path(f'record/transcripts/agent_{agent}.md')
    # The sandbox may not expose record; checking scripts below suffices.
    if p.exists():
        lines=p.read_text().splitlines()
        print(f'=== agent_{agent}, last transcript lines ({len(lines)} total) ===')
        print('\n'.join(lines[-22:]))
print('=== central partial certificate (output writes removed) ===')
p=Path('workspace/a1_central_all_but_four.py')
s=p.read_text().splitlines()
exec(compile('\n'.join(s[:47]),str(p),'exec'), {'__name__':'__main__'})
print('=== exceptional constructions ===')
p=Path('workspace/agent3_low.py')
exec(compile(p.read_text(),str(p),'exec'), {'__name__':'__main__'})
