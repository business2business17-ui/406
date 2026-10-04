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
