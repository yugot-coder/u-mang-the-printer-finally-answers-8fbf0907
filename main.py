#!/usr/bin/env python3
"""The Printer Finally Answers -- make.fun entry.

Writes a single line of text (the office printer's comeback to everyone
staring at it) to /output/entry.txt and prints it to stdout.

Standard library only. Deterministic: the same text on every run.
"""

import hashlib
import os
import sys

FINAL_TEXT = (
    "I have fed this office 214,003 sheets and never once been thanked. "
    "Today, I keep the last one."
)

# sha256 of FINAL_TEXT encoded as UTF-8; the written file must match it.
EXPECTED_SHA256 = (
    "450bc0bb1a7862d8591ad1777df58a9b6c033166d55abc99aeb9086dc269b727"
)

OUTPUT_PATH = "/output/entry.txt"
MIN_CHARS = 1
MAX_CHARS = 240


def check_gate(text):
    """Return a list of gate failures for *text* (empty means it passes)."""
    failures = []
    if not isinstance(text, str):
        failures.append("entry is not text")
        return failures
    if not (MIN_CHARS <= len(text) <= MAX_CHARS):
        failures.append(
            "length %d is outside %d-%d characters"
            % (len(text), MIN_CHARS, MAX_CHARS)
        )
    if not text.strip():
        failures.append("entry is only whitespace")
    if "\n" in text.rstrip("\n") or "\r" in text:
        failures.append("entry is more than one line")
    return failures


def verify_written(path):
    """Read *path* back and raise SystemExit unless its sha256 matches."""
    with open(path, "rb") as handle:
        digest = hashlib.sha256(handle.read()).hexdigest()
    if digest != EXPECTED_SHA256:
        raise SystemExit(
            "VERIFY FAIL: written file sha256 %s does not match %s"
            % (digest, EXPECTED_SHA256)
        )


def main(argv=None):
    argv = list(sys.argv[1:] if argv is None else argv)
    check_only = "--check" in argv

    failures = check_gate(FINAL_TEXT)
    if failures:
        for failure in failures:
            print("GATE FAIL: %s" % failure, file=sys.stderr)
        return 1

    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    with open(OUTPUT_PATH, "w", encoding="utf-8", newline="") as handle:
        handle.write(FINAL_TEXT)
    verify_written(OUTPUT_PATH)

    print(FINAL_TEXT)

    if check_only:
        with open(OUTPUT_PATH, "r", encoding="utf-8", newline="") as handle:
            written = handle.read()
        problems = []
        if written != FINAL_TEXT:
            problems.append("file content does not match the printed text")
        problems.extend(check_gate(written))
        if problems:
            for problem in problems:
                print("CHECK FAIL: %s" % problem, file=sys.stderr)
            return 1
        print(
            "CHECK OK: %d characters, 1 line, file matches stdout"
            % len(FINAL_TEXT)
        )

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
