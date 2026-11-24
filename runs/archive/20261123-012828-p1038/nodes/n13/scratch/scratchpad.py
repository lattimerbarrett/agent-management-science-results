from pathlib import Path
import pickle
for f in ['agent4_contract_fail1.pkl','agent4_contract2_fail1.pkl','agent4_actual_reference_counter.json','agent4_interval_counterexample.json']:
 print('\n',f)
 if f.endswith('.pkl'):
  z=pickle.load(open('experiments/e1/'+f,'rb'));print(str(z)[:4000])
 else:print(Path('experiments/e1/'+f).read_text()[:4000])
