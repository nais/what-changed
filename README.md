# what-changed

Action looks at changed files since last successful workflow run and determines what changed.

The action takes a list of file paths as input, and outputs a string as follows:

- `only-inputs`: true if only files in the input list changed
- `non-inputs`: true if only files outside the input list changed
- `both`: true if both files in the input list and outside the input list changed

## For developers

Most of the action is in `what_changed.py`, but this script is embedded in the composite workflow in `action.yaml`.
In order to update the action, run `mise run build`.
