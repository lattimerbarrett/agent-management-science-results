from itertools import product
import json, pathlib
P=[0]+[1<<i for i in range(8)]
possible={}
for a,b,c,t in product(P,repeat=4):
    if t>min(a,b,c): continue
    if any(x+y-t>128 for x,y in [(a,b),(a,c),(b,c)]): continue
    if t:
        da,db,dc,dt=(x.bit_length()-1 for x in [a,b,c,t])
        if any(x+y-dt>7 for x,y in [(da,db),(da,dc),(db,dc)]):continue
    elif min(a,b,c):
        da,db,dc=(x.bit_length()-1 for x in [a,b,c])
        # Directions of triple intersection have dim<=min(da,db,dc).
        # Disjoint pair intersections inside each 7-flat require
        # sum of corresponding direction dimensions minus common dim <=6.
        if max(da+db,da+dc,db+dc)-min(da,db,dc)>6:continue
    w=384-2*(a+b+c)+4*t
    possible.setdefault(w,[]).append([a,b,c,t])
assert 258 not in possible
print('Necessary cardinality/dimension constraints exclude wt258 for XOR3 affine7-flats.')
print('Permitted necessary weights256..384:',sorted(w for w in possible if 256<=w<=384))
pathlib.Path('workspace').mkdir(exist_ok=True)
pathlib.Path('workspace/agent3_triple_checks.json').write_text(json.dumps(possible))
# Save exactly this executable script for reproducibility.
pathlib.Path('workspace/agent3_triple_checks.py').write_text(pathlib.Path(__file__).read_text())
