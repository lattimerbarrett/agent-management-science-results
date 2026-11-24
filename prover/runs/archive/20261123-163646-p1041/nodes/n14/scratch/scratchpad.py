from pathlib import Path
for f in ['agent3_W3_256_Q382_310_constructor.py','agent3_W2_256_Q382_310_constructor.py']:
 p=Path('experiments/e2')/f
 print('\n###',f,'\n',p.read_text()[:13000])