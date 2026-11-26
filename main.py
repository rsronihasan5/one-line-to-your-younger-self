"""One Line to Your Younger Self.

Writes exactly one line to /output/entry.txt: the line the writer would
send back to their younger self. Standard library only.
"""

import os
import sys

LINE = (
    "Kid, eat the lunch your mother packed even when the other boys laugh "
    "\u2014 one day you'll pay good money for food that never tastes "
    "like home again."
)


def main() -> int:
    # Validate the gate inside the program: 1-200 characters, one line,
    # not only whitespace, English text.
    if not (1 <= len(LINE) <= 200):
        print(f"entry must be 1-200 characters, got {len(LINE)}",
              file=sys.stderr)
        return 1
    if LINE.strip() == "" or "\n" in LINE or "\r" in LINE:
        print("entry must be a single non-blank line", file=sys.stderr)
        return 1

    out_dir = "/output"
    os.makedirs(out_dir, exist_ok=True)
    # Clean only the contents of the output dir, never the dir itself.
    for name in os.listdir(out_dir):
        path = os.path.join(out_dir, name)
        if os.path.isdir(path) and not os.path.islink(path):
            for root, dirs, files in os.walk(path, topdown=False):
                for f in files:
                    os.remove(os.path.join(root, f))
                for d in dirs:
                    os.rmdir(os.path.join(root, d))
            os.rmdir(path)
        else:
            os.remove(path)

    with open(os.path.join(out_dir, "entry.txt"), "w",
              encoding="utf-8", newline="") as f:
        f.write(LINE)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
