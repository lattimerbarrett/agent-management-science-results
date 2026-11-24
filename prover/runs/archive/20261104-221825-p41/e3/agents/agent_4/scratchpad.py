import json,itertools
G=json.load(open('workspace/agent2_gluecounter.json'))['G'];bs=[]
for q in itertools.combinations(range(7),4):
 f=sum(1<<v for v in q)
 if all(f^(1<<v)in G for v in q):bs.append(q)
print(bs)
