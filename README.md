# MBTI–Fashion Vibe Network: Living Room Anchor & Compromise Bridge for Newlyweds

**Course:** MADT7202 — Web & Social Network Analytics (Midterm Project)  
**Author:** Kanyathat Rakdee  
**Student ID:** 6810424002  
**Image capture date:** 27 September 2026 (single-day capture)

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
- 67 public TikTok lookbook images captured from six anonymized creator accounts (A–F) on **27 September 2026**.
- Four coded attributes per image: 268 attribute observations in total.
- Image-level sample size: **N = 67**; attribute rows are not independent images.
- Data-integrity assertions check expected row and image counts, four attributes per image, one Fashion Vibe per image, and 16 MBTI labels / 12 Fashion Vibe categories.

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
- `mbti_fashion_coded_data_audit.csv`
- `mbti_fashion_image_level.csv`
- `mbti_network_topology_labeled.png`
- `mbti_fashion_vibe_network.html`

## Findings Reported in the Notebook

- **Clean-Traditional** is explored as a Living Room Anchor candidate (degree 8; reported MBTI-pair coverage 28/120, or 23.3%).
- **Playful-Streetwear** is explored as a Compromise Bridge candidate (reported weighted betweenness 0.3134; reported bridge load 34.8/58 no-overlap pairs, or 48.3%).
- **58 of 120 MBTI pairs (48%)** are reported as having no shared direct Fashion Vibe in the observed network.
- The notebook examines an ESTJ–INFP indirect mediation example and conducts six leave-one-creator-out runs.

These values are reported by the current notebook narrative and should be checked against the executed outputs before being treated as final. Network centrality represents structure in this sample, not proof of consumer preference or relationship compatibility.

## How to Run

1. Open the Google Colab notebook linked above or open `MBTI_Fashion_Room_Network_Analytics.ipynb` in a compatible Jupyter environment.
2. In Colab, select **Runtime → Run all**.
3. Wait for execution to finish and inspect the data-integrity checks, network metrics, figure, Couple Matcher, and interactive network output.
4. Confirm that the executed outputs match the values described in the notebook before citing them in the report.

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
