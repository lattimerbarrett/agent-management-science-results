import json,sys,pathlib,collections
sys.path.insert(0,'workspace')
from agent3_lift_closure import closure,veronese
D=json.load(open('workspace/agent1_boundary272_relatives.json'))
R=[]
for i,a in enumerate(D['seeds']):
 S=a['support'];X,r=closure(S,veronese(11,3));X5,r5=closure(S,veronese(11,5));assert not X;assert not X5
 R.append({'type':a['type'],'Q':a['Q'],'K5':len(S)-r5,'cl3extras':len(X),'cl5extras':len(X5)})
print(collections.Counter((a['K5'],a['cl3extras'],a['cl5extras']) for a in R))
json.dump(R,open('workspace/agent1_boundary272_closure_audit.json','w'))
pathlib.Path('workspace/agent1_boundary272_closure_audit.py').write_text(pathlib.Path(__file__).read_text())
