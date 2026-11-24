from agent4_export_gap_endos import *

def subst(w,images):return mul(*(images[x-1] if x>0 else inv(images[-x-1]) for x in w))
def export():
 out,C,M=run();data=json.loads(Path(__file__).with_name('agent4_gap_ia3_data.json').read_text());n=3
 endos=data['endomorphisms'];rels=[]
 def flip(x):return x+n if x<=n else x-n
 for ei,e in enumerate(endos):
  ims=[tuple(w) for w in e['images']]
  for q in permutations(range(1,n+1),3):
   if q[1]>q[2]:continue
   for ss in product([0,n],repeat=3):
    a,b,c=(q[i]+ss[i] for i in range(3));w=M[a,b,c]
    if ei==0:
     qq=[a,b,c];ii=q.index(1);qq[ii]=flip(qq[ii]);z=M[tuple(qq)]
    elif ei<6:
     perm=eval(e['name'][1:]);qq=[perm[q[i]-1]+ss[i] for i in range(3)];z=M[tuple(qq)]
    else:
     p1,p2=eval(e['name'][3:]);basec=q[2]
     if a==1+p1 and b in (2+p2,2+n-p2):z=conj(w,C[1,2+p2])
     elif a==2+p2 and b==1+p1:
      z=mul(M[flip(a),b,flip(c)],C[2,flip(c)],M[b,flip(a),c],C[1,c])
     elif a==2+p2 and b==1+n-p1:
      z=conj(mul(C[1,flip(c)],M[1+p1,c,2+n-p2],C[2,c],M[2+n-p2,flip(c),1+p1]),mul(C[basec,1+n-p1],C[basec,2+n-p2]))
     elif a==2+n-p2 and b==1+p1:
      z=mul(conj(mul(conj(mul(C[2,c],M[b,c,a]),C[basec,2+p2]),M[a,c,flip(b)]),C[basec,1+p1]),C[1,flip(c)])
     elif a==2+n-p2 and b==1+n-p1:
      z=mul(conj(mul(conj(C[1,c],C[basec,1+n-p1]),w),C[basec,2+n-p2]),M[1+p1,a,c],C[2,flip(c)])
     elif b==1+p1 and c==2+p2:z=conj(w,C[1,2+p2])
     elif b==1+p1 and c==2+n-p2:z=M[a,flip(c),b]
     else:z=w
    r=div(subst(w,ims),z)
    if r:rels.append({'endo':e['name'],'M':[a,b,c],'word':r})
 return {'names':data['names'],'rels':rels}
if __name__=='__main__':
 out=export();print('nontrivial signed compatibility relators',len(out['rels']));Path(__file__).with_suffix('.json').write_text(json.dumps(out,indent=2))
