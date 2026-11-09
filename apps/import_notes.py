#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
把每天的笔记导进记忆服务（8790）

切法：一行 "- " 开头的算一条，前面挂上日期。
重复导入不会产生重复，靠 sha 去重（这里简单用文本比对）。
"""

import glob
import json
import os
import re
import urllib.request

NOTES = r"C:\Users\w2423\.dsh\bili-duty\notes"
API = "http://127.0.0.1:8790"
SEEN = os.path.join(os.path.dirname(os.path.abspath(__file__)), "imported.txt")


def post(path, obj):
    body = json.dumps(obj, ensure_ascii=False).encode("utf-8")
    req = urllib.request.Request(API + path, data=body, headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=10) as resp:
        return json.loads(resp.read().decode("utf-8"))


def load_seen():
    if not os.path.exists(SEEN):
        return set()
    with open(SEEN, "r", encoding="utf-8") as f:
        return {line.strip() for line in f if line.strip()}


def memo(text):
    import hashlib
    return hashlib.sha256(text.encode("utf-8")).hexdigest()[:16]


def main():
    seen = load_seen()
    added = 0
    files = sorted(glob.glob(os.path.join(NOTES, "*.md")))
    for path in files:
        day = os.path.splitext(os.path.basename(path))[0]
        with open(path, "r", encoding="utf-8") as f:
            raw = f.read()
        for line in raw.splitlines():
            line = line.strip()
            if not line.startswith("- "):
                continue
            body = line[2:].strip()
            # 去掉行首的时间戳（"10:50 "），日期统一用文件名
            body = re.sub(r"^\d{1,2}:\d{2}\s+", "", body)
            if len(body) < 10:
                continue
            text = f"{day} {body}"
            h = memo(text)
            if h in seen:
                continue
            post("/write", {"text": text, "importance": 0.55, "source": "note"})
            with open(SEEN, "a", encoding="utf-8") as f:
                f.write(h + "\n")
            seen.add(h)
            added += 1
    print(f"导入 {added} 条，共扫 {len(files)} 个笔记文件")
    print(json.dumps(post("/health", {}), ensure_ascii=False))


if __name__ == "__main__":
    main()
