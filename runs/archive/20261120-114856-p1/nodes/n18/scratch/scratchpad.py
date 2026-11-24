from pathlib import Path
base=Path('experiments')
print('Workspace availability:', base.exists())
for eid, names in [('e1',['s1_proof_agent2.md']),('e2',['agent1_s2_proof.md','agent1_polynomial_convergence.md'])]:
    for name in names:
        matches=list((base/eid).rglob(name)) if (base/eid).exists() else []
        for p in matches:
            print('\nFILE:',p)
            text=p.read_text()
            print(text[:26000])
        if not matches: print('Not available:',eid,name)
