exec(open('workspace/agent3_jacobian_convert.py').read().split('for n in [18,24]:')[0])
rel=convert('workspace/agent3_jacobian_mixed26.json',0)
a=[0]*77
for mon,c in rel.items():a[idx[mon]]=c
for piv,b in zip(pivs,rref):
 c=a[piv]
 if c:a=[(x-c*y)%P for x,y in zip(a,b)]
print('relationterms',len(rel),'remainderterms',sum(bool(x) for x in a))
json.dump([[k,v] for k,v in rel.items()],open('workspace/agent3_jacobian_mixed26_push.json','w'))
