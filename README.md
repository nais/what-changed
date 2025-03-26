# what-changed

Action looks at changed files since last successful workflow run and determines what changed.

The action takes a list of file paths as input, and outputs a string as follows:

- `only-inputs`: true if only files in the input list changed
- `non-inputs`: true if only files outside the input list changed
- `both`: true if both files in the input list and outside the input list changed

## Inputs

The action takes two inputs, one of which is required:

- `files`: A comma-separated list of file paths to check for changes. Required.
  The list supports recursive [glob patterns](https://docs.python.org/3/library/glob.html#glob.glob) including hidden files and directories.
- `main-branch-name`: The name of the main branch. Optional, default is `main`.

## How does it work

First, we use [nrwl/nx-set-shas](https://github.com/nrwl/nx-set-shas) to determine the `BASE` and `HEAD` of the change set.
We then compare the list of files changed between `BASE` and `HEAD` with the list of files provided as input.

If the list of changed files is a subset of the input list, we output `only-inputs`.
If the list of changed files is disjoint from the input list, we output `non-inputs`.
Otherwise, we output `both`.

## For developers

Most of the action is in `what_changed.py`, but this script is embedded in the composite workflow in `action.yaml`.
In order to update the action, run `mise run build`.

It is recommended to install a pre-commit hook to ensure that the action is built before committing changes.
You can use `mise run install-pre-commit` to install the hook.
