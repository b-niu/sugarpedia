---
name: article-intake
description: Intake a new article into sugarpedia. Use when the user asks to add a new note, write a new article, or migrate external content into the knowledge base. Do not use for editing existing articles or for sugarvault drafts.
---

# Article Intake Pipeline

Follow these steps in order when a new article is written or migrated into this repo. Each step is a gate — do not skip.

## 1. Place the file

- Determine the correct subdirectory under `content/`. The six top-level partitions are `01_nature`, `02_culture`, `03_engineering`, `04_questions`, `05_workbench`, `06_sources`. Design rationale and归位判据 in `docs/design.md`.
- Create the subdirectory if it does not exist. Filenames use Chinese characters or ASCII, no spaces.
- If the content is an external source that the user did not write, put it in `06_sources/` and add `source` and `author` fields in frontmatter. If it is original, place it in the matching domain partition.

## 2. Standardize frontmatter

Every article must have these fields. See `docs/design.md` for the full spec — do not duplicate here.

```yaml
---
title: Article title
aliases: [Alternative titles or English name]
date: YYYY-MM-DD
status: growing   # seed / growing / stable / questioned / parked
tags: [controlled-tag, free-tag, ...]
up: "[[ParentConcept]]"   # optional — link to the broader topic above this note
---
```

- `tags`: at least one controlled tag from the design doc, plus free tags. No more than 5 total.
- `up`: use a `[[wikilink]]` to a broader concept. If the concept does not exist yet, create a stub file with just frontmatter and a one-line placeholder. This forces the link network to grow even for topics not yet written.

## 3. Fix MathJax rendering for GitHub

GitHub does **not** reliably render inline `$...$` next to Chinese characters — it shows raw LaTeX. Follow `docs/design.md` section 一·五 (公式渲染规则):

- Simple inline symbols (subscripts, Greek letters, operators): use Unicode (e⁺, μ, Δt, n·v = 0, 177.36°).
- Complex expressions (fractions, integrals, matrices): use `$$...$$` block form with blank lines before and after.
- **Never** use `$...$` inline in this repo.

## 4. Add bidirectional links

- Within the article, add `[[wikilinks]]` to other existing articles and to parent concepts. Links can be to stub pages.
- If the article is a sequel or a parallel to an existing note, open that existing note and add a link back (either in the opening summary or in an "See also" line).
- Prefer one well-placed link per conceptual connection over many scattered ones.

## 5. Run the word-preference scan

```bash
python sugarvault/scripts/check_words.py
```

- The script scans the **public** repo (content/, docs/, scripts/, README.md, TODO.md) and skips the private sugarvault directory.
- For every hit, fix it. Never leave a hit as-is. Common replacements are documented in `sugarvault/discipline/写作纪律.md`.
- Run the scan again until it returns exit code 0.

## 6. Update the README index

Add a row to the 📝 文章索引 table in `README.md`. Format:

```markdown
| 🏛️ 训诂 | ["表"字的语义演变时间线](./content/02_culture/philology/表字的语义演变时间线.md) | growing |
```

- Emoji maps to the partition, not the specific subdirectory.
- Keep the table sorted by partition (01_nature before 02_culture before 03_engineering, etc.).

## 7. Optional: Generate SVG illustrations

If the article would benefit from diagrams (geometric relations, timelines, function curves, conceptual comparisons):

- Place SVG files in `content/assets/<topic>/`.
- Write a Python script in `scripts/` that generates them parameterizedly (see existing scripts like `gen_display_svgs.py` or `gen_particle_svgs.py` as patterns).
- Images are always SVG, never PNG/JPG. The script is the source of truth — the SVG is a derived artifact.
- Insert with `![alt text](../../assets/<topic>/filename.svg)`.

## 8. What this skill does NOT do

- Does not edit existing articles beyond link-back additions in step 4.
- Does not write commits. The user decides when to commit and push.
- Does not run Quartz builds. That is a separate concern in TODO.md.
- Does not handle sugarvault drafts. Drafts live in `sugarvault/drafts/` and go through the funnel separately.
