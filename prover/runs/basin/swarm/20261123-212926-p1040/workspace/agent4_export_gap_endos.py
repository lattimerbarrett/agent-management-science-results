from agent4_export_gap_seeds import *
def export():
 n=3;out,C,M=run();names=out['names'];endos=[]
 def emit(name,images):
  assert len(images)==9
  endos.append({'name':name,'images':images})
 # inversion I1
 images=[]
 for typ,*q in names:
  if typ=='C':
   a,b=q;images.append(inv(C[a,b]) if b==1 else C[a,b])
  else:
   a,b,c=q;s=[0,0,0]
   if 1 in q:s[q.index(1)]=n
   images.append(M[a+s[0],b+s[1],c+s[2]])
 emit('I1',images)
 for perm in permutations(range(1,4)):
  if perm==(1,2,3):continue
  pp={i+1:x for i,x in enumerate(perm)}
  images=[]
  for typ,*q in names:
   if typ=='C':a,b=q;images.append(C[pp[a],pp[b]])
   else:a,b,c=q;images.append(M[pp[a],pp[b],pp[c]])
  emit('P'+str(perm),images)
 for p1,p2 in product([0,n],repeat=2):
  alpha=1 if p1==0 else -1
  images=[]
  for typ,*q in names:
   if typ=='C':
    a,b=q
    if b==1 and a!=2:z=mul(C[a,2+p2],C[a,1+p1]);z=z if alpha==1 else inv(z)
    elif a==1 and b!=2:z=mul(M[1+p1,2+n-p2,b],C[1,b])
    elif a==2 and b!=1:z=mul(M[1+p1,2+n-p2,b+n],C[2,b])
    elif (a,b)==(2,1):z=mul(C[2,1+p1],C[1,2+p2]);z=z if alpha==1 else inv(z)
    else:z=C[a,b]
   else:
    a,b,c=q
    if a==1+p1 and b==2+p2:z=conj(M[a,b,c],C[1,2+p2])
    elif a==1+p1 and b==2+n-p2:z=conj(M[a,b,c],C[1,2+p2])
    elif a==2+p2 and b==1+p1:
     z=mul(M[a+n,b,c+n],C[2,c+n],M[b,a+n,c],C[1,c])
    elif a==2+p2 and b==1+n-p1:
     z=conj(mul(C[1,c+n],M[1+p1,c,2+n-p2],C[2,c],M[2+n-p2,c+n,1+p1]),mul(C[c,1+n-p1],C[c,2+n-p2]))
    elif a==2+n-p2 and b==1+p1:
     z=mul(conj(mul(conj(mul(C[2,c],M[b,c,a]),C[c,2+p2]),M[a,c,b+n]),C[c,1+p1]),C[1,c+n])
    elif a==2+n-p2 and b==1+n-p1:
     z=mul(conj(mul(conj(C[1,c],C[c,1+n-p1]),M[a,b,c]),C[c,2+n-p2]),M[1+p1,a,c],C[2,c+n])
    elif b==1+p1 and c==2+p2:z=conj(M[a,b,c],C[1,2+p2])
    elif b==1+p1 and c==2+n-p2:z=M[a,c+n,b]
    else:z=M[a,b,c]
   images.append(z)
  emit('M12'+str((p1,p2)),images)
 out['endomorphisms']=endos
 return out
if __name__=='__main__':
 out=export();Path(__file__).with_name('agent4_gap_ia3_data.json').write_text(json.dumps(out,indent=2))
 print('endomorphisms',len(out['endomorphisms']))
