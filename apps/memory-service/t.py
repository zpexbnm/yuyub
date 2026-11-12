#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""看流水：python t.py [条数]

只读，不改。服务没起或令牌不对就打印一行提示，退出码 0。
"""
import json
import os
import sys
import urllib.request

URL = "http://127.0.0.1:8790/timeline?limit="
TOKEN_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "token.txt")


def token():
    """令牌只发在请求头里，不打印。"""
    try:
        with open(TOKEN_FILE, "r", encoding="utf-8") as fh:
            return fh.read().strip()
    except OSError:
        return ""


def main():
    n = int(sys.argv[1]) if len(sys.argv) > 1 and sys.argv[1].isdigit() else 20
    req = urllib.request.Request(URL + str(n), headers={"X-Mem-Token": token()})
    try:
        with urllib.request.urlopen(req, timeout=6) as r:
            data = json.loads(r.read().decode("utf-8"))
    except Exception as exc:
        print("流水读不到：", exc)
        return 0
    rows = data.get("events") or []
    if not rows:
        print("还空着")
        return 0
    for e in rows:
        print(f"{e['when']}  {e['actor'] or '?':<6} {e['summary']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
