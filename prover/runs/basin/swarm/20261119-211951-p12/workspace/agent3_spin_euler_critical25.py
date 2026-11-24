from pathlib import Path
s=Path('workspace/agent3_posweighted25.py').read_text().split('rows=[]\nfor k,weights')[0]
exec(s)
Erow=run(24,(2,)*12)
# Preserve common prime/columns, thenmakeF momentfunc.
s=s.replace('def run(k,weights):','def runF(k,weights):').replace('b=(48-k)*pow(48,-1,P)%P','b=(-k)*pow(48,-1,P)%P').replace('(b+a-1)%P','(b-a+1)%P').replace('for m in range(1,13):','for m in range(1,1):')
exec(s)
Frow=runF(24,(2,)*12)
import pickle
pm=pickle.load(open('workspace/agent2_exact_pairing.pkl','rb'))
M=matrix(GF(P),[[GF(P)(x.numerator)/GF(P)(x.denominator) for x in row] for row in pm])
V=matrix(GF(P),[Erow,Frow]);L=V*M
print('EF rankinquotient',FZ.stack(V).rank()-FZ.rank(),'pairingrank',L.rank(),flush=True)
a=json.load(open('workspace/agent2_anomaly25.json'));arow=[int(c)%P for c in a['coefficients']]
print('EF+anomaly quotientrank',FZ.stack(V).stack(matrix(GF(P),[arow])).rank()-FZ.rank(),flush=True)
print('pairingrowsfirst',list(L[0])[:5],list(L[1])[:5],flush=True)
json.dump({'prime':P,'E':Erow,'F':Frow,'columns':cols,'pairings':[[int(x) for x in row] for row in L]},open('workspace/agent3_spin_euler_critical25.json','w'))
if Path(__file__).name=='scratchpad.py':Path('workspace/agent3_spin_euler_critical25.py').write_text(Path(__file__).read_text())
