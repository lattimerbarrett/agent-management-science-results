import sage.topology as T
from pathlib import Path
print(T.__path__)
for root in T.__path__:
    for p in Path(root).glob('*.py*'):
        try:s=p.read_text(errors='ignore')
        except:continue
        lines=s.splitlines()
        for i,line in enumerate(lines):
            if any(w in line.lower() for w in ('simon','extendably','extendable shell','shelling complet')):
                print(p.name,i+1, '\n'.join(lines[max(0,i-2):i+3]))