from pathlib import Path
s=Path('record/finals.md').read_text()
code=s.split('```python\n',1)[1].split('```',1)[0]
exec(compile(code,'team_final.py','exec'))
# Independently convolve full group-ring coefficients for the witness.
cx={g:x[i] for i,O in enumerate(orbits) for g in O}
cz={g:z[i] for i,O in enumerate(orbits) for g in O}
cprod={g:0 for g in G}
for g in G:
    for h in G:
        cprod[mul(g,h)]+=cx[g]*cz[h]
assert cprod == {g:20+int(g==I) for g in G}
assert all(cx[mul(t,g)]==cx[mul(g,t)] for g in G)
assert all(cx[inv(g)]==cx[g] for g in G)
assert all(cz[mul(t,g)]==cz[mul(g,t)] for g in G)
assert all(cz[inv(g)]==cz[g] for g in G)
assert sum(cx.values())==sum(cz.values())==49
print('Independent full group-ring witness convolution and S-membership passed.')
