import json
j=json.load(open('workspace/agent1_lower44_certificate.json'));p=j['prime'];M=j['matrix'];d=1
for k in range(len(M)):
 r=next(i for i in range(k,len(M)) if M[i][k]%p)
 if r!=k:M[r],M[k]=M[k],M[r];d=-d
 v=M[k][k]%p;d=d*v%p;iv=pow(v,p-2,p)
 for i in range(k+1,len(M)):
  c=M[i][k]*iv%p
  for a in range(k,len(M)):M[i][a]=(M[i][a]-c*M[k][a])%p
assert d%p==540716==j['determinant']
print('Independent lower44 determinant:',d%p,'mod',p)
