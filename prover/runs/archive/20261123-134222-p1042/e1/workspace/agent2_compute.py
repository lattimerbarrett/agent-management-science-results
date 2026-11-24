import itertools as it, math, pickle, os, time
from collections import defaultdict

def make_complex(m):
 r=m-5
 cells=[]; ids=[]
 for k in range(5):
  cc=[]
  for cols in it.combinations(range(m),k):
   for rows in it.product(range(3),repeat=k):
    if any(rows.count(i)>2 for i in range(3)): continue
    f=tuple(zip(cols,rows)); rem=tuple(j for j in range(m) if j not in cols); a=rem[-1]
    for s in it.combinations(rem[:-1],r): cc.append((f,s))
  cells.append(cc); ids.append({x:i for i,x in enumerate(cc)})
 ds=[None]
 for k in range(1,5):
  D={}
  for c,(f,s) in enumerate(cells[k]):
   olda=max(set(range(m))-{x for x,y in f})
   for p,(x,y) in enumerate(f):
    ff=f[:p]+f[p+1:]; newa=max(set(range(m))-{xx for xx,yy in ff}); sign=(-1)**p
    terms={s:1}
    if newa!=olda:
     # wedge_i (v_i-v_olda); sorted s. At most one factor olda.
     for q in range(r):
      raw=s[:q]+(olda,)+s[q+1:]
      inv=sum(raw[i]>raw[j] for i in range(r) for j in range(i+1,r))
      ss=tuple(sorted(raw)); terms[ss]=terms.get(ss,0)-(-1)**inv
    for ss,coef in terms.items():
     if coef: D[(ids[k-1][(ff,ss)],c)]=sign*coef
  ds.append(D)
 return cells,ds

def check(ds):
 for k in range(2,5):
  a=defaultdict(list)
  for (i,j),v in ds[k-1].items(): a[j].append((i,v))
  z=defaultdict(int)
  for (j,l),w in ds[k].items():
   for i,v in a[j]: z[i,l]+=v*w
  assert not any(z.values()),k

def reduce_units(D,nrow,ncol,active_rows=None):
 # dictionaries indexed by rows and columns; cancel first minimal-degree unit row.
 R={i:{} for i in range(nrow) if active_rows is None or i in active_rows}; C={j:{} for j in range(ncol)}
 for (i,j),v in D.items():
  if i in R: R[i][j]=v; C[j][i]=v
 count=0
 while True:
  opts=((len(row),i,next((j for j,v in row.items() if abs(v)==1),None)) for i,row in R.items())
  opts=[x for x in opts if x[2] is not None]
  if not opts: break
  _,i,j=min(opts); a=R[i][j]; rr=R[i].copy(); cc=C[j].copy()
  for ii,b in cc.items():
   if ii==i:continue
   for jj,c in rr.items():
    if jj==j:continue
    z=R[ii].get(jj,0)-b*c*a
    if z: R[ii][jj]=z; C[jj][ii]=z
    else: R[ii].pop(jj,None); C[jj].pop(ii,None)
  for jj in rr: C[jj].pop(i)
  for ii in cc: R[ii].pop(j)
  del R[i];del C[j];count+=1
 print('cancelled',count,'remaining',len(R),len(C),'nnz',sum(map(len,R.values())), 'entries',sorted(set(v for rr in R.values() for v in rr.values()))[:20],flush=True)
 return R,C

def main(m):
 t=time.time(); cells,ds=make_complex(m);print('m',m,'sizes',list(map(len,cells)),flush=True);check(ds);print('chain checked',time.time()-t,flush=True)
 active=None; results=[]
 for k in range(1,5):
  R,C=reduce_units(ds[k],len(cells[k-1]),len(cells[k]),active)
  results.append((R,C));active=set(C)
  assert k==4 or not any(R.values())
 print('time',time.time()-t,flush=True)
 os.makedirs('workspace',exist_ok=True)
 with open(f'workspace/agent2_reduction_m{m}.pickle','wb') as f:pickle.dump(results,f)
def make_A(p):
 cells=[]; ids=[]
 for k in range(7):
  cc=[]
  for cols in it.combinations(range(p),k):
   for rows in it.product(range(3),repeat=k):
    if all(rows.count(i)<=2 for i in range(3)): cc.append(tuple(zip(cols,rows)))
  cells.append(cc);ids.append({f:i for i,f in enumerate(cc)})
 ds=[None]
 for k in range(1,7):
  D={}
  for j,f in enumerate(cells[k]):
   for i in range(k):D[ids[k-1][f[:i]+f[i+1:]],j]=(-1)**i
  ds.append(D)
 return cells,ds

def compute_A(p):
 cells,ds=make_A(p);print('A',p,'sizes',list(map(len,cells)),flush=True)
 active=None; out=[]
 for k in range(1,7):
  R,C=reduce_units(ds[k],len(cells[k-1]),len(cells[k]),active)
  out.append((R,C));active=set(C)
  if any(R.values()):break
 with open(f'workspace/agent2_A{p}.pickle','wb') as f:pickle.dump(out,f)

def residual_smith(m):
 from sage.all import matrix, ZZ
 with open(f'workspace/agent2_reduction_m{m}.pickle','rb') as f: R,C=pickle.load(f)[-1]
 rows=list(R);cols=list(C);ci={j:k for k,j in enumerate(cols)}
 M=matrix(ZZ,len(rows),len(cols),{(i,ci[j]):v for i,r in enumerate(rows) for j,v in R[r].items()},sparse=False)
 S=M.smith_form(transformation=False);diag=[S[i,i] for i in range(min(S.dimensions())) if S[i,i]]
 from collections import Counter
 print('m',m,'residual dimensions',M.dimensions(),'Smith nonzeros',Counter(diag),'free H3',len(rows)-len(diag),'free H4',len(cols)-len(diag),flush=True)
 return (m,dict(Counter(map(int,diag))),len(rows)-len(diag),len(cols)-len(diag))

if __name__=='__main__':
 for m in range(7,12):residual_smith(m)
 with open('workspace/agent2_compute.py','w') as f:f.write(open(__file__).read())
