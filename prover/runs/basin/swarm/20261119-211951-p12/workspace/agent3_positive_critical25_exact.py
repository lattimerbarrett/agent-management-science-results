from pathlib import Path
s=Path('workspace/agent3_posweighted_7over16_exact.py').read_text().split('row=run(21,(2,)*14)')[0]
exec(s)
def parts(n,lo=1):
 if n==0:return [()]
 return [(i,)+p for i in range(lo,n+1) for p in parts(n-i,i)]
rows=[];labels=[]
for E in range(9):
 k=21-E
 for inc in parts(E):
  weights=tuple([2]*(14-len(inc))+[2+i for i in inc]);rows.append(run(k,weights));labels.append((k,weights))
print('ALL67 QQ combinedrank',FZ.stack(matrix(QQ,rows)).rank(),flush=True)
import pickle
pickle.dump({'rows':rows,'labels':labels},open('workspace/agent3_positive_critical25_exact.pkl','wb'))
if Path(__file__).name=='scratchpad.py':Path('workspace/agent3_positive_critical25_exact.py').write_text(Path(__file__).read_text())
