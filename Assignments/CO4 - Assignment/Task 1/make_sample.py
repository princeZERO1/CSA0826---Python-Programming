"""Creates mess_oct.txt (small, with problems) and mess_big.txt (50,000 lines)."""
from pathlib import Path
here = Path(__file__).parent
small = ["192311001,Anita,1250.50", "192311002,Bala,1800", "192311003,Chitra,abc",
         "192311004,Dev", "192311005,Esha,2100.75", ""]
(here / "mess_oct.txt").write_text("\n".join(small) + "\n", encoding="utf-8")
with open(here / "mess_big.txt", "w", encoding="utf-8") as f:
    for i in range(50000):
        f.write(f"19{i:07d},Student{i},{1000 + i % 900}.{i % 100:02d}\n")
print("samples created")
