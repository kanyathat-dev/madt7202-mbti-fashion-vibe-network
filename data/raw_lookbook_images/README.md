# Raw Lookbook Images and Coding Methodology

**Project:** MADT7202 — MBTI–Fashion Vibe Network  
**Image capture date:** 27 September 2026  
**AI-assisted coding and data preparation period:** 27 September to 7 October 2026  
**Raw source images:** 67 files from six anonymized creator groups (Creators A–F)

## 1. Purpose and source

This directory contains the 67 raw lookbook image files used as visual source material for the MADT7202 MBTI–Fashion Vibe Network project. The images were captured from public TikTok lookbook content on **27 September 2026**. AI-assisted coding, evidence review, and preparation of the dataset continued through **7 October 2026**.

The files retain their raw UUID-style names (for example, `temp_image_<UUID>.WEBP`) so that the source files can be distinguished from the coding labels created during analysis. Creator usernames, account handles, and profile URLs are not used as identifiers in the dataset documentation; creator references use anonymized labels A–F.

The folder intentionally retains the 67 uploaded source files as supplied. The count of 67 files is a file count and is not, by itself, a claim that all files contain unique pixel content.

## 2. Image-to-data pipeline

The project transforms the source images into network-analysis data through four stages:

```text
67 raw TikTok lookbook images
          |
          v
1. Visual Feature Extraction
   4 observed clothing attributes per image
          |
          v
268 attribute-level observations
   with written visual evidence
          |
          v
2. Fashion Vibe Synthesis
   1 researcher-defined Fashion Vibe per image
          |
          v
3. Image-Level Aggregation (N = 67)
   group observations by their source image ID
          |
          v
4. Cross-Domain Mapping and Graph Construction
   Fashion Vibe -> Room Style; MBTI x Vibe network using NPMI
```

### Step 1 — Visual Feature Extraction (Gemini-assisted multimodal coding)

Gemini was used to inspect each lookbook image and help record four observable clothing attributes:

1. **Silhouette / Structure** — overall shape, cut, and structure of the outfit.
2. **Fabric / Texture** — visible material and surface texture.
3. **Key Garments** — principal clothing items and accessories.
4. **Palette / Pattern** — visible colors, contrast, and patterns.

A written **Evidence** description records visible details supporting the coded attributes. The resulting coding sheet contains **268 attribute-level observations** (67 images × 4 observations per image).

### Step 2 — Fashion Vibe Synthesis

The four attribute observations for an image are considered together to assign one primary category from the project's **12 researcher-defined Fashion Vibes**. For example, a structured blazer, sharp tailoring, and formal leather footwear may support a `Sharp-Tailored` classification. These labels are the project's own coding framework; they are not official fashion categories defined by the MBTI organization.

### Step 3 — Image-Level Aggregation

The 268 attribute rows are supporting evidence, not 268 separate source images. Before network analysis, records are grouped by the corresponding source image ID so that the image-level analytical unit remains **N = 67**. This step is intended to prevent counting the four attribute rows from one image as four independent images.

Coded IDs that use suffixes such as `_L1` through `_L4` refer to the four coded attribute records associated with one lookbook image. They **do not** mean that the original image was physically cropped into four separate image files.

### Step 4 — Cross-Domain Mapping and Graph Construction

The project uses a researcher-defined 1:1 mapping from a Fashion Vibe to a proposed living-room style (Room Style), then examines the co-occurrence between MBTI labels and Fashion Vibes using **Normalized Pointwise Mutual Information (NPMI)** to construct a bipartite network. The Fashion Vibe-to-Room Style mapping is a design hypothesis for this project, not an official relationship published by the MBTI organization.

## 3. Role of The Myers-Briggs Company framework

The [official descriptions of the 16 MBTI personality types from The Myers-Briggs Company](https://www.myersbriggs.org/my-mbti-personality-type/the-16-mbti-personality-types/) are used as a common reference for the project’s MBTI terminology and coding documentation. The project coding reference records official type summaries and core keywords in the `mbti_official_summary` and `mbti_core_keywords` fields of the coding/audit workflow.

This reference has three methodological purposes:

- **Consistent terminology:** provide a shared reference for interpreting the MBTI labels appearing in the source content.
- **Coding guidance:** make the reasoning behind the project’s MBTI-related labels easier to document and review alongside the visual evidence.
- **Auditability:** retain a documented reference point that reviewers can compare with the project’s observation-level evidence.

**Scope and claim discipline:** using an official MBTI description as a reference does not independently verify the personality type of the person in an image, prove that an MBTI type determines clothing preferences, or establish that a person will prefer a particular interior style. The MBTI labels are labels presented in the social-media content, not results independently validated by a psychological assessment. Fashion Vibes and Room Styles are researcher-defined categories, and The Myers-Briggs Company does not endorse the project’s fashion or interior-style mappings.

The MBTI reference is a coding-grounding aid; it does **not** remove creator-level sampling bias. The source set is unevenly distributed across creators (65 of the 67 images are reported as coming from four main creators, Creators A–D). The project's creator-sensitivity check, such as Leave-One-Creator-Out analysis, is the separate procedure used to examine how conclusions may depend on creator composition.

## 4. Mapping sheet and data lineage

The attribute-level mapping sheet is stored at [`data/raw_image_268_rows.csv`](../raw_image_268_rows.csv). It links each row to a raw filename and a Gemini-converted filename and contains these fields:

- `Raw Name`
- `Gemini Converted Filename`
- `Coded Image ID`
- `MBTI`
- `Creator`
- `Fashion Vibe`
- `Room Style`
- `Evidence`

The mapping sheet has 268 attribute-level rows. The `Raw Name` field identifies the source file; `Gemini Converted Filename` is a coding/proxy label, not proof that a separate image file was created from each observation. If a raw-file-to-proxy association was inferred during reconstruction rather than independently recorded at collection time, it should be treated as a mapping hypothesis until checked against the image and its evidence. Preserve the raw filenames and do not silently replace them with proxy names.

## 5. Privacy and handling

The project documentation uses anonymized creator labels A–F and does not list account usernames or profile URLs. File names alone do not guarantee that image pixels are anonymized: visible handles, watermarks, or other identifying overlays may remain inside an image. Review image contents and confirm that public redistribution is appropriate under course requirements and applicable permissions before sharing widely.

## 6. Audit checks and limitations

- **67 raw files** are retained in this directory.
- The mapping sheet contains **268 attribute-level rows**—four records per coded image ID.
- The unit of analysis for network construction is the image-level record (**N = 67**), not the 268 attribute rows.
- Exact duplicate files, if present, are retained in the raw folder as requested; the file count should not be interpreted as a count of 67 pixel-unique images. Duplicate content can affect frequency-based analyses, so it is a limitation to acknowledge rather than conceal.
- The raw UUID-to-Gemini-name relationship should be interpreted according to its evidence level; inferred pairings are not equivalent to an original collection-time filename log.
- MBTI labels, Fashion Vibes, and Room Styles serve the project’s social-media image-analysis and business-simulation purpose. The network does not establish psychological causation or validated real-world consumer preferences.
