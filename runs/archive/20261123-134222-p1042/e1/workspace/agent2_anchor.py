import itertools as it, math, pickle, os, time
from collections import defaultdict

def make_complex(m,q=4,b=(2,2,2)):
 r=m-q-1
 cells=[]; ids=[]
 for k in range(q+1):
  cc=[]
  for cols in it.combinations(range(m),k):
   for rows in it.product(range(3),repeat=k):
    if any(rows.count(i)>b[i] for i in range(3)): continue
    f=tuple(zip(cols,rows)); rem=tuple(j for j in range(m) if j not in cols); a=rem[-1]
    for s in it.combinations(rem[:-1],r): cc.append((f,s))
  cells.append(cc); ids.append({x:i for i,x in enumerate(cc)})
 ds=[None]
 for k in range(1,q+1):
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
def make_A(p,b=(2,2,2)):
 cells=[]; ids=[]
 for k in range(7):
  cc=[]
  for cols in it.combinations(range(p),k):
   for rows in it.product(range(3),repeat=k):
    if all(rows.count(i)<=b[i] for i in range(3)): cc.append(tuple(zip(cols,rows)))
  cells.append(cc);ids.append({f:i for i,f in enumerate(cc)})
 ds=[None]
 for k in range(1,7):
  D={}
  for j,f in enumerate(cells[k]):
   for i in range(k):D[ids[k-1][f[:i]+f[i+1:]],j]=(-1)**i
  ds.append(D)
 return cells,ds

def compute_A(p,b=(2,2,2)):
 cells,ds=make_A(p,b);print('A',p,b,'sizes',list(map(len,cells)),flush=True)
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

def top_kernel(D,nrow,ncol,active):
 R={i:{} for i in active};C={j:{} for j in range(ncol)};V={j:{j:1} for j in range(ncol)}
 for (i,j),v in D.items():
  if i in R:R[i][j]=v;C[j][i]=v
 while True:
  opts=[(len(rr),i,next((j for j,v in rr.items() if abs(v)==1),None)) for i,rr in R.items()]
  opts=[x for x in opts if x[2] is not None]
  if not opts:break
  _,i,j=min(opts);a=R[i][j];rr=R[i].copy();cc=C[j].copy()
  for jj,c in rr.items():
   if jj==j:continue
   for z,v in V[j].items():
    vv=V[jj].get(z,0)-c*a*v
    if vv:V[jj][z]=vv
    else:V[jj].pop(z,None)
  for ii,b in cc.items():
   if ii==i:continue
   for jj,c in rr.items():
    if jj==j:continue
    z=R[ii].get(jj,0)-b*c*a
    if z:R[ii][jj]=z;C[jj][ii]=z
    else:R[ii].pop(jj,None);C[jj].pop(ii,None)
  for jj in rr:C[jj].pop(i)
  for ii in cc:R[ii].pop(j)
  del R[i];del C[j];del V[j]
 assert not any(R.values())
 return list(V.values())

def anchor_relations(n):
 from sage.all import matrix,vector,QQ,ZZ
 aa,bb=make_A(4); d3=matrix(QQ,len(aa[2]),len(aa[3]),bb[3]);d4=matrix(QQ,len(aa[3]),len(aa[4]),bb[4]);I=d4.column_space()
 z=next(z for z in d3.right_kernel().basis() if z not in I)
 mat=d4.transpose().stack(matrix(QQ,1,len(z),list(z)))
 phi=mat.solve_right(vector(QQ,[0]*d4.ncols()+[1]));phi={f:phi[j] for j,f in enumerate(aa[3]) if phi[j]}
 us=list(it.combinations(range(n),4));ui={u:i for i,u in enumerate(us)};rels=[]
 for row in range(3):
  caps=[2]*3;caps[row]=1;cells,ds=make_complex(n,3,caps);active=None
  for k in (1,2):R,C=reduce_units(ds[k],len(cells[k-1]),len(cells[k]),active);active=set(C)
  ker=top_kernel(ds[3],len(cells[2]),len(cells[3]),active);print('aux kernels',row,len(ker),flush=True)
  local=[]
  for f,s in cells[3]:
   olda=max(set(range(n))-{x for x,y in f});terms={s:1};r=n-4
   for q in range(r):
    raw=s[:q]+(olda,)+s[q+1:];inv=sum(raw[i]>raw[j] for i in range(r) for j in range(i+1,r));ss=tuple(sorted(raw));terms[ss]=terms.get(ss,0)-(-1)**inv
   co={}
   for ss,c in terms.items():
    if not c:continue
    u=tuple(x for x in range(n) if x not in ss);ff=tuple((u.index(x),y) for x,y in f)
    val=-c*phi.get(ff,0)*(-1)**(sum(u)-6)
    if val:co[ui[u]]=val
   local.append(co)
  for v in ker:
   rr=defaultdict(int)
   for j,c in v.items():
    for i,d in local[j].items():rr[i]+=c*d
   if any(rr.values()):rels.append(dict(rr))
 M=matrix(QQ,len(us),len(rels),{(i,j):v for j,rr in enumerate(rels) for i,v in rr.items()})
 print('actual relations shape/rank',M.dimensions(),M.rank(),'denom',M.denominator(),flush=True)
 N=matrix(ZZ,len(us),n+math.comb(n,2),{(i,j):1 for i,u in enumerate(us) for j,a in enumerate([(x,) for x in range(n)]+list(it.combinations(range(n),2))) if set(a)<=set(u)})
 print('target rank',N.rank(),'same rational image',M.column_space()==N.column_space(),flush=True)
 if M.denominator()==1:
  M=matrix(ZZ,M);print('same integral image',M.column_module()==N.column_module(),flush=True)
 with open(f'workspace/agent2_anchor_n{n}.pickle','wb') as f:pickle.dump((us,M,N),f)

if __name__=='__main__':
 for n in (7,8):anchor_relations(n)
 with open('workspace/agent2_anchor.py','w') as f:f.write(open(__file__).read())

