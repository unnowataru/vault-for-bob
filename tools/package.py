"""配布用の zip を dist/ に作成する。使い方: python tools/package.py"""
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
FILES = ["SKILL.md", "README-for-Bob.md", "LICENSE", "examples/policy-bob-list.hcl", "examples/servers.csv"]

out = ROOT / "dist" / "vault-for-bob.zip"
out.parent.mkdir(exist_ok=True)
with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as z:
    for f in FILES:
        z.write(ROOT / f, f"vault-for-bob/{f}")
print(f"{out} ({out.stat().st_size:,} bytes, {len(FILES)} files)")
