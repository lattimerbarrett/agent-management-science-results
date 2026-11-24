import sys,json,pathlib
sys.path.insert(0,'workspace')
from agent1_topform_gluing import top_transvections
D=json.load(open('workspace/agent4_triorthogonal40_walk.json'))['aperiodic'];out=[];seeds=[]
for i,d in enumerate(D):
 O,st=top_transvections(d['support'],10);out.append({'source':i,'stats':st});seeds +=[dict(s,source=i) for s in O]
json.dump({'stats':out,'seeds':seeds},open('workspace/agent1_topform_gluing80_all30.json','w'));pathlib.Path('workspace/agent1_topform_gluing80_all30.py').write_text(pathlib.Path(__file__).read_text());print('TOTAL',len(seeds))
