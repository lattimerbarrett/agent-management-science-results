from pathlib import Path
source=Path('workspace/agent3_posweighted25.py').read_text().split('rows=[]\nfor k,weights')[0]
exec(source)
def parts(n,lo=1):
 if n==0:return [()]
 return [(i,)+p for i in range(lo,n+1) for p in parts(n-i,i)]
rows=[];labels=[]
for E in range(9):
 k=21-E
 for increments in parts(E):
  weights=tuple([2]*(14-len(increments))+[2+i for i in increments]);rows.append(run(k,weights));labels.append((k,weights))
print('ALL',len(rows),'COMBINED',FZ.stack(matrix(F,rows)).rank(),flush=True)
json.dump({'prime':P,'rows':rows,'labels':labels},open('workspace/agent3_positive_critical25.json','w'))
if Path(__file__).name=='scratchpad.py':Path('workspace/agent3_positive_critical25.py').write_text(Path(__file__).read_text())
