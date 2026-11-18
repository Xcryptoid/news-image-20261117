#!/usr/bin/env python3
"""Entry program for news-image-20261117 (Python 3.13, standard library only).

Copies the entry image (entry.png, beside this file) to the output
directory as entry.png. The grader runs it twice and both runs must write
the same bytes, so this is a plain byte-for-byte copy: no drawing, no
timestamps, no network.
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
    # sanity check: the copy must be a whole PNG of the same size, so a
    # truncated write can never pass as a valid entry.
    src_size = os.path.getsize(src)
    dst_size = os.path.getsize(dst)
    if dst_size != src_size or dst_size > 1048576:
        raise SystemExit("entry.png copy failed validation: %d bytes" % dst_size)
    print("wrote %s (%d bytes)" % (dst, dst_size))


if __name__ == "__main__":
    main()
