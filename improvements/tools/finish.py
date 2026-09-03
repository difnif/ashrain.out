# 완료된 zip의 산출을 재검증하고 PROGRESS.md에 행을 추가 (중복 방지)
import sys, json, subprocess, datetime, re
zn, mod = sys.argv[1], sys.argv[2]
out = subprocess.run(["python3", "/root/esc/build_out.py", zn, mod], capture_output=True, text=True).stdout
assert "missing 0" in out and "검산 불통과" not in out, out[-2000:]
subprocess.run(["python3", "/root/esc/reverify.py", zn], check=True)
row = [l for l in out.splitlines() if l.startswith("| ")][-1]
p = open("/root/esc/PROGRESS.md", encoding="utf-8").read()
if f"| {zn} |" in p:
    p = re.sub(rf"\| {re.escape(zn)} \|.*\n", row + "\n", p)
else:
    p = p.rstrip("\n") + "\n" + row + "\n"
open("/root/esc/PROGRESS.md", "w", encoding="utf-8").write(p)
print(row)
