import json,os
s=json.load(open('experiments/e1/agent4_flat_seeds.json'))
print({k:v for k,v in s.items() if int(k) in [338,342,346,350,354,358,362,322]})
print(open('experiments/e1/agent2_six_affine_candidate_model.py').read()[:6000])
