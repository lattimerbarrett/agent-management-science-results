# Agent Management Science: results

The data, logs and code behind the experiments in the post "Agent Management Science". Each experiment in the post
has one folder here, with what you need to check its numbers and to run it again.

## Results at a glance

One short block per experiment, in the order the post has them. The detail is in each folder's own README.

### Prover: explore, then prove · [`prover/`](prover/)

*Section of the post: "Branch on a doubt, collaborate on a proof".* One model, GPT-6.1 Sol at medium reasoning
effort, is organized three ways and set research-level problems from MathArena's ArXivMath.

| problems solved | September, 9 problems | October, 14 problems |
|---|---|---|
| **Full system** (explore, then a team of four on each candidate answer) | **8 of 9** · $23.30 a problem | **10 of 14** · $40.52 a problem |
| **One team of four**, given only the problem | **5 of 9** · $7.98 a problem | **8 of 14** · $14.69 a problem |
| **Lone agent**, given only the problem | **3 of 9** on the first run · **4 of 9** by any of up to 8 runs | **1 of 14** on the first run · **4 of 14** by any of up to 4 runs |

"Solved" means the system stopped on a proof that a separate judge, a model, accepted, and its answer matches the
paper's. No person has checked the proofs. The problem-by-problem tables, the logs of every run and the code are
in [`prover/`](prover/).

## How the repo is laid out

```
README.md       this page: the headline results of every experiment
_template/      a README to start a new section from
prover/         a section
```

**A section is one folder, and it stands alone.** It has its own README, its own result tables, its own logs, and
its own code with its own list of what to install. Nothing is shared between sections. So a change in one section
can't break another, and a reader can take one folder and leave the rest.

Inside a section:

| | what goes there |
|---|---|
| `README.md` | The headline numbers first. Then what was run, what the numbers mean, what is in the folder and how to run it again. |
| `results/` | The numbers behind each figure and sentence in the post, as small files (CSV, JSON, Markdown), with the script that rebuilds them from the logs. |
| `runs/` or `data/` | The raw logs or data, as the code wrote them. |
| the code | Only what the experiment needs to run, with its own dependency file (`pyproject.toml`, `requirements.txt`, ...) inside the folder. |

`prover/` is laid out this way, if you want an example to copy from.

## Adding your section

1. **Make a folder at the top level, named for the experiment**, in lowercase words joined by hyphens: for example
   `peer-reading/`, `harness-optimizers/` or `program-reconstruction/`.
2. **Copy `_template/README.md` into it and fill it in.** The headline numbers go first: the ones the post quotes.
3. **Add your results, logs and code**, laid out as in the table above.
4. **Add a block to "Results at a glance"** on this page: a heading that links to your folder, the section of the
   post it belongs to, and one small table or a few sentences. Keep everything else in your own README.
5. **Change only your own folder and your own block on this page.** If something in another section looks wrong,
   tell whoever owns it.

### Before you commit

- **No keys, tokens or passwords**, in code or in logs. Code reads its keys from the environment. Logs are where
  one slips in, so search yours before the first commit. This lists the files to look at:

      grep -rlE '(^|[^A-Za-z0-9_-])(sk-|hf_|ghp_|xox[abp]-)[A-Za-z0-9_-]{20,}' your-section/

- **Only what you may share.** If a dataset's terms don't allow copies of it, link to it and leave it out. Read
  through the logs for anything private.
- **No file over 50 MB.** GitHub refuses a file over 100 MB. Leave out caches, model weights and anything that
  can be made again, and say in your README what you left out (`prover/runs/OMITTED.tsv` is the prover's list).
- **No environments or caches**: `.venv/`, `node_modules/`, `__pycache__/`. The `.gitignore` here covers the common
  ones. Put a `.gitignore` in your own folder for anything else.
- **Every number in your README should be in a file under `results/`**, so a reader can trace it to the logs.

### Working on one section without downloading the others

The prover's logs are about 2 GB. To get only your own folder:

    git clone --filter=blob:none --sparse https://github.com/lattimerbarrett/agent-management-science-results.git
    cd agent-management-science-results
    git sparse-checkout set your-section _template

The files at the top level, this page among them, always come along. A folder that isn't in the repo yet works too:
make it, add your files, then commit and push as usual.
