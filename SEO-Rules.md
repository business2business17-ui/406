# SEO-Rules: MOBILIUS AirPods cases, Amazon US (EN US)

Version 1.0 (final after five verification passes; open items listed in section 8). Date 2026-10-06. Scope: Amazon US only, two series: **Pro** (`Airpods pro_Pro2_406516.xlsx`, 65 SKUs) and **AirPods 4** (`Airpods4_406517.xlsx`, 65 SKUs). Product type in the feed: `PORTABLE_ELECTRONIC_DEVICE_COVER`, browse node `headphone-cases`.

Companion files: `SEO-Rules_Research_Checkpoint.md` (sources and evidence), `seo_check.py` (automatic validator for every rule marked [CHECKED]).

## 0. How to read this document
Every rule carries a status:
- **[A]** Amazon primary source (Amazon announcement or Amazon's own template file). Fetched and read.
- **[B]** Amazon staff statement in Seller Forums. Fetched and read.
- **[U]** Decision made by the user (owner of the account). Binding for this project.
- **[C]** Secondary source or practitioner advice. A recommendation, never a rule.
- **[OPEN]** Not confirmed. The AI must not apply it as a rule.
- **[CHECKED]** Enforced by `seo_check.py`.

If two rules conflict, the order of authority is: [A] > [B] > [U] > [C]. A user decision [U] may be stricter than Amazon, never looser.

## 1. What SEO is based on
SEO text is built from data, then limited by Amazon rules and by verified product facts. Words are never invented.

| Layer | Question it answers | Source for this project |
|---|---|---|
| Demand | What do shoppers type? | `AirPods_US_SEO.xlsx` and `AirPods_US_Listing_Review.xlsx` (Helium 10 Magnet / Cerebro snapshot of 2026-09-26) are the SEO base [U]. No separate Cerebro xlsx exists. Phrases added later (AirPods 5, keychain) come from Helium 10 MCP and are marked as additions. Helium 10 data are estimates, not Amazon data |
| Competition | What ranks, and for which phrases? | Cerebro on competitor ASINs (organic rank, match type) |
| Rules | What may be written, how long? | Sections 3 and 4 below |
| Facts | What is true about the product? | Section 5 (user-confirmed) |

Not available now: Brand Analytics, Search Term Reports, DataDive (user confirmed). So demand numbers are estimates. After the first sales, replace them with the account's own Search Query Performance and Search Term Reports.

Ranking has two parts. **Relevance**: the phrase must be indexed in title, highlights, bullets, description, attributes or backend terms. **Performance**: sales, conversion, click rate, price, reviews, stock. Text only controls the first part.

Data limits to remember:
- Search volume was re-checked on 2026-10-04 and matches the 26.09 snapshot within about 20%. All trends are negative (-7% to -39% per 30 days).
- Keyword Sales in the user's file (for example 837 per week) does **not** match the MCP field (76) [OPEN]. The file's numbers stay as the file's own estimate. For phrases added by MCP use search volume only; do not apply the file's Keyword Sales threshold to them.
- Generic Pro phrases ("airpods pro case") include Pro 3 demand. "airpods pro 3 case" has 202,798 searches per month. The product does **not** fit Pro 3, so never target or mention it.

## 2. Hard rules in one table

| Field (feed attribute) | Limit | Visible to shopper | Indexed | Status |
|---|---|---|---|---|
| Title (`item_name`) | 75 characters incl. spaces, brand included | Yes | Yes | [A] limit, [U] brand counts |
| Item Highlights (`title_differentiation`) | 125 characters incl. spaces | Yes, next to title | Yes ("searchable"). Weight versus title unknown | [A], weight [OPEN] |
| Bullet 1 to 5 (`bullet_point`) | up to 500 characters each | Yes | See rule 4.3 | [U] |
| Product Description (`product_description`) | 2000 characters, plain text | Yes | Yes | limit [OPEN], no HTML [A] |
| Backend terms (`generic_keyword`) | 249 bytes (target 240) | No | Yes | [B] |
| Attributes (material, compatibility, theme...) | valid values only | Yes (detail table) | Yes | [A] template |

## 3. Amazon rules (confirmed)

### 3.1 Title
1. At most **75 characters including spaces**, all categories except media, effective 2026-07-27 as a gradual rollout. Over-limit titles are rewritten by Amazon AI. Brand owners get 14 days to review. Sellers stay responsible. [A] https://sellercentral.amazon.com/seller-forums/discussions/t/145b6d0f-999c-4555-896c-c694bda2e470 and [B] (TaylorR_Amazon: rollout starts July 27, not a hard deadline) https://sellercentral.amazon.com/seller-forums/discussions/t/878dffcd-ed3f-4570-88c8-497e547e825a
2. Exactly 75 is allowed. Highlights still show. [B] https://sellercentral.amazon.com/seller-forums/discussions/t/3b4f1dba-c7aa-4ab6-84b2-a0375cea315e
3. The 75 and 125 together replace the old 200 total ("total content capacity remains at 200 characters, split across two fields") [B].
4. Brand name counts toward 75. [U] (Amazon has not answered; the safe assumption is adopted.)
5. No promotional phrases, no `! $ ? _ { } ^ ¬ ¦`, same word at most twice (articles, prepositions and conjunctions exempt; brand name also limited to two), minimum information that clearly describes the product. [A*] from the Amazon help page text kept in `Amazon_Product_Title_and_Bullet_Point_Requirements.md` (help page is login-gated and was not re-fetched). [CHECKED]
6. Put the most important variating attribute (here: the print name) in the title. If it does not fit, keep the most important in the title and move the rest to highlights. [B] https://sellercentral.amazon.com/seller-forums/discussions/t/302aaac6-6f2b-4d86-bcd2-36fe24f0e6cd
7. Title formula for compatibility products: `[Brand] [Product] for [compatible product]` using "for", "compatible with", "fits" or "intended for". Logo use is not allowed. The statement must be true. [B] (Amazon staff posts roughly six years old; not republished with the 2026 title rules) https://sellercentral.amazon.com/seller-forums/discussions/t/1c03762da5f3b97be58bb1418a85f17b

### 3.2 Item Highlights
1. Up to 125 characters including spaces. [A]
2. Feature or benefit phrases, not full sentences. Do not repeat information already in the title. [A] Data Definitions in `Feed AirPods Cases.xlsm`
3. The template note "highlights show only when the item name is under 75 characters" is outdated. Staff confirmed a 75-character title still shows highlights. [B]
4. Highlights are optional in the feed and "primarily monitored for restricted content". Still fill them: they carry what no longer fits in the title. [A/C]

### 3.3 Bullets (format)
From the Amazon text kept in the requirements file [A*] and template Data Definitions [A]. All [CHECKED] unless noted.
- Start with a capital letter. No end punctuation. Sentence fragment. Use semicolons inside a bullet.
- Use `Header: description` structure.
- Numbers one to nine in full, except model names and measurements. Space between number and unit ("2.5 mm"). Heuristic check only.
- No ALL CAPS, no abbreviations (qty, pkg, w/, approx.), no emojis, no special symbols (™ ® € … † ‡ ¢ £ ¥ © ± ~).
- No ASINs, no placeholder text (N/A, TBD), no external links or company information, no guarantee or refund wording.
- No repeated content across bullets. Each bullet carries unique information.
- No fabric, care or country-of-origin content (own fields).
- No comparison with competitors, no reference to other products.
- Template note: high ASCII characters (® ©) and HTML tags are not allowed in any text field. [A]

### 3.4 Description
- Plain text only. HTML tags are not supported (Amazon stopped supporting them in 2021). [A] (template) and [B] (News_Amazon post) https://sellercentral.amazon.com/seller-forums/discussions/t/317b0dbe1fafa9c81be02e315813a0b5
- No all caps (template). Include unique features, line details and specifications.
- The 2000-character limit is widely cited but no Amazon staff statement was found. [OPEN] Work limit: 2000.

### 3.5 Backend terms
- Limit **249 bytes**, not characters. [B] Verified again: the same thread shows that a feed (inventory file) upload is rejected with "Please reduce your generic keyword length to less than '250' bytes"; manual entry may accept more in some cases, but this project uploads a feed, so 249 is the working limit. https://sellercentral.amazon.com/seller-forums/discussions/t/8e1ad5d2-5d5f-4086-bda3-735505e23bb1 Keep to 240 bytes or fewer.
- Template: terms relevant to searches, no repetition, no competitor brand names or ASINs. [A]
- Practitioner advice [C]: lowercase, space-separated, no punctuation, no words already in title or bullets (they are already indexed), no plurals of existing words.
- Exceeding the limit may make Amazon ignore the whole field [C]. Never exceed.

### 3.6 Trademarks (Apple, AirPods)
- A truthful compatibility statement may use the brand name in text. A logo may not be used. [B]
- Never state or imply the product is made by Apple. Never use Apple logos in images or text. [B]
- Never use ™ or ® symbols (not allowed in text fields). [A]
- Automatic "Potential Trademark Misuse" flags on AirPods listings are reported by sellers. Keep AirPods only in compatibility phrases. [C]
- Use the exact official attribute values for compatibility (section 5.3). [A]

## 4. Project rules (user decisions and their implementation)

### 4.1 No claims [U]
Allowed: verifiable physical facts (material, measured thickness, what is in the package, what the picture shows, design name).
Forbidden everywhere (title, highlights, bullets, description, backend, attributes): antimicrobial, shockproof, waterproof, dustproof, scratch-proof, drop-tested, military grade, MagSafe, wireless charging, anti-slip, eco-friendly, premium, best, perfect, durable, unbreakable, "360 protection", guarantee, refund, warranty, skin-friendly, and any mention of Pro 3. [CHECKED] (substring match; review hits by hand)
Feed attributes that carry claims must stay empty: Special Features values `Antimicrobial`, `Waterproof`, `Shockproof`, `Scratch Resistant`, `Wireless Charging Compatible`, `Dust Resistant`, `Anti-Slip`, `Heavy Duty Protection`. Water Resistance Level stays empty.

### 4.2 Brand [U]
Brand is `MOBILIUS` [U]. Brand attribute is `MOBILIUS`. Every title starts with the brand: this position is a convention, not an Amazon rule [C]. [CHECKED]

### 4.3 Bullets [U]
Each bullet up to 500 characters. All priority keywords must sit inside the **first 1000 bytes of the five bullets read in order**. Bytes equal characters for ASCII text. Text after byte 1000 is for shoppers only and carries no priority keyword. Reason: many practitioner sources say only about the first 1000 bytes of bullets are indexed [C], and Amazon staff recommend 1,000 characters total [B]. No Amazon source confirms an indexing cutoff [OPEN]. [CHECKED] as a warning.

### 4.3a Variations [U]
One parent per series (Pro, AirPods 4). Variation theme `COLOR`. The `Color` value of every child must be **unique inside its parent**, otherwise Amazon does not create the variation (the theme attribute must be populated for every child [A] template). Color source: the working print names in the series files (`Color / Pattern`). The PDF catalog (`catalog_406_u001q212_u001q276_...pdf`, 4 pages, 65 thumbnails) has only SKU codes and images, no names, so it cannot replace them. All 65 thumbnails were viewed and the names match the visible subjects and slogans. They are working names, not factory names [U]. Checked on the current working names: 65 of 65 unique in each series file, case-insensitive, ASCII only, longest 38 characters. [CHECKED] by `seo_check.py --batch`. The same Color text may appear in both series (different parents), but not twice in one parent.

### 4.4 Text language
EN US only. ASCII only. No Cyrillic and no accents in any field.

### 4.5 Item Highlights [U]
125 characters. No keyword stuffing. Facts only.

## 5. Product facts (the only facts the AI may use)

### 5.1 Both series [U]
- Material: TPU (thermoplastic polyurethane) with a soft-touch coating.
- Average thickness: 2.5 mm.
- Package: one case and one carabiner keychain. Earbuds and charging case are not included. "Keychain" is approved wording [U]; "carabiner" has no search demand (0), "keychain" has.
- Construction: two parts, top and base (from images in `AirPods_US_Listing_Review.xlsx`). The fixing mechanism is unknown: never mention lock, glue or magnet.
- Cutout for a charging cable is visible in the product images (Photo 4). Wireless charging is **not** claimed.
- Each SKU is one print design. The design name comes from the `Color / Pattern` column (working names; the PDF catalog carries no names).

Write "average 2.5 mm thickness" (never "approx.").

Case size and weight [U], confirmed 2026-10-06 for **both series**: length 64 mm, width 48 mm, height 25 mm, weight 30 g. Rules:
- Feed (product, not package): `Item Length` 64, `Item Width` 48, `Item Height` 25 with unit `Millimeters`; `Item Weight` 30 with unit `Grams`. Both units are valid values in the template, no conversion needed. [A] template
- Package fields [U]: `Item Package Length` 74, `Item Package Width` 58, `Item Package Height` 35, unit `Millimeters` (case size plus 5 mm on each side, so +10 mm per dimension; reading confirmed by the user, "да такой вариант"). `Package Weight` 40, unit `Grams`, carabiner included. If the user meant +5 mm per dimension (69 x 53 x 30 mm) the three numbers change; nothing else does.
- Text [U]: **size and weight numbers go only into the feed fields, never into title, highlights, bullets, description or backend terms.** Reason: the AirPods 4 case does not have a measured size of its own; the user sets the average size 64 x 48 x 25 mm for it, and ships the orders MFN (merchant-fulfilled). Only the measured thickness ("average 2.5 mm thickness") may be written in text. [CHECKED] Never write "lightweight" (a claim).

Source descriptions [U, done 2026-10-06]: the three claim phrases were removed from all 130 `Amazon Description` cells in both series files: "precise cut-outs and full access to the charging port" (second sentence now ends after "carabiner clip") and the sentence "Slim, lightweight protection against everyday scratches and bumps" (deleted). Only those cells changed. The compatibility sentence ("Compatible with AirPods Pro / Pro 2", "Compatible with AirPods 4") was left as it was and is **not** final: listing text must use the wording of section 5.2 and 5.4. The files are a source of print facts only; do not copy their sentences into a listing.

Print q230 [U, done 2026-10-06]: the print looks like a known animated character (visual impression from the catalog thumbnail, not a legal opinion). It is now described only by colors and shapes in both series files. `Color` = `Black / Spiky Hair Figure Green Flask` (short title name `Spiky Hair Green Flask`). Image Description and Amazon Description were rewritten to match the image: a grinning figure with spiky white and teal hair, a white outfit with green buttons, purple gloves, a bubbling green flask in one hand and a teal tool in the other. The old text ("scientist", "goggles", "test tube", "potion") did not match the image and is removed. The validator blocks those words for q230 [CHECKED]. Rewording the text does not change the design printed on the product; the rights decision on the design stays with the user.

Lettering printed on a design that contains a claim word (q246 "Perfect Fit") must not be quoted in listing text; describe it as "lettering". [CHECKED: the claim list flags "perfect"]

Photo 5, Pro series [U, done 2026-10-06]: in all 65 source images the captions were swapped (the view with the print was captioned "back", the view with the pairing button "front"). Corrected copies are in `fixed_images/pro_photo5/<SKU>_5.jpg` (same file names, 2000 x 2000). Only the two captions changed; every other pixel is the same (JPEG noise only). Script: `fix_photo5_labels.py`. The images on `content.uvmaster.ru` are not replaced: upload the corrected files there under the same names. Photo 5 of the AirPods 4 series (sample q212) has correct captions. The infographic text "DESIGNED FOR A CLOSE FIT" is a fit claim; it was not changed.

### 5.2 Pro series (`Airpods pro_Pro2_406516.xlsx`)
- One case fits **AirPods Pro (1st generation) and AirPods Pro 2** at the same time. Both must be named. [U]
- Never name or imply Pro 3. Never write "1/2" alone: "AirPods 1/2" is another product with its own demand.
- The user files do not state release years or charging-port type. Do not mention years or port type.

### 5.3 Attribute values from the template (valid values only)
| Attribute | Value | Status |
|---|---|---|
| Product Type | `PORTABLE_ELECTRONIC_DEVICE_COVER` | [A] |
| Item Type Keyword | the single valid value for `headphone-cases` | [A] |
| Material | `Thermoplastic Polyurethane` | [A] value, [U] fact |
| Compatible Headphone Models, Pro series | `Apple AirPods Pro` and `Apple AirPods Pro (2nd generation)` | [A] values, [U] fact |
| Compatible Headphone Models, AirPods 4 series | `Apple AirPods (4th generation)` and `Apple AirPods (5th generation)` | [A] values, [U] fact (same case dimensions) |
| Shell Type | `Soft` | [U] |
| Theme | one valid value per print (Floral, Animal, Landscape, Nature, Sport, Military, Space...) chosen from the design name | [A] list |
| Color | design name from `Color / Pattern` (free text) | source file |
| Number of Items | 1 | fact |
| Special Features | leave empty. `Key Ring` is not added: the item is a carabiner [U]. All claim values stay empty | [U] |
| Brand Name | MOBILIUS | [U] |
| Country of Origin | `China` | [U] |
| Product Id Type | `GTIN Exempt` | [U] (exemption approved for MOBILIUS in Seller Central, confirmed by the user) |
| Item Length / Width / Height / Weight | 64 / 48 / 25 `Millimeters`, 30 `Grams` (both series; average size for AirPods 4) | [U] |
| Manufacturer | `MOBILIUS` | [U] |
| Item Package Length / Width / Height | 74 / 58 / 35 `Millimeters` | [U] |
| Package Weight | 40 `Grams` (carabiner included) | [U] |

### 5.4 AirPods 4 series (`Airpods4_406517.xlsx`)
- One case fits **AirPods 4 and AirPods 5**: the case dimensions are identical. [U] Name both generations. Never write years (release years are not stated in the user files).
- Do not mention ANC anywhere (title, highlights, bullets, description, backend). [U] [CHECKED]
- The demand is larger for 5 than for 4 (section 6.2). Keep "AirPods 5" in the title.

## 6. Keyword architecture
Data: Helium 10 MCP `analyze_keywords`, US, 2026-10-04. Monthly search volume (SV). All phrases keep their natural word order where possible, but Amazon matches words, not strict phrases [C].

### 6.1 Pro series
| Tier | Phrase | SV | Placement |
|---|---|---|---|
| 1 | airpods pro 2nd generation case | 2,859 | title (2nd/1st Generation) + bullet 1 |
| 1 | airpods pro 2 case cover | 2,210 | bullet 1 (exact words "AirPods Pro 2 case cover") |
| 1 | airpods pro 2 case | 28,847 | title or bullet 1 (words "AirPods Pro 2" plus "case") |
| 2 | airpods pro 1st generation case | 663 | title + bullet 1 |
| 2 | case airpods pro 2 | 1,766 | covered by words in bullet 1 |
| 2 | airpods pro case cover | 3,177 | bullet 1 or 2. Includes Pro 3 demand: use only together with "2nd generation" or "1st generation" |
| 3 | airpods 2 pro case | 1,246 | backend only if words are not visible |
| 3 | air podspro2 case | 1,246 | backend |
| 3 | airpodpro case; air podspro case; airpod procase | 255; 387; 391 | backend |
| avoid | airpods pro 3 case | 202,798 | do not use. Not compatible |
| avoid | airpods 1/2 case | 476 | wrong product |
| 3 | airpods pro case with keychain; airpods case keychain; airpods pro case keychain; airpods pro 2 case keychain | 350; 540; 99; 37 | bullet 5 and highlights (words "keychain", "carabiner keychain") |
| no demand | airpods pro tpu case, tpu / soft-touch phrases, carabiner phrases | 0 | use in bullets for shoppers, not for ranking |

### 6.2 AirPods 4 series (covers AirPods 4 and AirPods 5)
Helium 10 MCP, US, 2026-10-04. The 26.09 file has no AirPods 5 phrases; these were added by MCP check and re-verified on 2026-10-06 (pass 5).
| Tier | Phrase | SV | Placement |
|---|---|---|---|
| 1 | airpods 5 case | 128,552 | title + bullet 1 |
| 1 | airpods 4 case | 86,564 | title + bullet 1 |
| 1 | airpod 5 case | 52,972 | spelling variant, backend if not visible |
| 1 | airpod 4 case | 42,078 | spelling variant, backend if not visible |
| 2 | airpods 5 case cover | 16,172 | bullet 1 |
| 2 | airpods 4 case cover; airpod case 4; airpods case 4; case airpods 4 | 7,735; 9,533; 5,948; 4,088 | bullet 1 or 2 |
| 2 | case for airpods 5; case for airpods 4 | 4,739; 3,165 | title uses "Case for AirPods 5 and AirPods 4" |
| 2 | airpods 4th generation case; airpods 5th generation case | 663; 559 | bullet 1 |
| 3 | air pods4 case; air pod 4 case; air pods 4 case | 4,510; 4,088; 3,330 | backend |
| 3 | airpods case keychain; airpods 5 case keychain; airpods 4 case with keychain | 540; 467; 250 | bullet 5 and highlights |
| avoid | airpods 4 and 5 case | 0 | no demand |

### 6.3 Observed practice (not rules)
Both leading competitors (`B0CMTLM78L`, `B0DGXSP5VD`) use a short title (about 60 characters) and put the compatibility list into bullet 1 and the highlights. The Pro 2 leader ranks first for "airpods pro 2 case" without "Pro 2" in its title. Ranking also depends on sales, so this is context only.

## 7. Writing procedure for the AI (per SKU)
1. Read SKU, series, `Color / Pattern`, `Image Description`, `Amazon Description` from the series file. Use nothing outside section 5.
2. Title: `MOBILIUS [material] Case for [compatibility], [design name]`. Brand and design name must fit in 75. Shorten the design name by dropping words, never by dropping the compatibility.
3. Highlights: up to three facts that are not in the title (soft-touch coating, two-part design, carabiner included, average 2.5 mm thickness). 125 characters at most.
4. Bullets in this order:
   1. Compatibility: exact generations, tier 1 phrases, "earbuds and charging case not included".
   2. Material: TPU, soft-touch coating, average 2.5 mm thickness.
   3. Design: print name and what the print looks like (from the images).
   4. Construction: two parts, cutout for the charging cable.
   5. Package: one case, one carabiner, ways to carry it (bag, backpack, belt loop if shown in the images).
   Priority keywords in the first 1000 bytes.
5. Description: up to 2000 characters, plain text, no HTML, repeats facts without new claims.
6. Backend: tier 3 spelling variants not visible elsewhere, 240 bytes or fewer.
7. Run `python3 seo_check.py listing.json`. Fix every ERROR. Review every WARNING.
8. Human check of anything the validator cannot judge: truthfulness of the print description, no claims, compatibility wording.

## 7a. Title budget for the print name (computed on the 65 working names)
Print names (without the `Black / ` prefix) are 14 to 30 characters, median 22. Room left after the fixed part, 75 characters in total:
| Series | Fixed part | Room | Full names that fit |
|---|---|---|---|
| Pro | `MOBILIUS TPU Case for AirPods Pro 2nd/1st Generation, ` (54) | 21 | 30 of 65 |
| Pro | `MOBILIUS Case for AirPods Pro 2nd/1st Generation, ` (50) | 25 | 55 of 65 |
| AirPods 4 | `MOBILIUS TPU Case for AirPods 5 and AirPods 4, ` (47) | 28 | 63 of 65 |
| AirPods 4 | `MOBILIUS Case for AirPods 5 and AirPods 4, ` (43) | 32 | 65 of 65 |
Recommended: drop "TPU" from the title (it has no search demand and lives in highlights and bullets), keep "Generation" written in full (matches the searched phrases), and write the print name in the title as a **short name**: the full `Color` name when it fits, otherwise a shortened but still unique form. Pro: 10 names need shortening. Short names stay unique inside the parent. The full name goes to `Color`. [Recommendation C, based on the computation above]

## 8. Open points and actions
Facts the AI may not assume (nothing blocks writing the texts):
| # | Open point | Owner |
|---|---|---|
| 1 | Whether Item Highlights carry the same search weight as the title | Amazon has not said |
| 2 | Whether an indexing cutoff at 1000 bytes of bullets exists. The project rule (section 4.3) works either way | no Amazon source |
| 3 | Description limit 2000 characters | no Amazon staff source |
| 4 | Keyword Sales mismatch between the SEO file and the MCP field. Not used for new phrases | not blocking |

Actions for the user:
| # | Action |
|---|---|
| A | Upload the corrected Photo 5 files (`fixed_images/pro_photo5/`) to `content.uvmaster.ru` under the same names |
| B | Rights decision on the print of q230 (the listing text is already neutral) |
| C | After the first sales, replace the estimated demand with the account's own Search Query Performance and Search Term Reports |

Closed: AirPods 4 uses the average size, shipped MFN, size numbers only in feed fields; the infographic text "DESIGNED FOR A CLOSE FIT" accepted by the user; q246 lettering handled as "lettering"; package size 74 x 58 x 35 mm and package weight 40 g; Photo 5 captions fixed for all 65 Pro SKUs; q230 text corrected; claim phrases removed from 130 source descriptions; case size and weight (both series); manufacturer MOBILIUS; `Key Ring` not added; q230 described only by colors and shapes; Shell Type `Soft`; AirPods 4 case also fits AirPods 5; country of origin China; GTIN Exempt (approved); "keychain" wording; variation theme `COLOR` with unique values; ANC not mentioned; PDF catalog received (images only, no names); SEO base = the two SEO xlsx files.

## 9. Verification log (five passes)
| Pass | What was checked | Result |
|---|---|---|
| 1 | Primary Amazon sources read: title 75 and highlights 125 (announcement of 2026-06-10), staff answers, backend 249 bytes, trademark wording, HTML in description, feed template | done |
| 2 | 20 keywords of `AirPods_US_SEO.xlsx` against Helium 10 MCP | volumes within about 20%, trends all negative; Keyword Sales differs (open point 4) |
| 3 | `seo_check.py` tested on a valid and on invalid listings, including q230 words and batch uniqueness of Color and title | works |
| 4 | Series files and PDF catalog: Color unique (65 of 65 per series after the q230 change), ASCII, 65 thumbnails viewed, descriptions cleaned, Photo 5 corrected for 65 SKUs, feed fields and valid values read from the template | done |
| 5 (final) | Re-fetched the five Amazon threads and re-quoted them (dates, 75 / 125, 200 split into two fields, 249 bytes and the feed error text, compatibility title formula and logo rule). Re-ran Helium 10 `analyze_keywords` for all 35 phrases used in sections 6.1 and 6.2: every volume equals the number in the tables | done |

Limits of the verification: the Amazon help pages are behind the Seller Central login and were not readable; the statements marked [A*] come from the Amazon text kept in `Amazon_Product_Title_and_Bullet_Point_Requirements.md`. The Amazon staff posts on compatibility wording are about six years old. Helium 10 numbers are estimates. Everything not confirmed is labeled [OPEN] or [C] in the text above.
