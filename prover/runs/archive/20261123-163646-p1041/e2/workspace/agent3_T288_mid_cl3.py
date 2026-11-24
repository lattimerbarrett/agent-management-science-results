import json,pathlib,sys,collections,time
sys.path.insert(0,'workspace');from agent3_graph_lifts import veronese;from agent3_lift_closure import closure
raw=json.loads(pathlib.Path('workspace/agent3_T288_mid_actual.json').read_text())['results'];vv=veronese(9,3)
res=[];hist=collections.Counter();t=time.time()
for obj in raw:
 E,_=closure(obj['base'],vv);hist[len(E)]+=1
 if E:res.append({'base':obj['base'],'extra':[p for p,_ in E]})
print('hist',hist,'secs',time.time()-t)
pathlib.Path('workspace/agent3_T288_mid_cl3.json').write_text(json.dumps({'histogram':dict(hist),'nonclosed':res},indent=2))
pathlib.Path('workspace/agent3_T288_mid_cl3.py').write_text(pathlib.Path(__file__).read_text())
