import json,pathlib
raw=json.loads(pathlib.Path('workspace/agent3_grid336_K.json').read_text())['seeds']
def val2(a):return (a&-a).bit_length()-1
hist={}
for o in raw:
 a,b,t=o['params'];va,vb=val2(a),val2(b);assert va+vb==3
 dirs=[1<<i for i in range(vb)]+[1<<(7+i) for i in range(va)];S=set(o['support'])
 assert len(dirs)==3 and all(all(x^v in S for x in S) for v in dirs)
 hist[(va,vb)]=hist.get((va,vb),0)+1
print('all',len(raw),'three-axis-period verified',hist)
pathlib.Path('workspace/agent3_grid336_period3.json').write_text(json.dumps({'count':len(raw),'histogram':{str(k):v for k,v in hist.items()}},indent=2))
pathlib.Path('workspace/agent3_grid336_period3.py').write_text(pathlib.Path(__file__).read_text())
