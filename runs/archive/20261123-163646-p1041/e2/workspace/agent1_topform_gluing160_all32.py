import sys,json,pathlib,collections
sys.path.insert(0,'workspace');from agent1_topform_gluing import top_transvections
D=json.load(open('workspace/agent1_topform_gluing80_all30.json'))['seeds'];out=[];seeds=[]
for i,d in enumerate(D):
 O,st=top_transvections(d['support'],11,maxout=100);out.append({'source':i,'stats':st});seeds +=[dict(s,source=i) for s in O]
for g in seeds:
 S=set(g['support']);o=next(iter(S));assert not [p^o for p in S if p!=o and all((q^p^o) in S for q in S)]
json.dump({'stats':out,'seeds':seeds},open('workspace/agent1_topform_gluing160_all32.json','w'));pathlib.Path('workspace/agent1_topform_gluing160_all32.py').write_text(pathlib.Path(__file__).read_text());print('TOTAL',len(seeds),'Ksame',collections.Counter(g['samecodeK'] for g in seeds))
