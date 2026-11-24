import pickle,itertools,json
D=pickle.load(open('workspace/agent2_C35.pkl','rb'));C=D['C'];base=C[:25];imag=base[15:25];rows=C+[a&b for a in imag for b in base];P={};basis=[]
for b in rows:
 while b:
  i=b.bit_length()-1
  if i in P:b^=P[i]
  else:P[i]=b;basis.append(b);break
print('enrichedrank',len(P));assert all((a&b).bit_count()%2==0 for a,b in itertools.combinations_with_replacement(basis,2))
D['C']=basis
pickle.dump(D,open('workspace/agent2_Cquartic.pkl','wb'));json.dump(D,open('workspace/agent2_Cquartic.json','w'))
