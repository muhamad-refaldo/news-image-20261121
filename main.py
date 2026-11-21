#!/usr/bin/env python3
"""Entrypoint: copy the pre-built entry image to the output directory.

The entry image is drawn by generate.py and shipped in this repository as
entry.png. This program only copies it to $MAKEFUN_OUTPUT_DIR/entry.png
(default /output/entry.png). Standard library only, deterministic, no
network access. It runs twice; both runs must write identical bytes.
"""
import os
import shutil

HERE = os.path.dirname(os.path.abspath(__file__))


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    src = os.path.join(HERE, "entry.png")
    dst = os.path.join(out_dir, "entry.png")
    shutil.copyfile(src, dst)


if __name__ == "__main__":
    main()
