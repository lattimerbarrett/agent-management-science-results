from pathlib import Path
p=Path('workspace/exterior_appendix.py');s=p.read_text()
s=s.replace('    rows=[]\n','    assert [(i,j) for i,o in enumerate(pairs) for j,v in enumerate(pairs) if set(v)<=set(o)]==[(i,i) for i in range(15)]\n    rows=[]\n')
s=s.replace('    assert S.Matrix(rows).rank()==14','    assert S.Matrix(rows).rank()==14 and S.Matrix(rows)*S.ones(15,1)==S.zeros(len(rows),1)')
s=s.replace('    assert S.expand(r[3]-s*r[2]+s*s*r[1]-s**3-c[3])==0','    assert S.expand(r[1]-3*s-c[1])==S.expand(r[2]-2*s*r[1]+3*s*s-c[2])==0\n    assert S.expand(r[3]-s*r[2]+s*s*r[1]-s**3-c[3])==0')
p.write_text(s)
p=Path('workspace/unified_full_certificate.py');s=Path('workspace/unified_incidence.py').read_text()+'\n\n'+s;p.write_text(s)
print(len(s),'bytes',len(s.splitlines()),'lines',flush=True)
exec(compile(s,str(p),'exec'),{'__name__':'__main__','__file__':str(p.resolve())})
