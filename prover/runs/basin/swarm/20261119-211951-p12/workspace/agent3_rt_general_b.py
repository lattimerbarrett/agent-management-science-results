from pathlib import Path
source=Path('workspace/agent3_rt_boundary_test.py').read_text().split('# b must have at least one ψ exponent.')[0]
exec(source)
print('begin general support search',flush=True)
DR=[{j-len(cols13):v for j,v in row.items()} for row in rows if row and min(row)>=len(cols13)]
RE=matrix(F,len(DR),len(dcols),{(i,j):v for i,row in enumerate(DR) for j,v in row.items()}).echelon_form()
rp=RE.pivots();rf=[j for j in range(len(dcols)) if j not in rp];rpi={j:i for i,j in enumerate(rp)};RE=RE[:len(rp),:];dix0={p:i for i,p in enumerate(dcols)}
print('rootdegree12 rank',len(rp),'qdim',len(rf),flush=True)
bD=root_at(11);T=matrix(F,len(cols12)+len(bD),C.ncols()+len(rf))
T[:len(cols12),:C.ncols()]=C
for i,term in enumerate(cols12+bD):
 v=(F**len(dcols))(0)
 if i<len(cols12):
  p,a,b=term
  if a==b==0:v[dix0[p,0]]=1
 else:
  p,k=term;v[dix0[p,k+1]]=-1
 for j in rp:
  if v[j]:v-=v[j]*RE[rpi[j]]
 for u,j in enumerate(rf):T[i,C.ncols()+u]=v[j]
K=T.left_kernel().basis_matrix()
print('general compact-support annihilator dim',K.nrows(),'elapsed',time.time()-start,flush=True)
bs=[]
for row in K:
 terms=[]
 for i,x in enumerate(row):
  if not x:continue
  if i<len(cols12):p,a,b=cols12[i];terms.append((0,p,a,b,int(x)))
  else:p,k=bD[i-len(cols12)];terms.append((1,p,k,0,int(x)))
 bs.append(terms)
pickle.dump({'prime':prime,'b':bs,'openbasis':cols12,'Dbasis':bD},open('workspace/agent3_rt_general_b.pkl','wb'))
if Path(__file__).name=='scratchpad.py':Path('workspace/agent3_rt_general_b.py').write_text(Path(__file__).read_text())
