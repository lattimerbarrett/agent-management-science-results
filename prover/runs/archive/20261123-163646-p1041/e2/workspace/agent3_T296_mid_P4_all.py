import json,pathlib,sys,collections,time
sys.path.insert(0,'workspace');from agent3_graph_lifts import veronese,kernel;from agent3_lift_closure import closure
raw=json.loads(pathlib.Path('workspace/agent3_T288_mid_cl3.json').read_text())['nonclosed'];v3=veronese(9,3);u3=veronese(10,3);u4=veronese(10,4);u5=veronese(10,5)
hist=collections.Counter();bad=[];t=time.time();n=0
for idx,obj in enumerate(raw):
 B=obj['base'];E,_=closure(B,v3);assert len(E)==4
 for p,c in E:
  H={p}|{B[j] for j in range(72) if c>>j&1};F=sorted(H|{x^512 for x in set(B)^H});assert len(F)==74
  C4,r=closure(F,u4);k4=74-r;k3=len(kernel(F,u3));k5=len(kernel(F,u5));n+=1
  hist[(len(C4),k3,k4,k5)]+=1
  if C4 or (k3,k4,k5)!=(11,1,0):bad.append({'index':idx,'point':p,'base':F,'cl4':[q for q,_ in C4],'K3':k3,'K4':k4,'K5':k5})
 if idx%3000==0:print('processed',idx,'lifts',n,'seconds',time.time()-t,flush=True)
print('TOTAL',n,'HIST',hist,'bad',len(bad),'seconds',time.time()-t)
pathlib.Path('workspace/agent3_T296_mid_P4_all.json').write_text(json.dumps({'count':n,'histogram':{str(k):v for k,v in hist.items()},'badseeds':bad},indent=2))
pathlib.Path('workspace/agent3_T296_mid_P4_all.py').write_text(pathlib.Path(__file__).read_text())
