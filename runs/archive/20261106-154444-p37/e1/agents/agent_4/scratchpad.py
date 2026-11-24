from pathlib import Path
for filename in ['q_dimension_checks.py','lambda_counts.py','rainbow_product_checks.py']:
    path=Path('workspace')/filename
    text=path.read_text()
    lines=text.splitlines(True)
    # Remove only our original self-copy line; leave guarded test code intact.
    new=''.join(line for line in lines if not ("Path('workspace/" in line and '.write_text(Path(__file__).read_text())' in line))
    # A guard containing only an import remains syntactically valid.
    path.write_text(new)
    print('Removed self-copy side effects:',filename)
