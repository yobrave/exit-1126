"""Build the one-line resignation letter for The One-Line Exit.

Reads entry.txt beside this file, validates it against the bounty gate
(UTF-8, 1..140 characters, not blank) and writes it to the output dir
the runner provides, printing a receipt along the way.
"""
import json
import os
import pathlib

HERE = pathlib.Path(__file__).resolve().parent
OUT_ROOT = os.environ.get("MAKEFUN_OUTPUT_DIR") or "out"
EXIT_GATE_MAX = 140
EXIT_STAMP = "desk-4F: one line, lights off on the way out"


def load_line():
    raw = (HERE / "entry.txt").read_bytes().decode("utf-8")
    return raw.strip("\r\n")


def seal(line):
    problems = []
    if not line.strip():
        problems.append("blank entry")
    size = len(line)
    if size > EXIT_GATE_MAX:
        problems.append(f"too long: {size} > {EXIT_GATE_MAX}")
    if size < 1:
        problems.append("empty entry")
    return {"chars": size, "problems": problems}


def main():
    line = load_line()
    report = seal(line)
    ok = not report["problems"]
    target = pathlib.Path(OUT_ROOT)
    target.mkdir(parents=True, exist_ok=True)
    receipt = {
        "gate": "exit-140",
        "stamp": EXIT_STAMP,
        "chars": report["chars"],
        "verdict": "PASS" if ok else "FAIL",
        "detail": report["problems"],
    }
    (target / "entry.txt").write_text(line + "\n", encoding="utf-8", newline="\n")
    print(json.dumps(receipt))


if __name__ == "__main__":
    main()
