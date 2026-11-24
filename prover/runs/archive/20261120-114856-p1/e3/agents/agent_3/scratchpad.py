import pathlib
for nm in ['workspace/mixed_conic_search_agent4.py','workspace/billiard_cert_agent1.py']:
 print(nm);print(pathlib.Path(nm).read_text()[:18000])