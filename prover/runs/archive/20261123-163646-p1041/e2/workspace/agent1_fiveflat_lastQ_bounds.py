import itertools,json,pathlib
D=list(range(-1,6))
def cap(d):return 0 if d<0 else 1<<d
def ok(a,b,L):return a<0 or b<0 or a+b<=L
def rowmax(L,bad=False):
 rows=[]
 for a,b,c in itertools.product(D,repeat=3):
  if not ok(a,b,L) or not ok(b,c,L):continue
  if bad and a==5:continue
  rows.append((cap(a)+cap(b)+cap(c),(a,b,c)))
 return max(rows)
pairmax=max(cap(a)+cap(b) for a,b in itertools.product(D,repeat=2) if ok(a,b,7))
r7=rowmax(7);r6=rowmax(6);bad6=rowmax(6,True)
assert pairmax==36 and r7[0]==68 and r6[0]==66 and bad6[0]==50
assert pairmax+r7[0]+32+1==137<153
assert 2*r6[0]+16+1==149<153
assert bad6[0]+r6[0]+32+1==149<153
assert 224+128-2*5==342>334
assert 192+128==320<322
for j in range(6):assert j//2<=j*(j-1)//2
r={'paircap':pairmax,'generic_H_row':r7,'cross_H_row':r6,'cross_H_badleaf_row':bad6,'contained_flat_pairtotal_bound':137,'one_small_pair_total_bound':149,'nonempty_leaftriple_weight_lower_bound':342,'empty_leaftriples_weight_upper_bound':320}
json.dump(r,open('workspace/agent1_fiveflat_lastQ_bounds.json','w'));pathlib.Path('workspace/agent1_fiveflat_lastQ_bounds.py').write_text(pathlib.Path(__file__).read_text());print(json.dumps(r,indent=2))
