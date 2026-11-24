from pathlib import Path
import json
D=64
kt=[0,D]+[2*D-D//(2**j) for j in range(1,7)]
kt=sorted(set(x for x in kt if x<2*D))
critical=[154,162,164,166,168]
checks={}
for n in critical:
    splits=[(a,b) for a in kt for b in kt if a and b and a+b==n]
    outside=[(a,b) for a in kt for b in kt if a and b and a+b==n+2]
    assert not splits and not outside
    checks[n]={'proper_splits':splits,'outside_splits':outside,'side_upper':n+2-D}
proper160=[(a,b) for a in kt for b in kt if a and b and a+b==160]
outside160=[(a,b) for a in kt for b in kt if a and b and a+b==162]
assert proper160==[(64,96),(96,64)] and not outside160
R={'KT_weight_superset_below128':kt,'critical_core_checks':checks,'proper160':proper160,'outside160':outside160}
Path('workspace/agent4_periodic_obstructions.json').write_text(json.dumps(R,indent=2))
Path('workspace/agent4_periodic_obstructions.py').write_text(Path('scratchpad.py').read_text().split('