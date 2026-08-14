"""Validate generated ICPC300 and Focus300 teaching notes."""

from __future__ import annotations

import argparse
import ast
import re
from pathlib import Path


REQUIRED_HEADINGS = (
    "first principles",
    "cases",
    "brute",
    "better",
    "expert",
)


def validate_note(path: Path) -> list[str]:
    text = path.read_text(encoding="utf-8")
    lowered = text.lower()
    errors = [
        f"{path}: missing section containing {heading!r}"
        for heading in REQUIRED_HEADINGS
        if heading not in lowered
    ]

    blocks = re.findall(r"```python\n(.*?)\n```", text, re.DOTALL)
    if not 2 <= len(blocks) <= 3:
        errors.append(
            f"{path}: expected brute and expert code, plus better code when "
            f"available; found {len(blocks)} Python blocks"
        )

    for index, block in enumerate(blocks, start=1):
        try:
            tree = ast.parse(block)
        except SyntaxError as error:
            errors.append(f"{path}: block {index}: {error.msg}")
            continue

        executable = [
            node
            for node in tree.body
            if not isinstance(node, (ast.Import, ast.ImportFrom))
        ]
        if not executable or all(isinstance(node, ast.Expr) for node in executable):
            errors.append(f"{path}: block {index} has no implementation")
        if re.search(r"\b(?:TODO|FIXME|NotImplemented|placeholder)\b", block, re.I):
            errors.append(f"{path}: block {index} contains placeholder text")

    return errors


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("directory", type=Path)
    parser.add_argument("--first", type=int, required=True)
    parser.add_argument("--last", type=int, required=True)
    arguments = parser.parse_args()

    errors: list[str] = []
    for number in range(arguments.first, arguments.last + 1):
        matches = list(arguments.directory.glob(f"{number:03d}-*.md"))
        if len(matches) != 1:
            errors.append(
                f"{arguments.directory}: item {number:03d} has {len(matches)} files"
            )
            continue
        errors.extend(validate_note(matches[0]))

    if errors:
        raise SystemExit("\n".join(errors))
    print(
        f"validated {arguments.last - arguments.first + 1} notes: "
        f"{arguments.first:03d}-{arguments.last:03d}"
    )


if __name__ == "__main__":
    main()
