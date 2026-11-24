from pathlib import Path
exec(Path('workspace/agent4_comb_direct_hilbert_checks.py').read_text().split('res=[]')[0])
maxerr=0.
for p in [2.,3.,5.]:
 for Q in [10.,100.,10000.]:
  previous=0.
  for n in range(1,9):
   B,C,_,_,_=bilinear(Q,p,n)
   ra=2-1/Q
   err=abs(B-C-(ra/2)*previous)/max(1.,abs(B))
   maxerr=max(maxerr,err)
   assert err<1e-7
   previous=B
print('72 exact-cell recurrence identities passed, max relative error',maxerr)
constants=[]
for m in [2,4,6,8,10]:
 left=np.array([0.]);eta=np.array([0.]);length=1.
 for j in range(m):
  left=np.r_[left+length/4,left+length/2]
  eta=np.r_[eta+2.**(-j),eta-2.**(-j)]
  length/=4
 x=left+length/2
 ix=np.where(x<.5)[0];iy=np.where(x>.5)[0]
 C=2*np.sum((eta[ix,None]-eta[None,iy])/(x[ix,None]-x[None,iy]))/(len(x)**2*np.pi)
 constants.append((m,float(C)))
 assert C<=-2/np.pi
 print('Cantor prefix',m,'cross form',C)
Path('workspace/agent4_comb_recurrence_checks.py').write_text(Path(__file__).read_text())
Path('workspace/agent4_comb_recurrence_checks.txt').write_text(str({'max_error':maxerr,'cantor_constants':constants}))
