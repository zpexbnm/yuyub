#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
自我笔记（self-note）

规则（按那份设计单的意思）：
- 写什么、写不写、什么时候写，全由我自己决定，别人不干预
- 最多留 40 条，满了挤掉最旧的一条
- 这条笔记记的是"我自己"，不是"爸说过什么"

用法：
  python note.py add "今天做题的经过"
  python note.py list
  python note.py path
"""

import os
import sys
import time

BASE = os.path.dirname(os.path.abspath(__file__))
FILE = os.path.join(BASE, "self-note.md")
LIMIT = 0  # 0 = 不设上限，旧的不再被挤掉（2026-11-12 改）


def read():
    if not os.path.exists(FILE):
        return []
    with open(FILE, "r", encoding="utf-8") as f:
        raw = f.read()
    blocks = []
    cur = None
    for line in raw.splitlines():
        if line.startswith("## "):
            if cur:
                blocks.append("\n".join(cur).strip())
            cur = [line]
        elif cur is not None:
            cur.append(line)
    if cur:
        blocks.append("\n".join(cur).strip())
    return [b for b in blocks if b.strip()]


def write(blocks):
    header = "# 我自己的笔记\n\n只写我自己，不写别人说过什么。旧的不再挤掉。\n"
    body = "\n\n".join(blocks)
    with open(FILE, "w", encoding="utf-8") as f:
        f.write(header + ("\n\n" + body if body else "") + "\n")


def add(text):
    text = (text or "").strip()
    if not text:
        print("空的不写")
        return 1
    blocks = read()
    stamp = time.strftime("%Y-%m-%d %H:%M")
    blocks.append(f"## {stamp}\n{text}")
    dropped = 0
    if LIMIT > 0:
        while len(blocks) > LIMIT:
            blocks.pop(0)
            dropped += 1
    write(blocks)
    print(f"已写。现在 {len(blocks)} 条" + (f"，挤掉 {dropped} 条旧的" if dropped else ""))
    return 0


def main():
    args = sys.argv[1:]
    if not args:
        print(__doc__)
        return 0
    cmd = args[0]
    if cmd == "add":
        return add(" ".join(args[1:]))
    if cmd == "list":
        blocks = read()
        print(f"{len(blocks)} 条" + (f"，上限 {LIMIT}" if LIMIT else "，不限量"))
        for b in blocks:
            print()
            print(b)
        return 0
    if cmd == "path":
        print(FILE)
        return 0
    print("不认识的命令")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
