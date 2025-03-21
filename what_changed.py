#!/usr/bin/env python

import argparse
import glob
import logging
import os
import subprocess
from itertools import chain

LOG = logging.getLogger(__name__)


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
    parser = argparse.ArgumentParser()
    parser.add_argument("base", help="Base commit")
    parser.add_argument("head", help="Head commit")
    parser.add_argument("filepaths", help="Comma-separated list of filepaths to check (supports globbing)")
    options = parser.parse_args()
    main(options)
