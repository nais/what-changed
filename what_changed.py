import glob
import logging
import os
import subprocess
from dataclasses import dataclass
from itertools import chain

LOG = logging.getLogger(__name__)


@dataclass
class Options:
    base: str
    head: str
    filepaths: str


def setup_logging():
    logging.basicConfig(level=logging.DEBUG, format="::%(levelname)s::%(message)s")
    # GitHub wants lowercase levelnames for workflow commands mapping
    for level in logging.getLevelNamesMapping().values():
        logging.addLevelName(level, logging.getLevelName(level).lower())


def main(options):
    setup_logging()
    cmd = ["git", "diff", "--name-only", options.base, options.head]
    changed_files = set(subprocess.run(cmd, capture_output=True, text=True).stdout.splitlines())
    LOG.debug("Changed files: %r", changed_files)
    input_files = set(chain(*(glob.glob(f) for f in options.filepaths.split(","))))
    LOG.debug("Input files: %r", input_files)

    if changed_files.issubset(input_files):
        LOG.info("Only inputs have been changed")
        output = "only-inputs"
    elif input_files.isdisjoint(changed_files):
        LOG.info("No inputs have been changed")
        output = "non-inputs"
    else:
        LOG.info("Both inputs and other files have been changed")
        output = "both"

    output_file = os.getenv("GITHUB_OUTPUT")
    if output_file:
        with open(output_file, "a") as f:
            f.write(f"changed={output}\n")
    else:
        LOG.info("No GITHUB_OUTPUT environment variable found, printing to stdout")
        LOG.info(f"changed={output}")


if __name__ == '__main__':
    options = Options(
        os.getenv("INPUT_BASE"),
        os.getenv("INPUT_HEAD"),
        os.getenv("INPUT_FILEPATHS"),
    )
    main(options)
