"""
src/maintenance/yara_rule_update.py

Automatically extends generated_rules.yar based on new malware samples
AND updates imphash_index.json.
"""

import json
from pathlib import Path
import pefile

RULES_DIR = Path("rules/yara")
META_DIR = Path("rules/metadata")
GEN_RULE = RULES_DIR / "generated_rules.yar"
IMP_PATH = META_DIR / "imphash_index.json"
MALWARE_DIR = Path("data/malware")


def rebuild_imphash_index():
    index = {}
    for f in MALWARE_DIR.rglob("*.exe"):
        try:
            pe = pefile.PE(str(f))
            imp = pe.get_imphash()
            index[imp] = f.name
        except Exception:
            continue

    META_DIR.mkdir(parents=True, exist_ok=True)
    with open(IMP_PATH, "w") as fp:
        json.dump(index, fp, indent=2)

    print(f"[YARA] Updated imphash_index.json with {len(index)} entries.")


def append_simple_rules():
    GEN_RULE.parent.mkdir(exist_ok=True, parents=True)
    with open(GEN_RULE, "w") as fp:
        for f in MALWARE_DIR.rglob("*"):
            if not f.is_file():
                continue
            fp.write(f'rule auto_{f.stem} {{ condition: filesize < 5MB }}\n')

    print("[YARA] Rebuilt generated_rules.yar")


def main():
    rebuild_imphash_index()
    append_simple_rules()
