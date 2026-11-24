from pathlib import Path
p=Path('experiments/e1')
print((p/'agent3_cvec_basis.py').read_text()[:18000])
print((p/'degree1_certificate.py').read_text()[:2500])