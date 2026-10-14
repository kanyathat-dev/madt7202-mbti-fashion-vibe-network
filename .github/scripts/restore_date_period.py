import json
from pathlib import Path
import fitz

# 1) Restore the Notebook's data/coding period while preserving the capture-day distinction.
notebook = Path("MBTI_Fashion_Room_Network_Analytics.ipynb")
raw = notebook.read_text(encoding="utf-8")
json.loads(raw)
old_sentence = "collected from **27 September 2026** across six anonymized creator accounts (Creators A–F)."
new_sentence = (
    "captured on **27 September 2026** across six anonymized creator accounts (Creators A–F). "
    "AI-assisted coding and dataset preparation continued from **27 September to 7 October 2026**."
)
if old_sentence not in raw:
    raise RuntimeError("Expected single-day sentence was not found in the notebook.")
raw = raw.replace(old_sentence, new_sentence, 1)
json.loads(raw)
notebook.write_text(raw, encoding="utf-8")
print("Notebook date narrative restored.")

# 2) Restore the date period in the one-page report PDF without changing hyperlinks.
pdf = Path("6810424002_Kanyathat Rakdee_MBTI_Fashion_Room_Network_Analytics_Midterm.pdf")
doc = fitz.open(pdf)
old_date = "27 September 2026"
new_date = "27 September to 7 October 2026"
hits = [(page, rect) for page in doc for rect in page.search_for(old_date)]
if len(hits) != 1:
    raise RuntimeError(f"Expected one date string in the report PDF, found {len(hits)}")
page, rect = hits[0]
fontsize = 7.245
page.add_redact_annot(rect, fill=(1, 1, 1), cross_out=False)
page.apply_redactions(images=0, graphics=0)
page.insert_text(
    (rect.x0, rect.y0 + fontsize * 0.9282),
    new_date,
    fontname="hebo",
    fontsize=fontsize,
    color=(39/255, 41/255, 42/255),
    overlay=True,
)
tmp = pdf.with_suffix(".tmp.pdf")
doc.save(tmp, garbage=4, deflate=True)
doc.close()
tmp.replace(pdf)

check = fitz.open(pdf)
text = "\n".join(page.get_text() for page in check)
if len(check) != 1 or text.count(new_date) != 1:
    raise RuntimeError("PDF period/page-count validation failed")
uris = [link.get("uri", "") for page in check for link in page.get_links()]
required = [
    "https://www.myersbriggs.org/my-mbti-personality-type/the-16-mbti-personality-types/",
    "https://colab.research.google.com/drive/1a6PxetaHc75K0ae7KYHsezqhQ93kY9j9",
    "https://github.com/kanyathat-dev/madt7202-mbti-fashion-vibe-network",
]
if not all(url in uris for url in required):
    raise RuntimeError(f"PDF link validation failed: {uris}")
check.close()
print("Report PDF period restored; one page and all three hyperlinks verified.")
