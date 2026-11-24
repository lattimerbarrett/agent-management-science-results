from pathlib import Path
p=Path('workspace/agent4_pachner_search.py').read_text();prefix=p[:p.index('n=12;')]
main='''n=12;universe=[sum(1<<v for v in cc) for cc in combinations(range(n),4)]
ed=[(1<<i)|(1<<((i+1)%n)) for i in range(n)]
fs={a|b for a,b in combinations(ed,2) if not a&b}
start=time.time();seen=set();scanned=0;nonVD=0;steps=0
while time.time()-start<100:
 choices=moves(fs)
 up=[c for c in choices if len(c[1])>len(c[0])]
 if up:choices=up
 if not choices:break
 old,new=random.choice(choices);gs=(fs-set(old))|set(new)
 yes=test(gs,1,.2)
 if yes:fs=gs;steps+=1
 edges={h for g in fs for h in submasks(g,2)}
 if len(edges)!=n*(n-1)//2:continue
 key=tuple(sorted(fs))
 if key in seen:continue
 seen.add(key);scanned+=1
 tri={h for g in fs for h in submasks(g,3)}
 sat={g for g in universe if all(h in tri for h in submasks(g,3))}
 if test(sat,0,.2) is not False:continue
 nonVD+=1
 legal=[]
 for g in universe:
  if g in sat:continue
  if sum(h in tri for h in submasks(g,3))==3:legal.append(g)
 good=False;known=True
 for g in legal:
  yes=test(sat|{g},1,.5)
  if yes:good=True;break
  if yes is None:known=False;break
 print('nonVDneighborly',nonVD,'satfacets',len(sat),'legal',len(legal),'goodfound',good,'known',known,flush=True)
 if known and not good:
  Path('workspace/a4_neighborly_trap.json').write_text(json.dumps(sorted(sat)));print('TRUE OBSTRUCTION',flush=True);break
print('done steps',steps,'neighborly',scanned,'nonVD',nonVD,'time',time.time()-start,flush=True)
'''
Path('workspace/agent4_neighborly_search.py').write_text(prefix+main)
exec(compile(prefix+main,'workspace/agent4_neighborly_search.py','exec'))
