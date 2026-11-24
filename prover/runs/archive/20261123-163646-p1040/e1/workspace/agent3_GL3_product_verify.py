import json,sys
sys.path.insert(0,'workspace')
from agent3_magnus import reduce_word,inverse,auto_commutator,compose
from agent2_nielsen_actions import magnus
D=json.load(open('workspace/agent3_GL3_product_identities.json'))
H=json.load(open('workspace/agent3_hap_relator_words_ALL.json'))
I,G,GI,_=magnus(3);z=tuple(map(tuple,D['z_auto']))
for j,h in enumerate(H['lifts']):
 c=auto_commutator(z,z,tuple(map(tuple,h['auto'])),tuple(map(tuple,h['inverse'])))
 f=I
 for a in D['relator_magnus_words'][8+j]:f=compose(f,G[a-1] if a>0 else GI[-a-1])
 assert f==c
for d in D['identities']:
 w=[]
 for u,j,e in d['terms']:
  r=D['relators'][j];w+=u+(r if e>0 else list(inverse(r)))+list(inverse(u))
 assert not reduce_word(w)
print('PASS all3centralcommutatorlifts and11literalGL3productidentities')
