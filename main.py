#!/usr/bin/env python3
"""passport-page-talvera entry for make.fun bounty
the-passport-page-of-a-countr-2-20261121-0318.

The image (entry.png, 1024x720, 230,111 bytes) is an invented passport
spread for the Republic of Talvera, a sea-only island nation: a data page
with an engraved profile portrait, bilingual fields and a machine-readable
zone with correct check digits, facing a visa page with a Korvath visa
sticker, entry/exit stamps from three neighbouring countries and a
harbourmaster condition stamp. Every stamp date falls after the passport's
issue date (14 JAN 2025) and the travel history closes with a return home
(03 MAY 2025). It was drawn by the build script in the work session and is
bundled here.

This program only copies the bundled image to the output path, verifying
it first. Standard library only, no network, and every run writes the
exact same bytes.
"""

import os
import struct
import sys

MAX_BYTES = 1_048_576
EXPECT_W, EXPECT_H = 1024, 720
PNG_MAGIC = b"\x89PNG\r\n\x1a\n"


def read_bundle():
    here = os.path.dirname(os.path.abspath(__file__))
    path = os.path.join(here, "entry.png")
    with open(path, "rb") as fh:
        return fh.read()


def check_png(data):
    """Check magic, size, and IHDR dimensions; return (width, height)."""
    if len(data) > MAX_BYTES:
        raise SystemExit(f"entry.png too large: {len(data)} bytes")
    if data[:8] != PNG_MAGIC:
        raise SystemExit("entry.png is not a PNG file")
    if len(data) < 33 or data[12:16] != b"IHDR":
        raise SystemExit("entry.png has no IHDR chunk")
    width, height = struct.unpack(">II", data[16:24])
    if (width, height) != (EXPECT_W, EXPECT_H):
        raise SystemExit(f"unexpected size {width}x{height}")
    if b"IEND" not in data[-12:]:
        raise SystemExit("entry.png has no IEND chunk")
    return width, height


def main():
    data = read_bundle()
    width, height = check_png(data)
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, "entry.png")
    with open(out_path, "wb") as fh:
        fh.write(data)
    with open(out_path, "rb") as fh:
        written = fh.read()
    if written != data:
        raise SystemExit("written bytes differ from the bundle")
    print(f"wrote {out_path} ({width}x{height}, {len(data)} bytes)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
