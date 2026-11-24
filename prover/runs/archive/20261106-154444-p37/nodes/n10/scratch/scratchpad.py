from pathlib import Path
for name in ['product_upper_checks.py','refutation_certificate.py','lambda_counts.py']:
 print('\nFILE',name);print((Path('experiments/e1')/name).read_text()[:16000])
