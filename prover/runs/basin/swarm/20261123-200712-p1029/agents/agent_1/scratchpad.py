import os
roots=['/usr/share/doc','/usr/local/share','/opt','/tmp']
hits=[]
for root in roots:
    if not os.path.isdir(root): continue
    for d,ds,fs in os.walk(root):
        ds[:]=[s for s in ds if s not in {'node_modules','.git','__pycache__'}]
        for f in fs:
            lo=f.lower()
            if any(s in lo for s in ['quasitrace','monotone_complete','awstar','aw-star','berberian']):
                hits.append(os.path.join(d,f))
print(hits[:100])
