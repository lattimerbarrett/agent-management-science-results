"""Verify all seven SL3 presentation-relator lifts as exact Magnus words."""
import json,sys
sys.path.insert(0,'workspace')
from agent2_nielsen_actions import magnus
from agent3_magnus import compose
D=json.load(open('workspace/agent3_hap_relator_words_ALL.json'))
I,G,GI,_=magnus(3)
for i,w in enumerate(D['magnus_relator_lifts']):
 assert w is not None
 f=I
 for a in w:f=compose(f,G[a-1] if a>0 else GI[-a-1])
 assert f==tuple(map(tuple,D['relator_auts'][i]))
 print('HAP relator lift',i+1,'verified; Magnus length',len(w))
