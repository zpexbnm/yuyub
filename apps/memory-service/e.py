#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""记一条流水：python e.py "做了什么" [类型]

类型默认「操作」。令牌只读文件、只发请求头。
"""
import json
import os
import sys
import urllib.request

URL = "http://127.0.0.1:8790/event"
TOKEN_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "token.txt")


def token():
    try:
        with open(TOKEN_FILE, "r", encoding="utf-8") as fh:
            return fh.read().strip()
    except OSError:
        return ""


def main():
    if len(sys.argv) < 2:
        print("用法：python e.py \"做了什么\" [类型]")
        return 1
    summary = sys.argv[1].strip()
    kind = sys.argv[2] if len(sys.argv) > 2 else "操作"
    body = json.dumps({"actor": "小鱼", "kind": kind, "summary": summary, "ref": "e.py"},
                      ensure_ascii=False).encode("utf-8")
    req = urllib.request.Request(
        URL, data=body,
        headers={"Content-Type": "application/json; charset=utf-8", "X-Mem-Token": token()},
    )
    try:
        with urllib.request.urlopen(req, timeout=8) as r:
            data = json.loads(r.read().decode("utf-8"))
    except Exception as exc:
        print("没记上：", exc)
        return 1
    print("记上了", data.get("id"))
    return 0


if __name__ == "__main__":
    sys.exit(main())
