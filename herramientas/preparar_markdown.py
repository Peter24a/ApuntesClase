import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "01_documento.md"
OUTPUT = ROOT / "tmp" / "01_documento-preparado.md"

lines = SOURCE.read_text(encoding="utf-8").splitlines()
prepared = []
separator = re.compile(r"^\|(?:\s*:?-+:?\s*\|)+\s*$")

for index, line in enumerate(lines):
    begins_table = (
        line.lstrip().startswith("|")
        and index + 1 < len(lines)
        and separator.match(lines[index + 1].strip())
    )
    if begins_table and prepared and prepared[-1].strip():
        prepared.append("")
    prepared.append(line)

OUTPUT.parent.mkdir(parents=True, exist_ok=True)
OUTPUT.write_text("\n".join(prepared) + "\n", encoding="utf-8")
print(OUTPUT)
