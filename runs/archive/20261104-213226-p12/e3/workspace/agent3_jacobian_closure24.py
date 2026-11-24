exec(open('workspace/agent3_jacobian_p31_24.py').read().split('initial=')[0])
exec(open('workspace/agent3_jacobian_convert.py').read().split('for n in [18,24]:')[0])
checkpoint={tuple(tuple(v) for v in k):c for k,c in json.load(open('workspace/agent3_jacobian_p31_24_checkpoint35.json'))}
for z,mult in enumerate([[(0,-2)],[(0,2)],[(2,2)],[(4,2)],[(1,1)]*2,[(1,1),(3,1)],[(3,1)]*2]):
 poly={tuple(sorted(mon+tuple(mult))):c for mon,c in checkpoint.items()}
 for r in range((2+sum(i for i,j in mult))//2):poly=deriv(poly)
 filename=f'workspace/agent3_jacobian_closure24_{z}.json';json.dump([[k,v] for k,v in poly.items()],open(filename,'w'))
 rel=convert(filename,0);a=[0]*77
 for mon,c in rel.items():a[idx[mon]]=c
 for piv,b in zip(pivs,rref):
  c=a[piv]
  if c:a=[(x-c*y)%P for x,y in zip(a,b)]
 print('multiplier',mult,'bottomterms',len(poly),'pushterms',len(rel),'remainderterms',sum(bool(x) for x in a))
