from pathlib import Path
p=Path('workspace/unified_incidence.py');s=p.read_text().replace(" assert p.nth(1)==-f and p.nth(2).subs(f,0)==2*c*e"," assert p.nth(1)==-f and p.nth(2).subs(f,0)==2*c*e\n assert p.nth(3).subs(f,0)==-a*e**2+2*b*c*e-c**2*d")
p.write_text(s);ns={'__name__':'audit'};exec(compile(s,str(p),'exec'),ns);ns['pencil']();print('Pencil checks passed',len(s),s.count('\n'))
