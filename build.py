#!/usr/bin/env python
import argparse
import shutil
import tempfile
import textwrap

PATTERN = "# Generated code below, DO NOT EDIT THIS LINE OR BELOW"


def main(options):
    indent = " " * options.indent_level
    with open(options.script_file, "r") as f:
        script = f.read()
    with tempfile.NamedTemporaryFile("w") as output:
        with open(options.action_file, "r") as f:
            for line in f:
                if line.strip() == PATTERN:
                    break
                output.write(line)
        output.write(indent + PATTERN + "\n")
        output.write(textwrap.indent(script, indent))
        output.flush()
        shutil.copy(output.name, options.action_file)



if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--action-file", help="The action file to embed the script in", default="action.yaml")
    parser.add_argument("--script-file", help="The script to embed", default="what_changed.py")
    parser.add_argument("--indent-level", type=int, default=8)
    main(parser.parse_args())
