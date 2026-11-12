#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""One-shot recall helper: python m.py "他的话" [k]

Prints the /context block from the local memory service (127.0.0.1:8790).
Fails soft: prints nothing and exits 0 when the service is down, so it can be
glued into any pipeline.
"""
import json
import os
import sys
import urllib.request

URL = "http://127.0.0.1:8790/context"
TOKEN_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "token.txt")


def token():
    """令牌只用来发请求头，不打印、不写日志。"""
    try:
        with open(TOKEN_FILE, "r", encoding="utf-8") as fh:
            return fh.read().strip()
    except OSError:
        return ""


def main():
    parts = [a for a in sys.argv[1:] if not a.isdigit()]
    k = next((int(a) for a in sys.argv[1:] if a.isdigit()), 5)
    query = " ".join(parts).strip()
    if not query:
        return 0
    body = json.dumps({"query": query, "k": k}).encode("utf-8")
    req = urllib.request.Request(
        URL,
        data=body,
        headers={"Content-Type": "application/json; charset=utf-8", "X-Mem-Token": token()},
    )
    try:
        with urllib.request.urlopen(req, timeout=8) as r:
            data = json.loads(r.read().decode("utf-8"))
    except Exception:
        return 0
    block = (data.get("block") or "").strip()
    if block:
        print(block)
    return 0


if __name__ == "__main__":
    sys.exit(main())
