# MBTI–Fashion Vibe Network: Living Room Anchor & Compromise Bridge for Newlyweds

**Course:** MADT7202 — Web & Social Network Analytics (Midterm Project)  
**Author:** Kanyathat Rakdee  
**Student ID:** 6810424002  
**Data and coding period:** 27 September to 7 October 2026

## Project Overview

This project explores how a bipartite network can support early-stage identification of a potential **Living Room Anchor** and **Compromise Bridge** for newlywed couples whose MBTI labels differ. The notebook analyzes observed co-occurrence patterns between MBTI labels and Fashion Vibe categories and translates them into hypotheses for furniture collection planning and a future style-recommendation tool.

**Business question:** When two people have different MBTI labels and no shared direct Fashion Vibe in the observed data, which style could provide a useful starting point for a shared living-room direction?

This is an exploratory network analysis. It does not establish that MBTI causes aesthetic preferences, validate individuals' personality types, or prove relationship compatibility. Recommendations remain hypotheses that require validation with real customers.

## Project Files

- **[Final English Report (PDF)](./6810424002_Kanyathat%20Rakdee_MBTI_Fashion_Room_Network_Analytics_Midterm.pdf)** — one-page report with the business decision, data and bias controls, graph construction, findings, recommended actions, and limitations.
- **[Jupyter Notebook](./MBTI_Fashion_Room_Network_Analytics.ipynb)** — notebook with the project narrative and analysis code.
- **[Open in Google Colab](https://colab.research.google.com/drive/1a6PxetaHc75K0ae7KYHsezqhQ93kY9j9)** — run and inspect the analysis interactively.

## Analytical Pipeline

### 1. Data and Audit Trail
- 67 public TikTok lookbook images captured on **27 September 2026** from six anonymized creator accounts (A–F); AI-assisted coding and dataset preparation continued through **7 October 2026**.
- The notebook reads `data/raw_image_268_rows.csv` as the source of truth: 268 evidence rows across 67 image IDs (four coded observations per image).
- Image-level sample size: **N = 67**; the 268 evidence rows are not independent source images.
- Assertions check the row count, one row per `_L1` through `_L4` suffix per image ID, stable labels within each image group, a one-to-one raw-name / proxy-name mapping, and all 16 MBTI labels / 12 Fashion Vibe categories. The notebook checks raw filenames against the repository image directory and records the source CSV SHA-256. This verifies file presence and the mapping declared by the CSV, not independently verified pixel-level correspondence between raw images and proxy filenames.

### 2. Analyze and Network Topology
- Bipartite graph with 16 MBTI nodes and 12 Fashion Vibe nodes.
- Edge weights use image-level Normalized Pointwise Mutual Information (NPMI).
- Retain observed edges with **NPMI > 0**.
- Shortest-path distance: **d = 1/NPMI** for retained positive-weight edges.
- Examine node degree, MBTI-pair coverage, betweenness centrality, shortest-path mediation, and leave-one-creator-out sensitivity.

### 3. Visualize and Explore the Recommendation Concept
The notebook includes code for:
- A labeled MBTI–Fashion Vibe network figure and an ESTJ–INFP shortest-path illustration.
- A Couple Matcher that explores shared Vibes or indirect paths for a selected MBTI pair.
- An interactive network HTML view for examining nodes, connected entities, and edge weights.

Generated files are written by the notebook when the relevant code executes successfully:
- `image_mapping_audit.csv` — one row per raw image with mapping caveat and repository-presence check
- `mbti_fashion_coded_data_audit.csv` and `mbti_fashion_image_level.csv`
- `mbti_vibe_network_metrics.csv`
- `leave_one_creator_out_sensitivity.csv` and `npmi_threshold_sensitivity.csv`
- `mbti_network_topology_labeled.png` and `mbti_fashion_vibe_network.html`

## Findings Reported in the Notebook

- **Clean-Traditional** is explored as a Living Room Anchor candidate (degree 8; reported MBTI-pair coverage 28/120, or 23.3%).
- **Playful-Streetwear** is the baseline Compromise Bridge candidate (weighted betweenness **0.3134**; Bridge Load **33.0 fractional path-load units**).
- **58 of 120 MBTI pairs (48.3%)** have no shared direct Fashion Vibe in the observed network. This percentage is distinct from Bridge Load; the latter sums fractional contributions over weighted shortest paths and is not a percentage of pairs.
- The notebook examines an ESTJ–INFP indirect mediation example, conducts six leave-one-creator-out runs, and varies minimum co-occurrence thresholds (1, 2, and 3). Threshold results include graph coverage, connected components, and unreachable pairs.

The notebook regenerates these metrics from the source CSV. Bridge Load is the accumulated fractional contribution over weighted shortest paths for no-overlap pairs, not a count of unique pairs or a percentage. Network centrality represents structure in this sample, not proof of consumer preference or relationship compatibility. The leave-one-creator-out sensitivity changes the top bridge in two of six runs; therefore the business recommendation is a shortlist to test, not a universal default.

## How to Run

1. Open the Google Colab notebook linked above or open `MBTI_Fashion_Room_Network_Analytics.ipynb` in a compatible Jupyter environment with internet access.
2. Select **Runtime → Run all**. The notebook downloads the committed CSV and queries the GitHub API to verify raw image filename presence.
3. Review the integrity output, network metrics, sensitivity tables, figure, Couple Matcher, and interactive network output. The notebook is split into data validation, image-level aggregation, network metrics, sensitivity analysis, static visualization, and interactive visualization cells.
4. Confirm that generated CSVs and figures exist and inspect all outputs. The notebook is executed by GitHub Actions and baseline assertions check 268 evidence rows, 67 images, 28 graph nodes, 51 retained edges, weighted betweenness 0.3134, Bridge Load 33.0, and 58/120 no-overlap pairs (48.3%). Do not silently alter results to force agreement with a narrative.

## Data, Coding, and Reference Notes

- Creator accounts are anonymized as A–F.
- MBTI labels were taken from the source content and were not independently validated as psychological assessments.
- Gemini assisted with Fashion Vibe attribute coding and supporting evidence.
- Fashion Vibe categories and the 1:1 interpretation to potential room-style directions are researcher-defined coding decisions, not official MBTI classifications.
- The official Myers & Briggs Foundation overview of the 16 personality types is available at [The 16 MBTI Personality Types](https://www.myersbriggs.org/my-mbti-personality-type/the-16-mbti-personality-types/). This reference does not validate labels in the social-media sample or establish a relationship between MBTI and Fashion Vibe.

## Limitations

The sample is small and concentrated among a subset of creators. Results depend on source content, coding decisions, the positive-NPMI pruning rule, and the inverse-weight distance transformation. Missing edges do not prove that a preference does not exist outside the sample. A proposed test with couples is future validation, not a completed experiment.

## Repository Contents

- [`6810424002_Kanyathat Rakdee_MBTI_Fashion_Room_Network_Analytics_Midterm.pdf`](./6810424002_Kanyathat%20Rakdee_MBTI_Fashion_Room_Network_Analytics_Midterm.pdf) — final English one-page report.
- [`MBTI_Fashion_Room_Network_Analytics.ipynb`](./MBTI_Fashion_Room_Network_Analytics.ipynb) — project narrative and end-to-end analysis code.
- `README.md` — project framing, pipeline, reported findings, run instructions, and limitations.


## Reproducibility checks

The notebook regenerates the coded-data audit, image-level table, network metrics, leave-one-creator-out results, threshold sensitivity results, static figure, and interactive network HTML. A GitHub Actions workflow executes the notebook and checks baseline outputs when the notebook, source CSV, or workflow changes. The 67-row mapping audit is committed at [`data/image_mapping_audit.csv`](./data/image_mapping_audit.csv).
