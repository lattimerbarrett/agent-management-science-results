from pathlib import Path
p=Path('workspace/agent2_C11_local_distances.py');src=p.read_text().replace('mi=220;partial=[220]*56\n  for mask in range(57,','mi=1024;partial=[]\n  for mask in range(1,');p.write_text(src)
import pickle,itertools,time,json
D=pickle.load(open('workspace/agent2_C11_local_data.pkl','rb'));rows=D['rows'];bas={}
for x,row in enumerate(rows):
 if x.bit_count()<=5:continue
 while row:
  p=row.bit_length()-1
  if p not in bas:bas[p]=row;break
  row^=bas[p]
H=list(bas.values());cols=[sum(((r>>i)&1)<<j for j,r in enumerate(H)) for i in range(94)];tab={0:0};hits=set();t=time.time()
for k in range(1,4):
 for inds in itertools.combinations(range(1,94),k):
  syn=0;mask=0
  for i in inds:syn^=cols[i];mask^=1<<i
  if syn in tab and tab[syn]!=mask:hits.add(mask^tab[syn])
  if syn^cols[0] in tab:hits.add(mask^tab[syn^cols[0]]^1)
  tab[syn]=mask
print('triples',len(tab),'hits',len(hits),'time',time.time()-t,flush=True)
for inds in itertools.combinations(range(1,94),4):
 syn=cols[inds[0]]^cols[inds[1]]^cols[inds[2]]^cols[inds[3]]
 for bit in (0,1):
  target=syn^(cols[0] if bit else 0)
  if target in tab:
   mask=sum(1<<i for i in inds)^tab[target]^bit
   if mask:hits.add(mask)
print('DONE','hits',len(hits),'time',time.time()-t,flush=True)
print('WORDS',[[i for i in range(94) if mask>>i&1] for mask in hits][:30],flush=True)
json.dump([hex(h) for h in hits],open('workspace/agent2_C11_D5_smallwords.json','w'))
Path('workspace/agent2_C11_D5_MITM.py').write_text(Path('scratchpad.py').read_text())
