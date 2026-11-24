from pathlib import Path
root=Path('experiments')
print('Team report directories available:', root.exists())
if root.exists():
    for p in sorted(root.iterdir()):
        print(p.name)
print('\nLogical audit based on the supplied reports:')
claims={
 'e1 constructs an endpoint witness':False,
 'e2 constructs an endpoint witness':False,
 'e3 constructs an endpoint witness':False,
 'scaling a witness by t in (0,1] preserves a witness':True,
 'elementary upper bound is eta <= 1/2':True,
 'latest verified result excludes eta = 1/2':True,
}
for claim,value in claims.items():
    print(f'{claim}: {value}')
print('Conclusion: G is downward closed and G is a subset of (0,1/2).')
print('Neither nonemptiness nor sup(G)=1/2 follows from those facts.')
