# Raw Lookbook Images

**Project:** MADT7202 — MBTI–Fashion Vibe Network  
**Capture date:** 27 September 2026 (single-day capture)

> **Ingestion status:** This folder has been created for the dataset, but the raw-image set is not yet complete. Do not treat the repository as containing the full 67-image dataset until all 67 uniquely mapped JPEG files are present and the generated manifest passes validation.

## Purpose and source

This directory is the designated location for the **67 raw lookbook images** collected from public TikTok content across six anonymized creators (Creators A–F) on **27 September 2026**. These images are the source-level evidence for the **268 coded attribute observations** used in the MADT7202 MBTI–Fashion Vibe Network analysis (four coded attributes per image).

## File naming and data lineage

Each image must be stored as a JPEG named exactly after its `image_id`, for example `IMG_INTJ_001.jpg`. The filename without `.jpg` must match the `image_id` in both `mbti_fashion_coded_data_audit.csv` and `mbti_fashion_image_level.csv`.

Keep the ID values already present in the Notebook/data; do not renumber IDs merely to make the suffixes contiguous. Some IDs in the current Notebook have numeric gaps, so matching the dataset takes priority over renumbering.

After preparation, `image_manifest.csv` should record each `image_id`, output filename, source/output SHA-256 hashes, source format, dimensions, and output size. `SHA256SUMS.txt` should provide file-integrity checksums. Do not include creator usernames, account handles, profile URLs, or other account identifiers in image filenames or the manifest. Use only anonymized Creator A–F labels in separate coding materials.

## Privacy and handling

The standardized file naming and manifest must not store usernames or source-account identifiers. The preparation workflow re-encodes source images as JPEG without carrying over EXIF metadata. This does not automatically remove any visible username, watermark, or account identifier embedded in the pixels; inspect each image before public release and redact visible identifying overlays where required by the course or applicable permissions. Keep the original source files separately and preserve this folder as the standardized analysis copy.

## Completeness and audit checks

The directory is complete only when it contains exactly **67 uniquely mapped JPEG files**, one for each distinct `image_id`, with no missing IDs, reused source files, byte-identical source duplicates, or overwrites. The validation script should check the Notebook ID set, compare IDs with `mbti_fashion_image_level.csv`, and verify that `mbti_fashion_coded_data_audit.csv` has 268 rows with four attribute rows per `image_id`.

The 67-image / 268-observation relationship means four coded attributes are associated with each source image. The 268 attribute rows must not be treated as 268 independent images; the image-level unit of analysis remains **N = 67**.
