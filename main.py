"""One Line to Your Younger Self.

Writes exactly one line to /output/entry.txt: the line the writer would
send back to their younger self. Standard library only.
"""

import os
import stat
import sys

LINE = (
    "Kid, eat the lunch your mother packed even when the other boys laugh "
    "\u2014 one day you'll pay good money for food that never tastes "
    "like home again."
)


def _remove(path):
    """Remove a file, link, or directory tree, restoring owner permission
    first when leftovers are read-only or untraversable."""
    if os.path.islink(path) or not os.path.isdir(path):
        try:
            os.remove(path)
        except OSError:
            os.chmod(path, stat.S_IRWXU)
            os.remove(path)
        return
    try:
        names = os.listdir(path)
    except OSError:
        os.chmod(path, stat.S_IRWXU)
        names = os.listdir(path)
    # Removing children needs write permission on this directory itself.
    try:
        os.chmod(path, stat.S_IRWXU)
    except OSError:
        pass
    for name in names:
        _remove(os.path.join(path, name))
    try:
        os.rmdir(path)
    except OSError:
        os.chmod(path, stat.S_IRWXU)
        os.rmdir(path)


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
        _remove(os.path.join(out_dir, name))

    out_path = os.path.join(out_dir, "entry.txt")
    with open(out_path, "w", encoding="utf-8", newline="") as f:
        f.write(LINE)

    # Verify the written file round-trips byte-identical; fail loudly
    # instead of leaving a bad artifact behind.
    with open(out_path, encoding="utf-8", newline="") as f:
        if f.read() != LINE:
            print("entry.txt does not match the intended line",
                  file=sys.stderr)
            return 1
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except OSError as exc:
        print(f"error: {exc}", file=sys.stderr)
        raise SystemExit(1)
