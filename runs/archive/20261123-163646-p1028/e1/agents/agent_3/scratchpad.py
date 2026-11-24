from pathlib import Path
p=Path('workspace/check_d5_fulltail8.py');s=p.read_text();s=s.replace("from pathlib import Path\nPath('workspace/check_d5_fulltail8.py').write_text(Path(__file__).read_text())\n",'');p.write_text(s)
p=Path('workspace/odd_construction.py');s=p.read_text();s=s.replace("assert ecc==EXPECTED_CAP[n],(n,ecc)","assert ecc==EXPECTED_CAP[n],(n,ecc)\n        assert max(R.values())==ecc")
s=s.replace("R=resistance_matrix(G); assert R[0,1]==EXPECTED_BULK[n]","R=resistance_matrix(G); assert R[0,1]==EXPECTED_BULK[n]\n        assert max(R.values())==R[0,1]")
p.write_text(s)
exec(compile(s,str(p),'exec'))
