from pathlib import Path
import time,json
src=Path('workspace/agent1_theta_test.py').read_text()
src=src.replace("print('theta relation',len(rel))",'').replace("print('FZ remainder nonzero',sum(bool(v) for v in row))",'')
src='\n'.join(line for line in src.splitlines() if not line.startswith('json.dump('))
src=src.replace('(p-q)**2','(B*p-A*q)**2')
results=[];start=time.time()
for n in range(14,27):
 for a in range(1,n//2+1):
  code=src.replace('A=B=7;',f'A={a}; B={n-a};')
  ns={};exec(compile(code,'theta_batch','exec'),ns)
  rem=sum(bool(x) for x in ns['row']);results.append([a,n-a,len(ns['rel']),rem])
  assert rem==0,(a,n-a,rem)
 print(n,'tested',len(results),'relations',round(time.time()-start,2),flush=True)
json.dump(results,open('workspace/agent1_theta_batch_results.json','w'))
