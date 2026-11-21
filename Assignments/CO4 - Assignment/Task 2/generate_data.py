"""Creates the sample daily biometric files used by Tasks 2 and 5 (deterministic)."""
from pathlib import Path

OUT = Path(__file__).parent / "data" / "2026-10"
OUT.mkdir(parents=True, exist_ok=True)
students = ["192311001", "192311002", "192311003", "192311004", "192311005", "192311006"]
pattern = {  # status per day Mon-Fri 5..9 Oct 2026
    "192311001": "PPPPP", "192311002": "PAPPP", "192311003": "AAAPP",
    "192311004": "PPAPA", "192311005": "PPPAP", "192311006": "AAPAA",
}
days = ["2026-10-05", "2026-10-06", "2026-10-07", "2026-10-08", "2026-10-09"]
for i, d in enumerate(days):
    lines = [f"{s},{d},{pattern[s][i]}" for s in students]
    if d == "2026-10-07":                       # damaged lines
        lines[1] = "192311002,2026-10-07"       # missing status
        lines[3] = "192311004,2026-10-07,X"     # wrong status letter
    text = "\n".join(lines) + "\n"
    if d == "2026-10-09":
        text += "\n"                            # empty last line
    (OUT / f"attendance_{d}.txt").write_text(text, encoding="utf-8")
print("created", len(days), "files in", OUT)
