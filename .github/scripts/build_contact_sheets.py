from pathlib import Path
from PIL import Image, ImageOps, ImageDraw, ImageFont
import csv, math

src = Path("data/raw_lookbook_images")
out = Path(".tmp_contact_sheets")
out.mkdir(exist_ok=True)
files = sorted([p for p in src.iterdir() if p.is_file() and p.name.lower().startswith("temp_image_")])
if len(files) != 67:
    raise RuntimeError(f"Expected 67 raw images, found {len(files)}")

with (out / "image_index.csv").open("w", newline="", encoding="utf-8-sig") as f:
    w = csv.writer(f)
    w.writerow(["index", "raw_name"])
    for i, p in enumerate(files, 1):
        w.writerow([i, p.name])

font = ImageFont.load_default()
thumb_w, thumb_h = 220, 280
card_h = 322
cols, per_page = 4, 16

for page_idx in range(math.ceil(len(files) / per_page)):
    chunk = files[page_idx * per_page : (page_idx + 1) * per_page]
    rows = math.ceil(len(chunk) / cols)
    sheet = Image.new("RGB", (cols * thumb_w, rows * card_h), "white")
    draw = ImageDraw.Draw(sheet)
    for j, p in enumerate(chunk):
        im = Image.open(p).convert("RGB")
        im.thumbnail((thumb_w - 8, thumb_h - 8))
        x = (j % cols) * thumb_w
        y = (j // cols) * card_h
        sheet.paste(im, (x + (thumb_w - im.width)//2, y + 3))
        index = page_idx * per_page + j + 1
        # Filename split into shorter two lines so it remains associated with the image.
        stem = p.name
        line1 = stem[:27]
        line2 = stem[27:]
        draw.text((x + 4, y + thumb_h + 2), f"{index:02d}. {line1}", fill="black", font=font)
        draw.text((x + 4, y + thumb_h + 17), line2, fill="black", font=font)
    target = out / f"sheet_{page_idx+1:02d}.jpg"
    sheet.save(target, "JPEG", quality=72, optimize=True)
    print(target, target.stat().st_size)
