#!/usr/bin/env python3
"""Entrypoint for the news-image-20261121 entry.

Copies the pre-built entry.png from this repository to the output
directory. Standard library only, no network, deterministic: every run
writes the same bytes. The image itself is drawn by generate.py.
"""
import os
import shutil


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    out = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out, exist_ok=True)
    shutil.copyfile(os.path.join(here, "entry.png"),
                    os.path.join(out, "entry.png"))


if __name__ == "__main__":
    main()
