from pathlib import Path
p=Path('experiments/e3/agent3_local_pohozaev_bridge.md');s=p.read_text();print(s[s.index('## Step 5'):])
print('\n---e7 mass end---')
s=Path('experiments/e7/agent3_compactness_bridge.md').read_text();print(s[:4500])
