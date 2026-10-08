# SEO-Rules: MOBILIUS AirPods cases, Amazon US (EN US)

Version 1.3 (sale window of 2026-10-08 added; rules otherwise as v1.2). Date 2026-10-08.

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

## 0a. Standing caveats (remember; do not drop in later work)
1. **Item Highlights versus title: Amazon does not say how much search weight Item Highlights carry compared with the title.** Never state, assume or optimize on the idea that highlights weigh the same as, less than or more than the title. Amazon only says highlights are "searchable and visible with titles". [A] (user instruction: "запомнить")
2. Item Highlights: **125 characters in total** for the whole field. [A] [U]
3. The indexing limit of **1000 bytes across the five bullets exists** [U, confirmed by the user]. No Amazon document was found for it, so the source of this rule is the user's confirmation, not Amazon text.
4. The description limit of **2000 characters** is confirmed [U]. No Amazon staff statement was found; the source of this rule is the user's confirmation.

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
- **Keyword Sales, reconciled on 2026-10-07.** The file's Keyword Sales (837 per week for "airpod pro case", 1,196 for "airpods 4 case", 443 for "airpods pro 2 case") is the weekly sales units attributed to the keyword for the **last complete week, 2026-09-13 to 2026-09-19** (Helium 10 `get_keywords_sales_history`: exactly 837, 1,196 and 443). The MCP field `keyword_sales_weekly` I compared earlier (76, 253, 63) is the **latest, still incomplete week, 2026-09-20 to 2026-09-26**, which is 5 to 12 times lower because sales data arrive with a delay. It is the same metric for a different week, not a different metric (my earlier note that it might be a different metric was wrong). Rule: use only the last complete week. Results: `keyword_sales_check_2026-10-07.csv` and section 6. The raw Cerebro dumps named in the file's methodology (saved on the user's disk, not in the repo) were not needed for this check.
- Generic Pro phrases ("airpods pro case") include Pro 3 demand. "airpods pro 3 case" has 202,798 searches per month. The product does **not** fit Pro 3, so never target or mention it.

## 2. Hard rules in one table

| Field (feed attribute) | Limit | Visible to shopper | Indexed | Status |
|---|---|---|---|---|
| Title (`item_name`) | 75 characters incl. spaces, brand included | Yes | Yes | [A] limit, [U] brand counts |
| Item Highlights (`title_differentiation`) | 125 characters in total, incl. spaces | Yes, next to title | Yes ("searchable"). Weight versus title: Amazon does not say (see 0a) | [A] |
| Bullet 1 to 5 (`bullet_point`) | up to 500 characters each; indexing limit 1000 bytes across the five | Yes | Yes, first 1000 bytes | [U] |
| Product Description (`product_description`) | 2000 characters, plain text | Yes | Yes | [U] confirmed, no HTML [A] |
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
- The 2000-character limit is confirmed by the user [U]. No Amazon staff statement was found. Work limit: 2000. [CHECKED]

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
Each bullet up to 500 characters. The indexing limit of **1000 bytes across the five bullets exists** [U]. Therefore all priority keywords must sit inside the **first 1000 bytes of the five bullets read in order**; bytes equal characters for ASCII text. Text after byte 1000 is for shoppers only and carries no priority keyword. Source of the limit: the user's confirmation; practitioner sources agree [C] and Amazon staff recommend 1,000 characters total [B]; no Amazon document was found. [CHECKED] as a warning.

### 4.3a Variations [U, changed 2026-10-07]
**Variations are not used for now.** Every SKU is a standalone listing: no parent SKU, no variation theme, no relationship records. The earlier plan (theme `COLOR`, unique `Color` per parent) applies again only if the user turns variations on. What stays: the title must be unique per SKU (checked) and the `Color` value keeps the print name. Consequence to know: 65 standalone listings per series share the same keyword set, so they compete for the same phrases; this is the user's decision.

### 4.4 Text language
EN US only. ASCII only. No Cyrillic and no accents in any field.

### 4.5 Item Highlights [U]
125 characters in total for the whole field. No keyword stuffing. Facts only. Do not claim anything about their search weight (section 0a).

### 4.6 Offer and price [U, 2026-10-07]
- Input: **Sale Price 22.99 USD** (default input field `sale_price`). Quantity **1** per SKU. Shipping template **Migrated Template** (the user typed "Mirgrated template"; it is the only valid value of the template). Fulfillment MFN (`Fulfillment by Merchant (Default)`). Dangerous Goods Regulations **Not Applicable**. Item condition New is assumed and flagged.
- **Sale window [U, 2026-10-08]: 2026-10-08 to 2027-05-08** (the user wrote 08.10.2026 to 08.05.2027, day.month.year). The template says the sale price starts to show after 0:00 of the start date. The window is stored in `pricing_input.json`.
- The feed has **separate** fields for the base price (`Your Price USD`) and for `Sale Price USD`; a sale price needs the start and end dates, which are now set. **The base price is still missing**: the user said "считаем от нее" (calculate from it) but gave no number and no factor. Nothing is invented. Fill `pricing_input.json` (or pass options) with one of: `explicit_standard` plus `standard_price` (a USD number), `reverse_discount` plus `discount_factor` (base price = 22.99 / factor, rounding `2_DECIMALS` or `END_99`). `standard_equals_sale` (base price 22.99, no promotion) would drop the sale window and is not consistent with the dates given. The build checks that the base price is above the sale price and that the end date is not before the start date.
- `List Price`: the template says to enter 0 if it cannot be provided; 0 is used and flagged. It is not an MSRP. MAP, minimum and maximum price: not set.

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
| Dangerous Goods Regulations | `Not Applicable` | [U] (2026-10-07) |
| Quantity (US) | 1 | [U] |
| Shipping Template (US) | `Migrated Template` | [U] (typo "Mirgrated" normalized to the valid value) |
| Fulfillment Channel Code (US) | `Fulfillment by Merchant (Default)` | [U] (MFN) |
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
Data: search volume (SV) from Helium 10 MCP `analyze_keywords`, US, re-checked 2026-10-07; Keyword Sales (KS) = weekly sales units for the keyword in the **last complete week, 2026-09-13 to 2026-09-19** (section 1). Values marked "file" come from `AirPods_US_SEO.xlsx` (the same week). The project threshold for a demand-confirmed phrase is SV >= 500 per month and KS >= 100 per week; missing data is never replaced by zero or by a guess. Full table: `keyword_sales_check_2026-10-07.csv`. Amazon matches words, not strict phrases [C].

Rules for using the status:
- **Confirmed** phrases get the priority positions (title words, bullet 1 exact phrase).
- **Fit statements** ("1st generation", "2nd generation", "4th generation", "5th generation") are written because the product facts require them, whatever their KS.
- **Below threshold** or **no complete-week data** phrases may appear naturally in bullets and description, never in a priority position, and never as the reason to add a claim.

### 6.1 Pro series
| Phrase | SV | KS per week | Status | Placement |
|---|---|---|---|---|
| airpods pro case | 32,497 | 796 (file) | confirmed; includes Pro 3 demand | bullet 1 exact phrase, always next to "2nd generation" and "1st generation" |
| airpod pro case | 34,020 | 837 | confirmed | spelling variant: backend if not visible elsewhere |
| airpods pro 2 case | 28,847 | 443 | confirmed | title words "AirPods Pro 2" and "Case", bullet 1 exact phrase |
| airpod pro 2 case | 18,533 | 632 (file) | confirmed | spelling variant, backend |
| airpods pro 2nd generation case | 2,859 | 78 | below threshold | fit statement: title "2nd/1st Generation" |
| airpods pro 1st generation case | 663 | 21 | below threshold | fit statement: title and bullet 1 (required by the product facts) |
| airpods pro 2 case cover | 2,210 | 75 | below threshold | natural wording in bullet 1 or 2 |
| airpods pro case cover | 3,177 | 83 | below threshold; includes Pro 3 | only together with the generation words |
| case airpods pro 2 | 1,766 | 34 | below threshold | natural wording |
| airpods 2 pro case; air podspro2 case | 1,246; 1,246 | 26; 37 | below threshold | backend only, if the words are not visible |
| airpodpro case; air podspro case; airpod procase | 255; 387; 391 | not checked | spelling variants | backend only, if not visible |
| airpods pro case with keychain; airpods case keychain | 350; 540 | no data; 3 | below threshold | the carabiner keychain is a product fact: write it in bullet 5 and highlights, not as a keyword push |
| airpods pro 3 case | 202,798 | (393 latest week, incomplete) | not our product | never use |
| airpods 1/2 case | 476 | n/a | wrong product | never use |
| tpu / soft-touch / carabiner phrases | 0 | n/a | no demand | bullets for shoppers only |

### 6.2 AirPods 4 series (covers AirPods 4 and AirPods 5)
| Phrase | SV | KS per week | Status | Placement |
|---|---|---|---|---|
| airpods 5 case | 128,552 | 1,650 | confirmed | title + bullet 1 |
| airpods 4 case | 86,564 | 1,196 | confirmed | title + bullet 1 |
| airpod 5 case | 52,972 | 1,262 | confirmed | spelling variant, backend if not visible |
| airpod 4 case | 42,078 | 1,381 (file) | confirmed | spelling variant, backend if not visible |
| airpods 4 case cover; airpod case 4; airpods case 4; case airpods 4; case for airpods 4 | 7,735; 9,533; 5,948; 4,088; 3,165 | 299; 314; 168; 110; 105 (file) | confirmed | bullet 1 and 2 natural exact phrases |
| air pods4 case; air pod 4 case; air pods 4 case | 4,510; 4,088; 3,330 | 145; 139; 133 (file) | confirmed | backend variants |
| airpods 5 case cover | 16,172 | latest week only (2) | no complete-week data | bullet 1 natural wording |
| case for airpods 5 | 4,739 | latest week only (3) | no complete-week data | title words "Case for AirPods 5" |
| airpods 4th generation case | 663 | 16 | below threshold | fit statement |
| airpods 5th generation case | 559 | no data | no complete-week data | fit statement |
| airpods 5 case keychain; airpods 4 case with keychain | 467; 250 | no data | no complete-week data | keychain is a product fact: bullet 5 and highlights |
| airpods 4 and 5 case | 0 | n/a | no demand | do not use |
Caution on the 5th generation: "airpods 5 case" went from 345 (week of 09-06) to 1,650 (week of 09-13) in the data, and only two complete weeks exist. The size of the demand is clear, its stability is not.

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
| 1 | Search weight of Item Highlights compared with the title (section 0a, permanent caveat) | Amazon does not say |

Closed on 2026-10-07: bullets indexing limit 1000 bytes treated as existing [U]; description limit 2000 [U]; Keyword Sales mismatch explained and reconciled (section 1).

Actions for the user:
| # | Action |
|---|---|
| A | Upload the corrected Photo 5 files (`fixed_images/pro_photo5/`) to `content.uvmaster.ru` under the same names |
| B | Rights decision on the print of q230 (the listing text is already neutral) |
| C | **Give the base price** (section 4.6): a USD number or a discount factor (base = 22.99 / factor). The sale window is set. Until then all 130 records are `DATA_REQUIRED`, with one blocker: `standard_price` |
| D | After the first sales, replace the estimated demand with the account's own Search Query Performance and Search Term Reports |

Closed: variations not used (standalone listings); quantity 1, shipping template, Dangerous Goods Regulations Not Applicable and the input Sale Price 22.99 USD recorded (2026-10-07); Keyword Sales mismatch (different week, not a different metric); 1000-byte bullets limit and 2000-character description limit confirmed by the user; Item Highlights weight kept as a permanent "Amazon does not say" caveat; AirPods 4 uses the average size, shipped MFN, size numbers only in feed fields; the infographic text "DESIGNED FOR A CLOSE FIT" accepted by the user; q246 lettering renamed "Box Cat Lettering"; package size 74 x 58 x 35 mm and package weight 40 g; Photo 5 captions fixed for all 65 Pro SKUs; q230 text corrected; claim phrases removed from 130 source descriptions; case size and weight (both series); manufacturer MOBILIUS; `Key Ring` not added; Shell Type `Soft`; AirPods 4 case also fits AirPods 5; country of origin China; GTIN Exempt (approved); "keychain" wording; ANC not mentioned; PDF catalog received (images only, no names); SEO base = the two SEO xlsx files.

## 9. Verification log (seven passes)
| Pass | What was checked | Result |
|---|---|---|
| 1 | Primary Amazon sources read: title 75 and highlights 125 (announcement of 2026-06-10), staff answers, backend 249 bytes, trademark wording, HTML in description, feed template | done |
| 2 | 20 keywords of `AirPods_US_SEO.xlsx` against Helium 10 MCP | volumes within about 20%, trends all negative; Keyword Sales reconciled on 2026-10-07 (it is the last complete week) |
| 3 | `seo_check.py` tested on a valid and on invalid listings, including q230 words and batch uniqueness of Color and title | works |
| 4 | Series files and PDF catalog: Color unique (65 of 65 per series after the q230 change), ASCII, 65 thumbnails viewed, descriptions cleaned, Photo 5 corrected for 65 SKUs, feed fields and valid values read from the template | done |
| 5 (final) | Re-fetched the five Amazon threads and re-quoted them (dates, 75 / 125, 200 split into two fields, 249 bytes and the feed error text, compatibility title formula and logo rule). Re-ran Helium 10 `analyze_keywords` for all 35 phrases used in sections 6.1 and 6.2: every volume equals the number in the tables | done |
| 6 | Keyword Sales reconciliation (2026-10-07): `get_keywords_sales_history` reproduced three file values exactly (837, 1,196, 443 for the week 2026-09-13 to 09-19) and the three MCP values (76, 253, 63) for the incomplete week 2026-09-20 to 09-26; 20 phrases checked, results in `keyword_sales_check_2026-10-07.csv` | done |
| 7 | Agent 1 batch `US-AIRPODS-20261007-001`: 130 records built and validated (no validator errors, title unique per SKU), diff against v1.0.0 generated, pricing modes tested (standard equals sale, reverse discount with and without dates, price conflict) | done |

Limits of the verification: the Amazon help pages are behind the Seller Central login and were not readable; the statements marked [A*] come from the Amazon text kept in `Amazon_Product_Title_and_Bullet_Point_Requirements.md`. The Amazon staff posts on compatibility wording are about six years old. Helium 10 numbers are estimates. Everything not confirmed is labeled [OPEN] or [C] in the text above.
