# Replication Package: Domain-Driven Design in Practice

Replication package for **"Domain-Driven Design in Practice: A Large-Scale
Empirical Characterisation of the Open-Source Ecosystem"** (under review,
*Information and Software Technology*).
Preprint: [arXiv:2607.06471](https://arxiv.org/abs/2607.06471)

**Archived dataset (DOI):**
[10.4121/c4371d7c-6023-4460-b8ba-0c482654b082](https://doi.org/10.4121/c4371d7c-6023-4460-b8ba-0c482654b082)
(4TU.ResearchData)

## Contents

| Path | Description | Paper section |
|---|---|---|
| `repominer/` | GitHub mining tools: topic- and README-based repository discovery, metadata/commit/issue/PR collection, database merging | Sec. 3.2–3.4 |
| `predict_software_architecture_gpt_and_classification.py` | Agentic GPT-4o pipeline: iterative repository inspection, binary DDD verdict, and architectural style label; triplicate execution | Sec. 3.5 |
| `save_architecture_predictions_to_database.py` | Majority-vote consolidation of the triplicate runs into final labels | Sec. 3.5 |
| `gpt_top_repository_overview.py` | GPT-4o business-domain classification and qualitative overview of top repositories | Sec. 3.5, 4.5 |
| `prompts/` | Exact system prompts used by the two pipelines (verbatim) | Sec. 3.5 |
| `sql/rq_queries.sql` | SQL queries producing all quantitative findings, per research question | Sec. 4 |
| `data/verified_repositories.csv` | The 2,502 semantically verified DDD repositories with metadata and architecture labels | Sec. 3.5, 4.2 |
| `data/kappa_validation_sample.csv` | Manually labelled 50-repository validation sample (LLM + two human assessors) | Sec. 3.6 |

All reliability statistics in the paper (Cohen's κ, F1) can be recomputed
directly from `data/kappa_validation_sample.csv`.

## Pipeline configuration

- Model: OpenAI GPT-4o via Azure OpenAI API (version `2024-05-01-preview`)
- `temperature = 0`, `seed = 42`
- Agentic multi-turn inspection, up to 8 turns per repository
- Triplicate execution with majority-vote consensus

## Reproducing the study

1. Mine candidate repositories: see `repominer/` (requires a GitHub API token).
2. Run semantic validation: `predict_software_architecture_gpt_and_classification.py`
   (requires Azure OpenAI credentials), then consolidate with
   `save_architecture_predictions_to_database.py`.
3. Compute findings: run the queries in `sql/rq_queries.sql` against the
   resulting SQLite database, or against the archived dataset (DOI above).

## Data governance

The archived dataset contains repository metadata, activity records, and
classification outputs for the full candidate pool (11,742 repositories) and
the verified set (2,502). Third-party source code content and personal
identifiers (e.g., commit author names and emails) are deliberately excluded
for licensing and privacy reasons. The full corpus can be regenerated with the
mining tools in this repository.

## Citation

If you use this package, please cite the paper (arXiv:2607.06471) and the
dataset (DOI: 10.4121/c4371d7c-6023-4460-b8ba-0c482654b082).

## License

MIT (code). The archived dataset is licensed CC BY 4.0.
