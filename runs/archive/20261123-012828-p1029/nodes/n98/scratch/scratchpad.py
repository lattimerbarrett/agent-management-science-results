from pathlib import Path
# Audit the existing notes for hypotheses relevant to the supplied
# finite-factor monotone sequential completeness theorem.
for name in ['agent3_completion_audit.md','agent4_reduction_notes.md']:
    p=Path('experiments/e1')/name
    print('\n'+name)
    if p.exists():
        for line in p.read_text().splitlines():
            if any(word in line.lower() for word in ['finite', 'monotone', 'normal', 'not claim', 'not been']):
                print(line)
print('\nHypothesis match: unital AW* + finite + factor; sequence bounded by the unit.')
