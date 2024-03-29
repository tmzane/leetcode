#!/usr/bin/env python3

import os
import re
from dataclasses import dataclass


@dataclass
class Problem:
    link: str
    number: int
    title: str
    difficulty: str
    file: str
    test: str = ""


TEMPLATE = """\
# leetcode

[![checks](https://github.com/tmzane/leetcode/actions/workflows/checks.yml/badge.svg)](https://github.com/tmzane/leetcode/actions/workflows/checks.yml)

My [LeetCode](https://leetcode.com) solutions written in Go.

## Progress

### Total

| Easy | Medium | Hard |
|:----:|:------:|:----:|
|{Easy}|{Medium}|{Hard}|

### Solutions

|  #  | Title | Difficulty | Solution | Tests |
|:---:|:------|:----------:|:--------:|:-----:|
"""


def main() -> None:
    problems: list[Problem] = []
    total: dict[str, int] = {"Easy": 0, "Medium": 0, "Hard": 0}

    for filename in sorted(os.listdir()):
        if not re.fullmatch(r"^[0-9]{4}[a-z_]+.go$", filename):
            continue

        with open(filename) as f:
            link = f.readline().removeprefix("// ").removesuffix("\n")
            f.readline()
            header = f.readline().removeprefix("// ").removesuffix("\n")

        # the header consists of the task's number, name and difficulty.
        pattern = r"^([0-9]{4})\. ([a-zA-Z ()]+) \[(Easy|Medium|Hard)\]$"
        match = re.fullmatch(pattern, header)
        assert match is not None

        number = int(match.group(1))
        title = match.group(2)
        difficulty = match.group(3)
        file = f"[👀]({filename})"

        p = Problem(link, number, title, difficulty, file)
        problems.append(p)
        total[p.difficulty] += 1

    with open("solutions_test.go") as f:
        it = iter(problems)
        for i, line in enumerate(f):
            if re.match(r"^// [0-9]{4}\.", line):
                next(it).test = f"[✅](solutions_test.go#L{i + 1})"

    with open("README.md", "w") as f:
        f.write(TEMPLATE.format(**total))
        for p in problems:
            f.write(f"|{p.number}|[{p.title}]({p.link})|{p.difficulty}|{p.file}|{p.test}|\n")


if __name__ == "__main__":
    main()
