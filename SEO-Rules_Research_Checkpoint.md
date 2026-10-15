# SEO-Rules: research checkpoint 1 (Amazon US, brand MOBILIUS)

Date: 2026-10-04. Scope: Amazon US only, EN US. This is NOT the final SEO-Rules. It records what is verified so far and what is still open.

## Status labels
- **A** = Amazon primary source (Seller Central announcement by Amazon staff, or Amazon's own template file in this repo). Fetched and read.
- **B** = Amazon staff statement in Seller Forums. Fetched and read.
- **C** = secondary source (blogs, agencies). Not accepted as a rule. Context only.
- **OPEN** = conflicting or unverified. Not to be used by the AI as a rule.

## 1. Title (item_name)
| Rule | Status | Source |
|---|---|---|
| Max 75 characters including spaces, all categories except media, effective 2026-07-27 | A | Amazon announcement (News_Amazon, 2026-06-10): https://sellercentral.amazon.com/seller-forums/discussions/t/145b6d0f-999c-4555-896c-c694bda2e470 |
| 75 is the maximum, not "under 75". If all 75 are used, Item Highlights still show | B | Amazon staff (Michelle): https://sellercentral.amazon.com/seller-forums/discussions/t/3b4f1dba-c7aa-4ab6-84b2-a0375cea315e |
| Titles over 75 are replaced gradually by an Amazon AI rewrite. Brand owners get 14 days to review in Review Listing Changes. Sellers stay responsible | A | same announcement |
| Put the most important variating attributes in the title. Move the rest to Item Highlights | B | News_Amazon: https://sellercentral.amazon.com/seller-forums/discussions/t/302aaac6-6f2b-4d86-bcd2-36fe24f0e6cd |
| Whether the brand name counts toward the 75 | OPEN | No Amazon answer found. A seller reports the tool counts the brand typed in the field. Treat brand as counted until Amazon says otherwise |
| Forbidden characters, promo phrases, same word max twice, minimum descriptive info | A* | `Amazon_Product_Title_and_Bullet_Point_Requirements.md` (user file, reproduces the Amazon help page). *The help page is login-gated and was not re-fetched |

## 2. Item Highlights (title_differentiation)
| Rule | Status | Source |
|---|---|---|
| Up to 125 characters including spaces. Indexed for search and shown next to the title | A / C | Announcement says "searchable and visible with titles". Search weight versus title: OPEN, Amazon has not said |
| Feature or benefit phrases, not full sentences. Do not repeat the title | A | Data Definitions tab, `Feed AirPods Cases.xlsm` |
| Template text says highlights show "only when the item name is under 75 characters" | Outdated | Contradicted by Amazon staff (see section 1). Use the staff answer |
| The 10-125 range in the user's .md | OPEN | No Amazon source found for the 10 minimum |

## 3. Bullet points (bullet_point x5)
| Rule | Status | Source |
|---|---|---|
| Start with a capital, no end punctuation, no emojis, no ALL CAPS, no abbreviations, no ASINs, no placeholder text, no fabric/care/country info | A* | user .md and template Data Definitions ("Do NOT use all caps or abbreviations... not for fabric content, care instructions or country") |
| Per-bullet limit | OPEN | Amazon staff quote "do not exceed 15 words or 500 characters per bullet, 1,000 total". The user .md says 10-255 per bullet. Limits vary by product type. Need the category style guide for PORTABLE_ELECTRONIC_DEVICE_COVER and the exact thread URL |
| "Only the first 1000 bytes across five bullets are indexed" | OPEN | Appears in many blogs (C). No Amazon source found. The Amazon staff text is a recommendation of 1,000 characters total, not an indexing cutoff. Safe practice: keep all five bullets within 1,000 bytes so the question does not matter |

## 4. Backend search terms (generic_keyword)
| Rule | Status | Source |
|---|---|---|
| Limit is 249 bytes (not characters) | B | Cooper_Amazon quoting "Keyword attributes explained": https://sellercentral.amazon.com/seller-forums/discussions/t/8e1ad5d2-5d5f-4086-bda3-735505e23bb1 |
| Feed template: no repetition, no competitor brand names or ASINs | A | template Data Definitions |
| Exceeding the limit makes Amazon ignore the whole field | C | Seen in Amazon help paraphrases and blogs. Keep a margin below 249 |
| Inventory-file uploads may enforce 250 or other limits than manual edit | C | Support agent statement in the same thread. Test with a small upload |
| Lowercase, spaces only, no commas, no words already in title or bullets | C | practitioner advice, to confirm against the help page |

## 5. Facts from the user's own feed (`Feed AirPods Cases.xlsm`, source A)
- Product Type: `PORTABLE_ELECTRONIC_DEVICE_COVER`. Browse node: `headphone-cases` (Cell Phones & Accessories > Accessories > Headphones, Earbuds & Accessories > Cases). Item Type Keyword has one valid value.
- Required in template: SKU, Product Type, Item Name, Brand Name, Product Id Type (UPC, EAN, GTIN, ASIN, GTIN Exempt), Product Description, Bullet Point, Country of Origin.
- Conditionally required here include: Special Features, Style, Number of Items, Color, Theme, Shell Type, Coverage, Compatible Headphone Models, Compatible Devices, Manufacturer, Package dimensions and weight.
- **Compatibility has official valid values**: `Apple AirPods Pro`, `Apple AirPods Pro (2nd generation)`, `Apple AirPods (4th generation)` and others. Use these for the Compatible Headphone Models field. Do not invent compatibility text.
- Variation themes include `COMPATIBLE_HEADPHONE_MODELS/THEME`, `COLOR`, `COLOR/COMPATIBLE_HEADPHONE_MODELS`. Theme valid values include Floral, Animal, Landscape, Nature, Sport, Military, Space and others.
- Valid values lists are closed for Special Features (43), Material (42), Shell Type (Hard, Hybrid, Soft), Water Resistance Level (5). Free text there is rejected.
- Important: "Antimicrobial" is a Special Features valid value, but the bullet rules list "anti-microbial" as a prohibited claim. Do not use it without evidence.

## 6. Trademark and compatibility wording
- Amazon-accepted pattern for accessories: `[Brand] [Product] for/compatible with/fits [Apple product]`, truthful, no Apple logo, no statement that the product is Apple's. Status: C (aggregated from forum threads). PRIMARY Amazon IP policy page still to be read.
- Enforcement is automated and produces false "Potential Trademark Misuse" flags on AirPods listings (Seller Forums, 2025). Keep "AirPods" only in the compatibility phrase.

## 7. Rufus / COSMO / Alexa for Shopping
All found material is C (agencies). Practical consensus: consistent facts across title, bullets, attributes, images. No Amazon primary document found. The final rules will treat this as a recommendation, not a rule.

## 8. Helium 10 MCP checks done
- Connected US account has **no MOBILIUS products** (`list_my_products` returned 0). Index checks (`check_asin_keyword_index`) will only work after listings exist.
- Competitor B081TQ9V4G (top organic in the user's SEO file): live title is still ~190 characters. The 75-character rule is rolling out gradually, so competitor titles are not a model for length.
- Usage budget for the MCP: 876 of 1000 calls remaining.

## 9. Not done yet
1. Category Listing Report: not provided. Not needed for US-only title/bullet rules but needed for exact required attributes. If you can export it from Seller Central, add it to the repo.
2. Cerebro xlsx: not in the repo yet.
3. Description limits and HTML rules (A+, product description), image rules, Subject Matter/Intended Use attributes.
4. Amazon Intellectual Property policy page (primary).
5. Re-verification pass x5 and the final SEO-Rules.
6. Product facts (material, shell type, dimensions, GTIN/exemption, exact AirPods fit) for the listings.

---

# Update 2 (2026-10-04): user decisions and Helium 10 MCP verification

## 10. Decisions confirmed by the user
| Topic | Decision |
|---|---|
| Brand | MOBILIUS. Brand counts toward the 75-character title limit |
| Item Highlights | 125 characters including spaces |
| Bullets | Up to 500 characters each. Use the available length. See open point A below |
| Claims | No claims at all. Removed: antimicrobial. Also not used: shockproof, waterproof, drop-tested, MagSafe, scratch-proof, print-durability guarantees |
| Product facts | TPU, soft-touch coating. Source: user |
| Compatibility, Pro | One case fits AirPods Pro (1st generation) and AirPods Pro 2 at the same time. Both must be stated. No Pro 3 claim. Source: user and `Airpods pro_Pro2_406516.xlsx` |
| Compatibility, AirPods 4 | `Airpods4_406517.xlsx` |
| Data sources | Helium 10 MCP (Magnet, Cerebro) plus Cerebro xlsx (not yet in repo) |

## 11. Feed fields that carry the confirmed facts (valid values from the user's template)
- Material: `Thermoplastic Polyurethane` is a valid value. Use it. "Soft-touch coating" has no valid value, so it goes into bullets and description as plain text.
- Compatible Headphone Models (Pro file): `Apple AirPods Pro` AND `Apple AirPods Pro (2nd generation)`. Do not add `Apple AirPods Pro (3rd generation)`.
- Compatible Headphone Models (AirPods 4 file): `Apple AirPods (4th generation)`. The valid list also has a 5th generation. A competitor lists "AirPods 5 (2026)". Do not claim 5th generation without the user's confirmation.
- Special Features valid values include `Wireless Charging Compatible`, `Scratch Resistant`, `Shockproof`, `Waterproof`, `Antimicrobial`. The "no claims" decision means these stay empty unless the user confirms a test. `Key Ring` and `Lanyard` are valid if the carabiner is confirmed in the package.
- Shell Type valid values: Hard, Hybrid, Soft. Proposal: `Soft` (TPU). Needs user confirmation.

## 12. Helium 10 MCP verification (2026-10-04, US)
**Search volume: confirmed.** All 20 phrases from `AirPods_US_SEO.xlsx` re-checked with `analyze_keywords`. Volumes are within about 20% of the 26.09 snapshot, and all 30-day trends are negative (-7% to -39%), as the file states. Examples (file → now): airpods pro case 30631 → 32497; airpods pro 2 case 27152 → 28847; airpods 4 case 102844 → 86564; case for airpods 4 3136 → 3165.

**Keyword Sales: NOT confirmed.** The file shows 837/week for "airpod pro case" and 1196 for "airpods 4 case". The MCP field `keyword_sales_weekly` returns 76 and 253 for the same phrases. The scale differs by a factor of 5 to 12, not constant. Different metric definition is likely, not proven. The file's threshold (Keyword Sales >= 100/week) cannot be reproduced with the current MCP numbers. Resolve with the Cerebro xlsx.

**Organic rank: confirmed** for B0CMTLM78L (rank 1 on airpods pro 2 case and 40 more phrases, exact ASIN, `exclude_variations=true`).

**Live competitor structure (observed, not a rule):**
- B0CMTLM78L title: "Ljusmicker for AirPods Pro Case Cover with Cleaner Kit,Black" (60 characters). It ranks #1 organic for "airpods pro 2 case" although "Pro 2" is not in the title. Generation words ("2nd/1st Generation") sit in Item Highlight and bullet 1. Ranking also depends on sales, so this does not prove that highlights outrank titles.
- B0DGXSP5VD title: "Ljusmicker for AirPods 5/4 Case (2026/2024) with Cleaner Kit,Black". Both competitors put compatibility in bullet 1 as "Accurately Match: Compatible with...". Both contain claims (shockproof, skin-friendly) that the user's no-claims rule excludes.

**Pro 3 contamination:** "airpods pro 3 case" has 202,798 searches per month, more than any phrase in the file. Generic Pro phrases ("airpods pro case", "airpod pro case") mix Pro 1/2/3 demand. The product is not for Pro 3, so these phrases cannot be the main target. Use "pro 2", "2nd generation", "1st generation" phrases as the model-specific core.

**Wrong-product trap:** "airpods 1/2 case" (476) and "airpod 1/2 case" (279) mean AirPods 1 and 2, not Pro 1 and Pro 2. Write "Pro 2nd/1st Generation" in full. Never "1/2".

**Attribute phrases have no demand:** "airpods pro tpu case", "airpods pro 2 case tpu", "airpods 4 tpu case", "airpods 4 case soft", "airpods pro case with carabiner" and "airpods 4 case anc" returned 0 search volume. TPU and soft-touch are for the buyer and for AI shopping assistants, not for keyword targeting. Do not spend title characters on them.

**Candidate phrases with volume (to use or test):** airpods pro 2nd generation case 2859; airpods pro 2 case cover 2210; airpod pro 2nd generation case 1839; air pods pro 2 case 1768; case airpods pro 2 1766; airpods 2 pro case 1246; airpods pro 1st generation case 663; airpods pro case 1st generation 306; airpods 4th generation case 663; airpods 4 cover 610; airpods 4 protective case 305; airpods keychain case 527 (only if keychain/carabiner is confirmed in the package); airpods 4 case keychain 406; airpods 4 case for women 467; airpods 4 case cute 3335; airpods pro case cute 1246.

## 13. Existing drafts need rework
`AirPods_US_Listing_Review.xlsx` ("Контроль длины") uses working limits: Title <= 100, bullets <= 500, description <= 2000, backend < 250 bytes. Title 100 violates the 75 limit. Backend < 250 bytes should be <= 249. Both must change. The same file also records wireless charging and carabiner as "from images, needs product test" and states that Photo 5 of the Pro series has front/back labels swapped.

## 14. Illustrative title lengths (NOT approved text; the brand counts)
- "MOBILIUS TPU Case for AirPods Pro 2nd/1st Generation, Black Desert Stamps" = 73 characters
- "MOBILIUS TPU Case for AirPods 4 (4th Generation), Black Peony Print" = 67 characters
So brand + material + product + compatibility + print name fits in 75, but only if print names stay short.

## 15. Open points
A. Bullets: "<= 500 each" and "use the maximum" gives up to 2,500 characters. Amazon staff recommends 1,000 total, and many sources say only about the first 1,000 bytes are indexed. Proposed rule: each bullet up to 500, with all priority keywords inside the first 1,000 bytes of the five bullets taken in order. Needs user confirmation.
B. Wireless charging: the images say it is supported, the review file says it needs a product test. Under the no-claims decision it stays out until confirmed.
C. Package contents (carabiner/keychain): needed for keychain phrases.
D. Shell Type `Soft` vs `Hybrid`.
E. AirPods 4: ANC vs standard case, and 5th generation fit.
F. Cerebro xlsx (resolves the Keyword Sales mismatch).
G. Still to read from Amazon primary sources: description limits, Intellectual Property policy page, category style guide.
