from pathlib import Path
s=Path('experiments/e3/agent2_c2_hnf.py').read_text().replace("open('workspace/agent2_true_relations.json')","open('experiments/e3/agent2_true_relations.json')")
s=s.replace("for data in results:\n", "for data in results:\n if data['n'] != 5: continue\n")
s=s[:s.index("Path('workspace/")];exec(compile(s,'hnf','exec'))
import pickle
pickle.dump((names,S.rows),open('rank5_quad.pkl','wb'))
print('saved',len(S.rows))