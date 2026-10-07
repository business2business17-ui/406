# 406: MOBILIUS AirPods cases, Amazon US SEO

| File | What it is |
|---|---|
| `SEO-Rules.md` | The rules for the user and the AI: limits, formats, keywords, facts, procedure. Start here |
| `SEO-Rules_Research_Checkpoint.md` | Evidence and source log behind the rules (checkpoints 1 and 2) |
| `keyword_sales_check_2026-10-07.csv` | Search volume and weekly Keyword Sales (week 2026-09-13 to 09-19, plus the neighbouring weeks) for 20 phrases, with the SV >= 500 and KS >= 100 verdict |
| `seo_check.py` | Validator for every rule marked [CHECKED]. `python3 seo_check.py --selftest`, `listing.json`, or `--batch listings.json` |
| `Airpods pro_Pro2_406516.xlsx`, `Airpods4_406517.xlsx` | Series files, 65 SKUs each (print facts, Color names, photo links). Descriptions cleaned of claims, q230 corrected |
| `AirPods_US_SEO.xlsx`, `AirPods_US_Listing_Review.xlsx` | SEO base (Helium 10 snapshot of 2026-09-26) |
| `Feed AirPods Cases.xlsm` | Amazon upload template (`PORTABLE_ELECTRONIC_DEVICE_COVER`) |
| `Amazon_Product_Title_and_Bullet_Point_Requirements.md` | Amazon title and bullet requirements text |
| `fixed_images/pro_photo5/`, `fix_photo5_labels.py` | Photo 5 of the Pro series with the front/back captions corrected, and the script |
| `catalog_406_...pdf` | Catalog of the 65 prints (images and SKU codes only) |
| `agent1_build.py` | Agent 1 build: reads the two series files, writes listing content by `SEO-Rules.md`, validates with `seo_check.py`, writes the files below |
| `output/jsonl/handoff_US_batch001.jsonl` | Canonical handoff records for Agent 2, one per SKU (130), schema 1.0.0 |
| `output/xlsx/AirPods_US_Agent1_Review_batch001.xlsx` | Human review file: Products, Content, Pricing, SEO, Attributes, Compatibility, Claims, Warnings, Images, Versions, Audit, Handoff |
| `output/issues/` | `batch_summary.md`, `issues_US_batch001.csv`, `seo_sanitization_report.md` |
| `output/json/global_product_data_US.json` | Global product facts per series |
