import json
from pathlib import Path
import fitz

p = Path("MBTI_Fashion_Room_Network_Analytics.ipynb")
raw = p.read_text(encoding="utf-8")
json.loads(raw)
old = "27 September to 7 October 2026"
if old not in raw:
    raise SystemExit("Expected capture-date range not found in Notebook.")
raw = raw.replace(old, "27 September 2026")
p.write_text(raw, encoding="utf-8")
json.loads(p.read_text(encoding="utf-8"))

pdf = Path("6810424002_Kanyathat Rakdee_MBTI_Fashion_Room_Network_Analytics_Midterm.pdf")
doc = fitz.open(pdf)
hits = [(page, rect) for page in doc for rect in page.search_for(old)]
if len(hits) != 1:
    raise SystemExit(f"Expected one date range in report PDF; found {len(hits)}")
page, rect = hits[0]
size = 7.245
page.add_redact_annot(rect, fill=(1, 1, 1), cross_out=False)
page.apply_redactions(images=0, graphics=0)
page.insert_text((rect.x0, rect.y0 + size * 0.9282), "27 September 2026", fontname="hebo",
                 fontsize=size, color=(39/255, 41/255, 42/255))
tmp = pdf.with_suffix(".tmp.pdf")
doc.save(tmp, garbage=4, deflate=True)
doc.close()
tmp.replace(pdf)
check = fitz.open(pdf)
txt = "\n".join(pg.get_text() for pg in check)
uris = [link.get("uri", "") for pg in check for link in pg.get_links()]
assert old not in txt and "27 September 2026" in txt
assert len(check) == 1
assert all(u in uris for u in [
 "https://www.myersbriggs.org/my-mbti-personality-type/the-16-mbti-personality-types/",
 "https://colab.research.google.com/drive/1a6PxetaHc75K0ae7KYHsezqhQ93kY9j9",
 "https://github.com/kanyathat-dev/madt7202-mbti-fashion-vibe-network",
])
print("Updated Notebook and one-page PDF; all three links preserved.")
