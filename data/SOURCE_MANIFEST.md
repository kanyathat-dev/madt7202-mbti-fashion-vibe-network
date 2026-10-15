# Data Provenance and Collection Protocol

**Project:** MADT7202 — MBTI–Fashion Vibe Network  
**Dataset:** 67 TikTok lookbook images; 268 coded observations  
**Purpose:** Document the reported collection workflow, sampling decisions, privacy handling, and the limits of what can be independently reproduced from the repository.

## 1. Source and collection method

The project used public TikTok fashion-lookbook content. The collection notes supplied for this project describe manual retrieval through the public web interface rather than an automated scraper. The recorded discovery queries included:

- `#mbtioutfits`
- `#mbtifashion`
- `#ootd`

### Selection criteria recorded for the project

1. The source content was publicly accessible.
2. The lookbook explicitly associated an outfit with a four-letter MBTI label.
3. The outfit was sufficiently clear to identify garment attributes.
4. Each image represented one distinct lookbook outfit for image-level analysis.

The project narrative records 27 September 2026 as the image-capture date and 7 October 2026 as the end of the coding/data-preparation period. The full working period is therefore recorded as 27 September–7 October 2026.

## 2. Units of analysis and volume

- **Image-level sample:** 67 images (`N = 67`).
- **Coded observations:** 268 observations, or four coded cues per image.
- **Network node sets:** 16 MBTI labels and 12 researcher-defined Fashion Vibe categories.
- **Creator labels:** six anonymized groups (A–F); 65 of 67 images came from four main creators.

The image is the unit used for network weighting. The 268 coded observations are not 268 independent source images.

## 3. Privacy and handling

The collection notes state that retrieval was manual, not performed with automated scrapers, headless browsers, or high-concurrency crawlers, and did not circumvent access controls. Creator labels were anonymized as A–F. Usernames and identifying account details were not retained in the analysis dataset. Coding focused on clothing attributes, not biometric identification.

These statements describe the recorded workflow. They do not by themselves establish that every possible use of the source content was permitted under all applicable platform terms or legal requirements.

## 4. Platform terms and auditability — an explicit documentation gap

The repository does **not** currently retain a complete set of original post URLs or a dated, item-level record showing which TikTok Terms of Service / Community Guidelines provisions were reviewed and what conclusion was reached.

Consequently, a reviewer can inspect the repository's stored data, anonymization choices, and filename audit, but cannot independently reconstruct every source post or verify a documented terms review for each item from this repository alone. Public accessibility is not treated here as proof of unrestricted permission. No claim of completed legal clearance is made without a supporting record.

For stronger future auditability, retain a private or appropriately access-controlled source log with the source URL, retrieval date, query or discovery route, selection decision, policy reviewed and review date, and a note on why the material was retained. Do not add personal identifiers that are not necessary for the audit trail, and do not publish source URLs if doing so would expose individuals contrary to the project's privacy approach.

## 5. Sampling limitations and single-source rationale

TikTok was chosen as a single source because short-form fashion lookbooks provide a relatively consistent visual format for garment-attribute coding. That is a scope and consistency decision, not evidence that the sample represents all fashion content.

The sample is purposive and creator-concentrated: 65/67 images originate from four primary creators. Curated lookbooks may over-represent coordinated, aspirational styling compared with everyday apparel choices. MBTI labels appearing in source content were not independently validated as psychometric assessments. Findings should not be generalized to all TikTok users, other platforms, offline purchasing behaviour, or relationship compatibility without external validation.

## 6. Files and reproducibility boundaries

- `data/raw_image_268_rows.csv`: four coded observations per image.
- `data/image_mapping_audit.csv`: declared raw-to-coded filename mapping and repository-presence audit.
- `data/raw_lookbook_images/`: raw image files retained in the repository.

The filename audit distinguishes three different claims:

1. A raw filename exists in the repository.
2. The CSV declares a mapping from the raw filename to a coded/proxy filename.
3. The coded/proxy image has been independently verified pixel-by-pixel against the original source post.

The current audit supports the first two claims; proxy-to-pixel correspondence is not independently verified.

## 7. Responsible interpretation

The network reports co-occurrence patterns in this coded sample. It does not establish causation, independently validate MBTI labels, or prove personal preferences or couple compatibility. Recommendations are hypotheses for future customer testing, not universal rules.
