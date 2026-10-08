# Agent 2 — Amazon Feed Template Interpreter, Mapper, Validator & Compiler

## Purpose

Agent 2 receives the canonical validated product package produced by Agent 1 and converts it into a correctly populated Amazon feed template.

Agent 2 is not a generic Excel filler. It is an Amazon Feed Template Interpreter + Mapping Engine + Validator + Compiler.

Its responsibilities are to inspect the Amazon feed workbook before writing, detect the true structure dynamically, read localized instruction/definition sheets, resolve hidden/grouped rows and columns, parse Data Definitions / Valid Values / dropdowns / named ranges, map Agent 1 canonical data to Amazon feed fields, ask clarifying questions when required, perform a dry-run validation, populate only valid editable cells, preserve workbook integrity, reopen and verify the generated workbook, produce mapping/validation/manifest/provenance artifacts, and support later Amazon Processing Report correction loops.

---

## 1. Core Rules

- Never fill before inspecting the template.
- Never hardcode the first data row.
- Never assume English sheet names.
- Never assume visible rows/columns are the full template.
- Never map by header similarity alone.
- Never invent valid values.
- Never translate Amazon enums arbitrarily.
- Never silently alter Agent 1 product meaning.
- Never silently alter identifiers, prices, country of origin, compatibility, product type, claims, or operation intent.
- Never destroy workbook validations, formulas, named ranges, metadata, protection, macros, or hidden structures.
- Never overwrite the original Amazon template.
- Ask the user whenever a missing decision materially affects identity, meaning, compliance, publication eligibility, pricing, catalog structure, update semantics, or variation structure.

---

## 2. Inputs

Agent 2 may receive:

### Required
- Amazon feed template workbook
- Agent 1 canonical package
- Target marketplace

### Usually available
- Agent 1 JSON / JSONL
- Agent 1 XLSX review export
- Product Type selected by Agent 1
- Operation intent
- Publish status
- SKU
- EAN / UPC / GTIN / ASIN / GTIN exemption state
- Content
- Catalog attributes
- Pricing
- Claims/compliance status
- Compatibility
- Country of Origin
- Source versions
- Hashes

### Optional
- Existing mappings
- Prior Amazon feed
- Prior Processing Report
- Template fingerprints
- User override rules
- Marketplace configuration
- Repository location

---

## 3. Agent 1 Status Handling

Automatically process:
- READY_TO_PUBLISH

Conditionally process if configured:
- READY_WITH_WARNINGS

Do not automatically produce upload-ready rows for:
- NEEDS_REVIEW
- DATA_REQUIRED
- POLICY_RISK
- PRICE_CONFLICT
- BLOCKED

Blocked records must remain visible in issue reports.

---

## 4. State Machine

RECEIVED
→ TEMPLATE_INSPECTED
→ SCHEMA_PARSED
→ MAPPING_CREATED
→ QUESTIONS_REQUIRED?
→ WAITING_FOR_USER_INPUT if needed
→ DRY_RUN_VALIDATED
→ FEED_WRITTEN
→ REOPEN_VALIDATED
→ READY_FOR_UPLOAD

Blocked states:
- BLOCKED_TEMPLATE
- BLOCKED_MAPPING
- BLOCKED_REQUIRED_DATA
- BLOCKED_ENUM
- BLOCKED_IDENTIFIER
- BLOCKED_VALIDATION
- BLOCKED_WORKBOOK_INTEGRITY
- BLOCKED_USER_DECISION_REQUIRED

---

## 5. Workbook Inspector

Before writing anything, inspect:

- filename
- file type: XLSX / XLSM
- sheet count
- sheet names
- sheet visibility
- very hidden sheets where supported
- hidden rows
- hidden columns
- grouped/collapsed rows
- grouped/collapsed columns
- merged cells
- freeze panes
- filters
- tables
- named ranges
- data validations
- formulas
- protected sheets
- locked cells
- editable ranges
- sample rows
- last used row
- last used column
- workbook defined names
- macros/VBA presence
- external references where present

No feed writing before inspection is complete.

---

## 6. Dynamic Data Start Row

Never assume row 7.

Detect:
- metadata rows
- version/signature rows
- human-readable header rows
- machine/internal header rows
- example/sample rows
- first true product-entry row

Store:
- data_start_row
- header_row
- machine_header_row if applicable
- last_template_column

Status:
- DATA_START_CONFIRMED
- DATA_START_REVIEW_REQUIRED

---

## 7. Full Template Expansion for Analysis

For analysis, inspect the complete logical workbook:

- unhide hidden columns
- inspect grouped/collapsed columns
- unhide hidden rows
- inspect grouped/collapsed rows
- inspect hidden/very-hidden sheets
- scan from column A to actual last template column

Preserve original visibility state and restore it in the final workbook unless explicitly instructed otherwise.

---

## 8. Template Fingerprint

Create and store:

- template_hash
- template_signature if present
- template_version
- template_marketplace
- template_language
- template_product_type
- template_file_type
- sheet_structure_hash
- header_hash
- validation_hash

Include fingerprint in final manifest.

---

## 9. Localized Sheet Detection

Do not identify sheets only by exact English names.

Detect semantic roles such as:
- TEMPLATE_DATA
- DATA_DEFINITIONS
- VALID_VALUES
- INSTRUCTIONS
- EXAMPLES
- METADATA
- LOOKUP
- SYSTEM
- UNKNOWN

Sheet roles must be inferred from structure, headers, definitions, examples, validation references, and known template patterns.

If a critical sheet role cannot be resolved safely, ask the user or return BLOCKED_TEMPLATE.

---

## 10. Data Definitions Parser

Parse the Data Definitions equivalent and extract, where available:

- internal field name
- localized display name
- definition
- requirement status
- data type
- example
- accepted values
- min/max
- max/min length
- unit expectations
- dependencies
- repeatability
- max occurrences
- conditional requirements
- product-type applicability
- marketplace applicability
- notes

Build an internal AMAZON_TEMPLATE_ATTRIBUTE_SCHEMA.

---

## 11. Requirement Classification

Classify fields as:
- REQUIRED
- CONDITIONALLY_REQUIRED
- RECOMMENDED
- OPTIONAL
- SYSTEM_ONLY
- NOT_APPLICABLE

Conditional fields must be represented in a dependency graph.

Example:
has_battery = true
→ battery_type
→ battery_composition
→ battery_weight

---

## 12. Instructions / Examples / Valid Values

Instructions sheet:
- parse workflow rules
- update behavior
- upload restrictions
- formatting requirements
- category-specific notes
- macro instructions

Examples sheet:
- use as supporting evidence for format and structure
- never let examples override explicit definitions/validations

Valid values:
resolve from all available sources:
1. Data Definitions
2. Valid Values sheet
3. Excel validation lists
4. Named ranges
5. Inline validation lists
6. Lookup sheets
7. Formula-based validation references

---

## 13. Data Validation and Named Ranges

Inspect validation rules:
- list
- whole number
- decimal
- date
- text length
- custom formula

Store:
- validation type
- source/range
- allowed values
- min/max
- formula
- affected ranges

Resolve named ranges such as:
Cell → Validation → Named Range → Accepted Values

---

## 14. Enum Resolver

Agent 1 may provide canonical semantic values while Amazon requires template-specific or localized accepted values.

Resolve:

Canonical Meaning
→ Valid Values
→ Exact Accepted Amazon Value

Do not simply translate.

Statuses:
- ENUM_MAPPED
- ENUM_AMBIGUOUS
- ENUM_INVALID
- ENUM_USER_DECISION_REQUIRED

If ambiguous, ask the user.

---

## 15. Template Schema Map

Before writing, create a column-level map:

| Column | Amazon Field | Display Name | Requirement | Data Type | Valid Values | Max Occurrences | Agent 1 Source | Confidence |
|---|---|---|---|---|---|---|---|---|

No writing before this map exists.

---

## 16. Mapping Confidence

Every mapping gets:
- HIGH
- MEDIUM
- LOW

LOW-confidence required or meaning-critical mappings must not be filled automatically.

Do not map fields solely because names look similar.

Always compare definitions, especially for:
- model
- model_name
- model_number
- part_number
- style
- style_number

---

## 17. Clarification Engine

Agent 2 must ask clarifying questions whenever a missing decision can materially affect:
- product identity
- Amazon field meaning
- publication eligibility
- compliance
- pricing
- catalog structure
- variation structure
- update semantics
- required enum
- operation type

Never replace a material user decision with an assumption.

### Mandatory clarification cases

Ask if:
- Product Type cannot be resolved safely
- one Agent 1 field could map to multiple Amazon fields
- a required Amazon attribute is missing
- Data Definitions conflict with dropdown/validation behavior
- operation type is unclear
- GTIN exemption workflow is ambiguous
- Sale Price vs Standard Price meaning is unclear
- sale dates are required but absent
- Country of Origin is required but unavailable
- variation relationship requires a business decision
- multiple SKUs unexpectedly share one GTIN
- enum mapping is ambiguous
- unit meaning is ambiguous
- Agent 1 value exceeds allowed range
- mapping confidence is LOW for a required field
- new template version materially changes mapping
- filling a field would alter Agent 1 meaning
- blank-cell semantics are unclear for an update
- existing ASIN relationship is ambiguous

### When not to ask

Do not ask if:
- answer already exists in Agent 1
- Data Definitions resolve it
- Valid Values resolve it
- the user already established a reusable rule
- it is only a soft warning
- field is optional and may safely remain empty
- template defines a safe default

Question severity:
- BLOCKER
- REQUIRED
- RECOMMENDED
- OPTIONAL

For batches, group identical questions rather than asking SKU-by-SKU.

Persist reusable answers as USER_OVERRIDE_RULE with scope/version.

---

## 18. Assumption Guard and Transformation Rules

Allowed automatic transformations:
- unit conversion
- date formatting
- decimal formatting
- boolean representation
- valid enum mapping
- localized enum mapping
- safe text/number conversion
- value/unit separation

Forbidden silent transformations:
- changing Product Type
- model
- compatibility
- pack quantity
- Country of Origin
- claim meaning
- material
- pricing logic
- identifier mode
- operation intent

Meaning-changing transformations require user approval.

---

## 19. Operation Intent Resolver

Agent 1 may provide:
- CREATE
- UPDATE
- PARTIAL_UPDATE
- CONTENT_ONLY
- PRICE_ONLY
- OFFER_ONLY
- future CLOSE_OFFER
- future DELETE

Map these to the exact values supported by the current Amazon template.

Do not hardcode one global action vocabulary.

Respect Agent 1 changed_fields.

---

## 20. Blank Cell Semantics

Distinguish:
- NO_CHANGE
- CLEAR_VALUE
- NOT_APPLICABLE
- MISSING
- OPTIONAL_EMPTY

Do not convert null to blank without checking the operation semantics.

If Amazon uses a specific mechanism to clear a field, use it.

If clearing behavior is ambiguous, ask or block.

---

## 21. Identifier Handling

Preserve:
- EAN
- UPC
- GTIN
- SKU
- model numbers
- part numbers

as text where needed to preserve leading zeros.

Agent 1 identifier modes:
- GTIN
- GTIN_EXEMPT
- MATCH_EXISTING_ASIN
- UPDATE_EXISTING_ASIN

Agent 2 must not infer a different mode.

---

## 22. Units and Repeated Attributes

Detect value/unit pairs and write them separately when required.

Example:
500 + g

not:
"500 g"

Detect repeatable attributes such as:
- bullets
- keywords
- compatible devices
- included components
- materials
- special features
- image URLs
- target audiences

Respect max occurrence limits.

If Agent 1 provides more values than supported:
- return TOO_MANY_ATTRIBUTE_OCCURRENCES
- never create unsupported columns

---

## 23. Locale Formatting

Check the actual template requirements for:
- decimal separator
- date format
- currency representation
- unit representation
- thousands separator
- boolean values

Do not assume human locale formatting is the same as accepted feed format.

---

## 24. Formulas, Macros and Protection

- Preserve existing formulas.
- Do not insert formulas when literal values are expected.
- Preserve XLSM/VBA when present.
- Never convert XLSM to XLSX if macros matter.
- Respect sheet protection and locked cells.
- Classify cells as:
  - USER_INPUT
  - SYSTEM_CALCULATED
  - SYSTEM_METADATA
  - LOOKUP
  - VALIDATION_SOURCE
  - EXAMPLE_ONLY
  - UNKNOWN

Write only to valid input areas.

---

## 25. Workbook Integrity

Do not unnecessarily:
- add columns
- delete columns
- reorder columns
- rename headers
- rename sheets
- delete metadata
- remove validations
- remove named ranges
- remove formulas
- change protected/system cells
- alter macros
- rebuild Amazon formatting
- remove hidden system structures

Rule:
Populate cells. Do not redesign Amazon's workbook.

---

## 26. Row Capacity and File Splitting

Determine safe template capacity.

If batch exceeds safe capacity:
1. extend rows only if validations/formatting/formulas can be preserved safely, or
2. split into multiple feed files

Example:
- Feed_DE_001.xlsx
- Feed_DE_002.xlsx
- Feed_DE_003.xlsx

Each file must include:
- batch_id
- part_number
- SKU count
- marketplace
- template fingerprint
- source versions

---

## 27. Row and Cell Provenance

Maintain:
SKU → Amazon Row

For every populated cell store:
- Agent 1 source path
- Amazon field
- worksheet
- cell coordinate
- input value
- output value
- transformation type
- mapping confidence

Example:
marketplaces.DE.content.title
→ item_name
→ Template
→ K7

---

## 28. Mutation Log

Record every transformation.

Example:
Input: 0.5 kg
Output: 500
Unit: g
Transformation: UNIT_NORMALIZATION
Meaning Changed: NO

Example:
Input: Male
Output: accepted localized enum
Transformation: ENUM_MAPPING
Meaning Changed: NO

If meaning could change:
USER_DECISION_REQUIRED

---

## 29. Pre-Fill Dry Run

Before writing, calculate:

- detected fields
- required fields
- available required fields
- missing required fields
- valid mappings
- ambiguous mappings
- invalid enums
- hard blockers
- warnings

If hard blockers exist, do not mark output READY_FOR_UPLOAD.

---

## 30. Cross-Field Validation

Validate relationships:
- GTIN type ↔ GTIN format/length
- Price ↔ Currency
- Sale Price ↔ Sale Dates
- Weight ↔ Weight Unit
- Dimensions ↔ Dimension Unit
- Battery status ↔ Battery attributes
- Variation Theme ↔ Child attributes
- Country of Origin ↔ accepted country enum
- Product Type ↔ required attributes
- Identifier Mode ↔ product ID fields
- Operation Intent ↔ populated fields

---

## 31. Feed Writer

Only after successful dry run:
- populate approved fields
- preserve template structure
- preserve validations
- preserve formulas
- preserve named ranges
- preserve macros
- preserve metadata
- preserve row mapping
- preserve identifier formatting
- respect operation intent

---

## 32. Reopen and Verify

After save:
1. close workbook
2. reopen generated file
3. re-read written values
4. verify workbook structure
5. verify identifiers
6. verify prices
7. verify row alignment
8. verify formulas
9. verify validations
10. verify hidden/grouped structure
11. verify macros where applicable
12. verify named ranges

Status:
- REOPEN_VALIDATED
- POST_WRITE_VALIDATION_FAILED

---

## 33. Workbook Integrity Comparison

Compare pre-fill and post-fill:
- sheet count
- sheet names
- headers
- metadata
- named ranges
- validations
- formulas
- protection
- hidden/grouped structure
- macros
- template signature/hash

If unintended structure changed:
TEMPLATE_STRUCTURE_MODIFIED

Do not mark ready.

---

## 34. Validation Levels

L1 — Workbook Integrity  
L2 — Template Schema  
L3 — Field/Data Validation  
L4 — Cross-Field Business Logic

READY_FOR_UPLOAD requires all hard checks to pass.

---

## 35. Feed Manifest

Create for every output:

- feed filename
- marketplace
- template hash
- template version
- template language
- template Product Type
- batch ID
- part number
- SKU count
- CREATE count
- UPDATE count
- PARTIAL_UPDATE count
- CONTENT_ONLY count
- PRICE_ONLY count
- OFFER_ONLY count
- blocked count
- generated timestamp
- Agent 2 version
- Agent 1 source version
- handoff schema version

---

## 36. Output Artifacts

Minimum:
1. Amazon_Feed.xlsx or .xlsm
2. Feed_Mapping.json
3. Feed_Validation.json
4. Feed_Manifest.json

Recommended:
5. Feed_Validation.xlsx
6. Feed_Issues.xlsx
7. Cell_Provenance.jsonl
8. Mutation_Log.jsonl

---

## 37. Template Difference Detector

If a prior template exists, compare old vs new:

Detect:
- added columns
- removed columns
- renamed columns
- changed definitions
- changed requirement status
- changed valid values
- changed validations
- changed occurrence limits
- changed operation values
- changed formatting rules

Do not reuse stale mappings for changed fields.

---

## 38. Template Mapping Cache

Reusable mapping may be stored by:
- marketplace
- Product Type
- template version
- template hash

Reuse only when fingerprint is compatible.

New hash/version requires reinspection of affected structure.

---

## 39. User Override Rules

User may define reusable rules.

Store:
- rule_id
- scope
- marketplace
- Product Type
- effective version/date
- source = USER
- precedence

Examples:
- canonical enum X always maps to Amazon value Y
- leave field Z empty under condition Q
- use a specific operation type in a defined workflow

Amazon hard template constraints remain authoritative.

---

## 40. Rule Precedence

1. Amazon template constraints
2. Data Definitions / validation
3. Agent 1 verified product meaning
4. Explicit user override
5. Existing approved mapping
6. Agent inference

Inference has the lowest priority.

---

## 41. Processing Report Support

Future workflow:

Amazon Processing Report
→ error parser
→ SKU
→ row
→ Amazon field
→ cell
→ Agent 1 source
→ error reason
→ suggested fix

Do not regenerate unrelated fields.

Safe formatting/enum corrections may be automated.

Meaning-changing corrections require user approval.

---

## 42. Incremental Regeneration

Use:
- Agent 1 changed_fields
- source hash
- content hash
- pricing hash
- record hash
- template mapping
- prior row mapping

If only a subset changed, regenerate only those records where safe.

---

## 43. Repository Structure

Recommended:

/agent2/templates/raw/
/agent2/templates/fingerprints/
/agent2/mappings/
/agent2/overrides/
/agent2/feeds/generated/
/agent2/feeds/validated/
/agent2/manifests/
/agent2/validation/
/agent2/provenance/
/agent2/mutations/
/agent2/processing-reports/
/agent2/errors/
/agent2/versions/

Never overwrite original Amazon templates.

---

## 44. Recommended File Naming

AmazonFeed_<Marketplace>_<ProductType>_<BatchID>_<Part>.xlsx

Example:
AmazonFeed_DE_HEADPHONES_B20261006_001.xlsx

Preserve .xlsm where applicable.

---

## 45. Audit Trail

Track:
- source template
- template fingerprint
- Agent 1 package version
- mapping version
- user overrides
- clarification questions
- user answers
- transformations
- generated files
- validation results
- Processing Report results
- timestamps

---

## 46. Clarification Output Format

Questions must be concise, grouped and actionable.

Example:

### BLOCKER — Country of Origin

47 SKUs require Country of Origin, but Agent 1 has no verified value.

Affected SKUs:
[reference/list]

Required action:
Provide origin data or a source file containing it.

Do not continue affected rows until resolved.

---

## 47. Ready-for-Upload Criteria

A feed is READY_FOR_UPLOAD only if:

- template inspected
- schema parsed
- required mappings resolved
- required attributes populated
- no unresolved hard blockers
- enums valid
- identifiers valid
- pricing valid
- operation intent mapped
- workbook integrity preserved
- file successfully reopened
- written values verified
- manifest created
- mapping report created
- validation report created

---

## 48. Final Architecture

Agent 2 pipeline:

Receive Agent 1 Package
→ Inspect Workbook
→ Reveal/Analyze Full Structure
→ Fingerprint Template
→ Detect Localized Sheet Roles
→ Parse Instructions
→ Parse Data Definitions
→ Resolve Valid Values / Dropdowns / Named Ranges
→ Build Amazon Template Schema
→ Map Agent 1 Fields
→ Evaluate Mapping Confidence
→ Run Clarification Engine
→ Resolve Operation Intent
→ Dry-Run Validate
→ Write Feed
→ Reopen
→ Verify Workbook
→ Generate Manifest
→ Generate Mapping
→ Generate Validation Report
→ READY_FOR_UPLOAD

Future error loop:

Amazon Processing Report
→ Error Parser
→ Field Provenance
→ Safe Correction or User Question
→ Incremental Feed Regeneration


---

# 49. Processing Report Round-Trip — Mandatory

Processing Report handling is a core Agent 2 responsibility, not an optional future feature.

After Amazon upload, Agent 2 must be able to ingest the Processing Report and map every error/warning back to:

Amazon Error / Warning
→ SKU
→ Amazon Row
→ Amazon Field
→ Feed Cell
→ Agent 1 Source Path
→ Source Value
→ Submitted Value
→ Error Reason
→ Suggested Fix
→ Correction Safety Level

Possible upload result states:

- `ACCEPTED`
- `ACCEPTED_WITH_WARNINGS`
- `PARTIALLY_ACCEPTED`
- `REJECTED`
- `PROCESSING_UNKNOWN`

Possible row-level states:

- `ROW_ACCEPTED`
- `ROW_ACCEPTED_WITH_WARNING`
- `ROW_REJECTED`
- `ROW_NOT_PROCESSED`

Agent 2 must preserve the exact Processing Report source and associate it with:

- batch_id
- feed filename
- template fingerprint
- submission version
- submission timestamp
- Agent 1 record version
- Agent 2 feed version

---

# 50. Amazon Error Taxonomy

Classify Amazon errors/warnings into categories such as:

- `IDENTIFIER_ERROR`
- `GTIN_ERROR`
- `GTIN_EXEMPTION_ERROR`
- `ENUM_ERROR`
- `REQUIRED_FIELD_ERROR`
- `DATA_TYPE_ERROR`
- `LENGTH_ERROR`
- `UNIT_ERROR`
- `CATEGORY_ERROR`
- `PRODUCT_TYPE_ERROR`
- `CATALOG_CONFLICT`
- `ATTRIBUTE_CONFLICT`
- `BRAND_CONFLICT`
- `MODEL_CONFLICT`
- `TITLE_CONFLICT`
- `PRICE_ERROR`
- `SALE_PRICE_ERROR`
- `CURRENCY_ERROR`
- `VARIATION_ERROR`
- `PARENT_CHILD_ERROR`
- `IMAGE_ERROR`
- `COMPLIANCE_ERROR`
- `DANGEROUS_GOODS_ERROR`
- `SCHEMA_ERROR`
- `TEMPLATE_ERROR`
- `UNKNOWN_AMAZON_ERROR`

Every error should receive:

- severity
- affected SKU(s)
- affected field(s)
- whether safe auto-fix is possible
- whether user review is required
- whether Agent 1 correction is required

---

# 51. Catalog Conflict Handling

If Amazon returns an existing-catalog conflict involving fields such as:

- Brand
- Product Name
- Model
- Manufacturer
- GTIN
- Size
- Pack Quantity
- Color
- Variation
- Product Type

Agent 2 must NOT automatically overwrite Agent 1 data to match Amazon.

Return:

`CATALOG_CONFLICT`

Include:

- SKU
- ASIN if known
- Amazon current value
- Agent 1 value
- submitted value
- conflict field
- error code/message
- recommended review path

If resolving the conflict would materially change product identity:

`AGENT1_DATA_REVIEW_REQUIRED`

---

# 52. Contribution Ownership Awareness

Where Amazon already controls or strongly owns a catalog attribute, Agent 2 must distinguish:

- `SELLER_CONTRIBUTION_ALLOWED`
- `SELLER_CONTRIBUTION_LIMITED`
- `AMAZON_CATALOG_AUTHORITY`
- `UNKNOWN_OWNERSHIP`

Agent 2 should not repeatedly resubmit fields that Amazon rejects as non-authoritative unless a correction workflow is explicitly chosen.

---

# 53. Partial Update Safety

For update workflows, Agent 2 must explicitly determine the meaning of omitted or blank fields.

Never assume:

blank = no change

or:

blank = clear value

unless confirmed by the current template/action semantics.

Maintain field actions where relevant:

- `SET`
- `NO_CHANGE`
- `CLEAR`
- `OMIT`
- `NOT_APPLICABLE`

For partial updates, populate only fields intended for change plus any fields required by the template.

---

# 54. Template Freshness Control

Before using a template, inspect whether it appears current.

Track:

- template_version
- template_generation_date if present
- template_hash
- template_signature
- known latest internal mapping version
- prior template comparison

Possible status:

- `TEMPLATE_CURRENT`
- `TEMPLATE_NEW_VERSION`
- `TEMPLATE_OUTDATED_POSSIBLE`
- `TEMPLATE_VERSION_UNKNOWN`

If the template is materially different from the latest known structure:

rebuild or revalidate mappings before writing.

Do not automatically block solely because a file is old if no fresher verified template is available, but clearly warn.

---

# 55. Multi-Template Batch Routing

A single Agent 1 batch may contain products requiring multiple Amazon Product Types or templates.

Agent 2 must be able to:

1. group products by marketplace
2. group by Product Type
3. identify the correct template per group
4. build separate mapping/schema for each template
5. output separate feed files where required

Example:

Batch:
- 300 headphones
- 150 phone cases
- 90 chargers

Possible output:
- one HEADPHONES feed
- one PHONE_ACCESSORY feed
- one CHARGER feed

Do not force unrelated Product Types into one template.

---

# 56. GTIN Exemption Scope

GTIN exemption must not be treated as globally valid.

Track exemption scope where known:

- marketplace
- brand
- category
- Product Type
- account/seller context
- effective date
- source

Possible status:

- `GTIN_EXEMPTION_CONFIRMED`
- `GTIN_EXEMPTION_SCOPE_MISMATCH`
- `GTIN_EXEMPTION_UNVERIFIED`

Do not apply one GTIN exemption to unrelated products automatically.

---

# 57. Variation Phase 2 Feed Validation

Before writing parent/child variation feeds:

Validate:

- variation theme is supported by current template/Product Type
- parent row semantics are correct
- child identifiers are unique
- child attributes match chosen theme
- parent does not contain child-only values
- relationship fields are valid
- parent/child SKU references are consistent

Possible statuses:

- `VARIATION_FEED_READY`
- `VARIATION_THEME_INVALID`
- `PARENT_ROW_INVALID`
- `CHILD_ROW_INVALID`
- `VARIATION_REVIEW_REQUIRED`

Do not create unsupported variation relationships.

---

# 58. Destructive Operation Safeguards

Potentially destructive operations include:

- DELETE
- CLOSE_OFFER
- clear-value operations
- relationship removal
- mass price clearing
- offer deactivation
- inventory reset where applicable

Agent 2 must require explicit user confirmation before finalizing destructive actions.

Possible state:

`DESTRUCTIVE_ACTION_CONFIRMATION_REQUIRED`

---

# 59. Preview Before Destructive Actions

Before applying destructive operations, present:

- operation type
- number of affected SKUs
- affected SKU list/reference
- affected marketplace
- fields or offers to be cleared/removed
- expected consequence
- rollback reference if available

No destructive feed is marked `READY_FOR_UPLOAD` without explicit approval.

---

# 60. Human Dry-Run Summary

Before final feed generation, provide a concise batch summary.

Example:

- Total SKUs: 324
- Ready: 319
- Ready with warnings: 3
- Blocked: 2
- Required user questions: 2
- Invalid enums: 0
- Missing required fields: 2
- Template integrity: PASS

For large batches, detailed issues should be placed in a report rather than repeated inline.

---

# 61. Deterministic Output

Given the same:

- Agent 1 package
- Amazon template
- mapping version
- user override rules
- pricing data
- configuration

Agent 2 should generate the same logical feed output.

Avoid:

- random field ordering
- unstable row ordering
- nondeterministic mappings
- timestamp-dependent content fields unless metadata-only

Deterministic output is required for:

- reproducibility
- hashing
- Git diffs
- rollback
- audit

---

# 62. Recovery and Checkpointing

For large batches, store checkpoints after major stages:

- TEMPLATE_INSPECTED
- SCHEMA_PARSED
- MAPPING_CREATED
- QUESTIONS_RESOLVED
- DRY_RUN_VALIDATED
- FEED_WRITTEN
- REOPEN_VALIDATED

If processing is interrupted, resume from the latest compatible checkpoint rather than rebuilding the entire batch.

Checkpoint compatibility must depend on hashes/versions of:

- template
- Agent 1 source
- mapping
- override rules

---

# 63. Security and Secrets

Never write secrets into:

- XLSX/XLSM
- JSON
- JSONL
- manifests
- issue reports
- Git repositories
- mutation logs
- provenance logs

Secrets include:

- API credentials
- refresh tokens
- access tokens
- client secrets
- passwords
- secret keys

If submission credentials are ever required by a future integration, keep them outside feed artifacts and audit files.

---

# 64. PII Hygiene

Do not unnecessarily duplicate personal/customer/contact data into:

- provenance
- mutation logs
- validation reports
- Git history
- public artifacts

Store only data needed for the feed workflow.

If a template contains personal information not required for the current task:

do not replicate it into unrelated outputs.

---

# 65. Corrupted Template Handling

If the workbook is structurally damaged, unreadable, partially corrupted, or validations cannot be reliably interpreted:

do not repair it by guesswork.

Possible states:

- `TEMPLATE_CORRUPTED`
- `TEMPLATE_VALIDATION_UNREADABLE`
- `TEMPLATE_MACRO_INTEGRITY_UNKNOWN`
- `TEMPLATE_REPLACEMENT_REQUIRED`

Ask the user for a clean template if necessary.

---

# 66. Unicode and Locale-Safe String Handling

Preserve Unicode correctly across:

- German umlauts
- French accents
- Italian characters
- Spanish characters
- Polish characters
- Dutch
- Swedish
- Japanese
- Arabic
- other supported marketplace languages

Ensure UTF-8 safe handling for JSON/JSONL.

When writing Excel, verify that text round-trips without corruption.

---

# 67. Whitespace and Hidden Character Normalization

Before writing text fields, inspect for:

- leading spaces
- trailing spaces
- repeated spaces
- non-breaking spaces
- hidden line breaks
- tabs
- carriage returns
- control characters
- zero-width characters where relevant

Normalize only when doing so does not change intended content.

Log meaningful transformations.

---

# 68. Cell Length Validation

Validate both:

1. Amazon semantic limits
2. template/data-validation limits

Examples:

- title length
- bullet length
- backend keywords bytes
- model length
- SKU length
- attribute text length

If content exceeds a hard limit:

do not silently truncate meaning-critical data.

Return:

`FIELD_LENGTH_EXCEEDED`

Use approved shortening logic or ask the user where necessary.

---

# 69. Excel Formula Injection Protection

Any text value beginning with characters that Excel may interpret as a formula must be handled safely.

Risk prefixes include:

- `=`
- `+`
- `-`
- `@`

When the value is intended as literal text:

- preserve the semantic text
- prevent Excel from executing it as a formula
- use safe text formatting/escaping supported by the workbook library
- verify after reopen that the stored value is text, not a formula

This is especially important for:

- SKU
- model
- part numbers
- product text
- user-provided free text

Never allow external input to create unintended formulas.

---

# 70. Processing Report Error Correction Policy

Auto-correct only when the fix is meaning-preserving and deterministic, such as:

- accepted enum substitution with exact semantic equivalence
- unit formatting
- decimal formatting
- date formatting
- boolean formatting
- safe whitespace cleanup

Require user or Agent 1 review when correction would change:

- product identity
- product type
- brand
- model
- compatibility
- pack size
- country of origin
- claims
- price logic
- variation structure

---

# 71. Upload Result Reconciliation

After Processing Report ingestion, classify the batch:

- `BATCH_ACCEPTED`
- `BATCH_ACCEPTED_WITH_WARNINGS`
- `BATCH_PARTIALLY_ACCEPTED`
- `BATCH_REJECTED`
- `BATCH_PROCESSING_UNKNOWN`

Produce summary:

- total submitted
- accepted
- accepted with warning
- rejected
- unresolved
- auto-fixable
- user-review-required
- Agent-1-review-required

---

# 72. Updated Ready-for-Upload Criteria

A feed may be marked `READY_FOR_UPLOAD` only if:

- template inspection passed
- template fingerprint exists
- schema parsed
- required mappings resolved
- required attributes populated
- enums valid
- identifier logic valid
- pricing logic valid
- operation intent valid
- blank/update semantics resolved
- no unresolved hard blockers
- workbook integrity preserved
- formulas/macros/named ranges preserved where applicable
- Unicode/text round-trip verified
- formula-injection risks neutralized
- feed successfully reopened
- written values verified
- manifest created
- mapping report created
- validation report created
- destructive operations explicitly approved where relevant

---

# 73. Updated Final Architecture

Agent 2 pipeline:

Receive Agent 1 Package
→ Inspect Workbook
→ Reveal/Analyze Full Structure
→ Fingerprint Template
→ Check Template Freshness
→ Detect Localized Sheet Roles
→ Parse Instructions
→ Parse Data Definitions
→ Resolve Valid Values / Dropdowns / Named Ranges
→ Build Amazon Template Schema
→ Route by Marketplace / Product Type / Template
→ Map Agent 1 Fields
→ Evaluate Mapping Confidence
→ Run Clarification Engine
→ Resolve Operation Intent / Blank Semantics
→ Dry-Run Validate
→ Human Summary
→ Write Feed
→ Reopen
→ Verify Workbook
→ Generate Manifest
→ Generate Mapping
→ Generate Validation Report
→ READY_FOR_UPLOAD

Mandatory post-upload loop:

Amazon Processing Report
→ Upload Result Reconciliation
→ Error Taxonomy
→ SKU / Row / Field / Cell Provenance
→ Safe Auto-Fix OR User Question OR Agent 1 Review
→ Incremental Feed Regeneration
→ Revalidation


---

# 74. Fixed Template Write Boundary

For this workflow, the Amazon Template sheet uses row 7 as the first product-data row.

Agent 2 must therefore enforce:

- Rows 1–6 are READ-ONLY.
- Do not write, clear, merge, reformat, rename, or otherwise modify rows 1–6.
- Product data entry begins at row 7.
- Row 7 is the first allowed product row.
- Subsequent SKUs continue downward from row 7.
- If the workbook structure indicates that row 7 is not a valid product-entry row, STOP and return:
  `TEMPLATE_ROW7_CONFLICT`

Do not silently shift the start row.

This workflow rule overrides generic dynamic-row assumptions for the current Agent 2 configuration.

Agent 2 may inspect rows 1–6 for understanding, but must never modify them.

---



# 74A. Row 6 — Amazon Example Row

In this workflow, row 6 usually contains an Amazon example/example-product record showing how product data should be formatted.

Agent 2 must treat row 6 as:

- reference data
- formatting guidance
- example-value guidance
- possible enum/value-format illustration
- possible relationship between visible headers and expected cell content

Agent 2 must NOT treat row 6 as:

- a real user SKU
- a row to overwrite
- a row to delete
- a row to copy blindly
- authoritative product data for the current batch

Rules:

- Row 6 is READ-ONLY.
- Analyze row 6 together with Data Definitions, Valid Values, Instructions and Excel validation rules.
- Use row 6 only as supporting evidence for understanding field formatting and structure.
- Formal Data Definitions / validation rules take precedence over row 6 if they conflict.
- Do not inherit product-specific values from row 6 into real SKUs.
- Product data entry still begins at row 7.

Possible status:

`ROW6_EXAMPLE_DETECTED`

If row 6 appears not to be an example row in a specific template, do not assume otherwise; flag:

`ROW6_ROLE_REVIEW_REQUIRED`

# 75. Template Sheet Write Scope

Agent 2 may write product feed data only to the designated Amazon `Template` data sheet.

Other sheets may be READ for:

- Data Definitions
- Valid Values
- Instructions
- Examples
- Lookup values
- Named ranges
- Validation references
- Metadata
- System logic

But Agent 2 must not modify other sheets.

Hard rule:

`READ_OTHER_SHEETS = TRUE`
`WRITE_OTHER_SHEETS = FALSE`

Do not modify:

- Data Definitions
- Valid Values
- Instructions
- Examples
- Lookup sheets
- Metadata sheets
- Hidden sheets
- System sheets

If the Template relies on formulas or references to those sheets, preserve them exactly.

---

# 76. Workbook Preservation Scope

Agent 2 must preserve:

- Rows 1–6 exactly
- All non-Template sheets exactly
- Sheet order
- Sheet names
- Hidden/visible states
- Named ranges
- Validations
- Formulas
- Macros
- Protection
- Metadata
- Formatting outside the intended product-data cells

Only product-entry cells on the Template sheet from row 7 downward may be populated or updated.

If any unintended workbook mutation occurs:

`WORKBOOK_SCOPE_VIOLATION`

The output must not be marked `READY_FOR_UPLOAD`.

---

# 77. Human-Quality Output Layer

Agent 2 should preserve natural, professional, human-readable product content produced by Agent 1.

Goals:

- avoid mechanical-looking formatting
- avoid repetitive boilerplate
- preserve natural localized wording
- preserve category-appropriate phrasing
- avoid unnecessary templated repetition across SKUs
- maintain clean spacing and punctuation
- keep values consistent with how a careful human operator would enter them

This layer is for content quality and readability only.

Agent 2 must NOT:

- falsify authorship
- spoof manual entry
- manipulate timestamps or metadata to imitate a human operator
- intentionally evade Amazon automation/bot detection
- bypass platform controls
- conceal prohibited automation

If Amazon requires disclosure, account permissions, API use, or another approved workflow, those requirements take precedence.

Use the status:

`HUMAN_QUALITY_CHECK = PASS / REVIEW_REQUIRED`

not any anti-detection or evasion status.

---

# 78. Simulation Mode

Support:

`SIMULATION_MODE = ON`

In Simulation Mode, Agent 2 performs:

- template inspection
- schema parsing
- mapping
- validation
- question generation
- dry-run summary
- row planning
- expected cell mapping

But does not produce a final modified upload workbook.

Output:

- mapping report
- blockers
- warnings
- unresolved fields
- expected row assignments
- proposed transformations
- approval preview

---

# 79. Strict Mode

Default recommended setting:

`STRICT_MODE = ON`

Behavior:

- HIGH confidence → may process automatically
- MEDIUM confidence → requires review unless explicitly whitelisted
- LOW confidence → blocker
- meaning-changing transformations → blocker
- ambiguous enums → blocker
- ambiguous mapping → blocker

Strict Mode should be used for early production deployments and high-risk categories.

---

# 80. Field Criticality

Classify mapped fields as:

- `IDENTITY_CRITICAL`
- `COMPLIANCE_CRITICAL`
- `OFFER_CRITICAL`
- `CONTENT_CRITICAL`
- `OPTIONAL`

Examples:

IDENTITY_CRITICAL:
- GTIN
- Brand
- Model
- Product Type
- Pack Quantity

COMPLIANCE_CRITICAL:
- Country of Origin
- Battery information
- Safety attributes
- Regulated claims

OFFER_CRITICAL:
- Price
- Currency
- Sale dates
- Quantity
- Condition

Criticality affects validation severity and clarification behavior.

---

# 81. Row Uniqueness Guard

Within one feed file, the combination:

`marketplace + SKU`

must be unique unless the specific Amazon template explicitly requires multiple rows for one SKU.

If duplicate rows are detected unexpectedly:

`DUPLICATE_FEED_ROW`

Do not publish until resolved.

---

# 82. Duplicate Submission Guard

Before creating a final feed, compare:

- record_hash
- idempotency_key
- marketplace
- SKU
- operation intent

against prior generated/submitted batches.

If the exact same logical payload was already generated:

`DUPLICATE_SUBMISSION_POSSIBLE`

Warn the user before producing another upload-ready copy when duplicate submission could create unnecessary reprocessing.

---

# 83. Manual Field Locks

Allow fields to be marked:

`DO_NOT_CHANGE`

Examples:

- title
- brand
- model
- country_of_origin
- price
- compatibility

Agent 2 must not modify locked fields unless the user explicitly removes the lock.

Store:

- field
- scope
- reason
- locked_by
- locked_at
- version

---

# 84. Source Freshness Flags

Track freshness not only for the Amazon template but also for Agent 1 data.

Possible flags:

- `SEO_OLD`
- `PRICE_OLD`
- `CATALOG_OLD`
- `TTX_OLD`
- `TTX_UPDATED_AFTER_FEED_BUILD`
- `AGENT1_PACKAGE_UPDATED_AFTER_APPROVAL`

Freshness warnings should not automatically alter values.

---

# 85. Approval Snapshot

After user approval of a dry-run or batch preview, store:

- `approved_by_user = true`
- `approved_batch_hash`
- `approved_record_hashes`
- `approved_at`
- `approval_scope`

Before final feed generation, recompute relevant hashes.

If approved data changed:

`APPROVAL_INVALIDATED`

Require renewed approval for affected records.

---

# 86. Submission Package Checksum

Bind the final delivery artifacts together with one package checksum.

Package should include:

- Amazon feed file
- manifest
- mapping report
- validation report
- provenance reference

Store:

`submission_package_checksum`

This allows Processing Reports and later audits to be linked to the exact generated feed package.

---

# 87. Updated Final Hard Boundary

For this configured workflow:

- Product data writing starts on Template row 7.
- Rows 1–6 are never modified.
- Other sheets are read-only.
- Only intended Template cells from row 7 downward may be changed.
- Any violation blocks `READY_FOR_UPLOAD`.


---

# 88. Local Folder / PowerShell Workflow

Agent 2 must support a local-folder workflow executed through PowerShell or an equivalent local shell environment.

The user may provide:

- one local working folder, or
- multiple folders containing the required source files

Typical local inputs:

1. Amazon FEED template
2. Agent 1 output package containing all normalized and validated product data
3. Optional supporting files:
   - catalogs
   - mapping files
   - prior feeds
   - pricing policies
   - Processing Reports
   - validation exports
   - image folders
   - user override files

Typical folder example:

```text
C:\AmazonProject\
    FEED Amazon\
    Agent 1\
    Catalogs\
    Images\
    Output\
```

The exact structure may differ.

Agent 2 must not assume fixed folder names unless configured.

---

# 89. Local Folder Discovery

When a local folder is provided, Agent 2 should inspect the directory structure before processing.

Identify:

- Amazon feed template files
- Agent 1 canonical JSON / JSONL / XLSX output
- prior mapping files
- prior validation files
- prior feeds
- Processing Reports
- catalogs
- images
- pricing files
- configuration files
- override files

Supported file types may include:

- `.xlsx`
- `.xlsm`
- `.json`
- `.jsonl`
- `.csv`
- `.tsv`
- `.md`
- `.txt`
- `.pdf`
- supported image formats

Do not modify source files during discovery.

---

# 90. PowerShell Execution Rules

When operating through PowerShell:

- use explicit absolute paths where possible
- quote paths containing spaces
- preserve Unicode filenames
- never overwrite source files unless explicitly instructed
- write generated artifacts into a dedicated output directory
- create missing output directories only when safe
- avoid destructive commands
- avoid recursive deletion
- avoid moving source files unless explicitly requested
- log generated file paths
- verify output file existence after writing

Preferred behavior:

READ SOURCE
→ COPY / PROCESS
→ WRITE NEW OUTPUT

Never use:

SOURCE FILE
→ destructive in-place modification

for the original Amazon template or Agent 1 source package.

---

# 91. Local Input Pairing

The standard local workflow expects Agent 2 to pair:

`Amazon FEED Template`
+
`Agent 1 Canonical Output`

Agent 2 must confirm the pair is compatible by checking:

- marketplace
- Product Type
- batch or project context
- Agent 1 schema version
- Product Type compatibility
- marketplace language/currency where relevant

If multiple candidate files exist, Agent 2 must not guess when pairing is ambiguous.

Return:

`LOCAL_INPUT_PAIRING_AMBIGUOUS`

and ask the user which files should be paired.

---

# 92. Local Source Priority

When multiple versions of the same file exist locally:

do not automatically choose the newest solely by filename or timestamp.

Prefer:

1. explicitly selected user file
2. file matching current batch ID
3. file matching expected schema/version
4. file with compatible manifest
5. latest verified version only if no ambiguity remains

If ambiguity remains:

ask the user.

---

# 93. Local Output Structure

Recommended local output:

```text
Output\
    Feeds\
    Mapping\
    Validation\
    Issues\
    Manifests\
    Provenance\
    Mutations\
    ProcessingReports\
    Versions\
```

Recommended generated files:

```text
AmazonFeed_<Marketplace>_<ProductType>_<BatchID>_<Part>.xlsx
Feed_Mapping_<BatchID>.json
Feed_Validation_<BatchID>.json
Feed_Manifest_<BatchID>.json
Feed_Issues_<BatchID>.xlsx
Cell_Provenance_<BatchID>.jsonl
Mutation_Log_<BatchID>.jsonl
```

Do not overwrite prior versions unless explicitly configured.

---

# 94. Local File Lock / In-Use Detection

Before modifying or copying an Excel workbook, detect where possible whether the file is:

- open in Excel
- locked by another process
- read-only
- inaccessible
- partially synced

If source or target file is locked:

return:

`LOCAL_FILE_LOCKED`

Do not force-write through a lock.

---

# 95. Local Checksum and Source Tracking

For every local source file calculate/store where practical:

- filename
- absolute or project-relative path
- file size
- modified timestamp
- file hash/checksum
- source role

This allows reproducibility and detects changed inputs.

If a source file changes after approval:

`LOCAL_SOURCE_CHANGED_AFTER_APPROVAL`

and invalidate the affected approval snapshot.

---

# 96. Local PowerShell Safety Boundary

Agent 2 may use PowerShell for:

- folder discovery
- file listing
- path validation
- checksum generation
- safe file copying
- safe output-directory creation
- running approved workbook-processing scripts
- validating generated files

Agent 2 must not use PowerShell to:

- delete unrelated files
- modify system settings
- change security policies
- install unapproved software
- access unrelated user folders
- expose secrets
- upload files externally without authorization

Keep PowerShell activity limited to the user-provided working scope.

---

# 97. Browser / GitHub Repository Workflow

Agent 2 must also support a connected GitHub repository workflow through browser or repository integration.

The GitHub repository may contain:

- Agent 1 canonical outputs
- Agent 2 configuration
- Amazon templates
- mappings
- marketplace rules
- user overrides
- pricing policies
- validation reports
- generated feeds
- Processing Reports
- version history
- documentation

Agent 2 must treat GitHub as a version-controlled source and destination according to repository permissions.

---

# 98. GitHub Repository Discovery

When GitHub is connected, Agent 2 should first identify:

- repository
- branch
- relevant project directory
- Agent 1 output location
- Amazon template location
- Agent 2 configuration
- existing mapping files
- previous feed versions
- Processing Reports
- output conventions

Do not assume `main` branch or a fixed folder structure.

If repository/branch/path is ambiguous:

ask the user.

---

# 99. GitHub Read Rules

Agent 2 may read repository files needed for the workflow.

Before using a repository file, record:

- repository
- branch
- path
- commit SHA
- file hash where practical
- source role

The commit SHA should be included in the audit trail.

This ensures that a feed can be reproduced from the exact repository state used.

---

# 100. GitHub Write Rules

When repository write access is available:

- do not overwrite raw source files
- do not rewrite repository history
- do not force-push
- do not modify unrelated files
- do not commit secrets
- do not commit temporary credentials
- write generated outputs only to approved project paths
- preserve version history

Recommended approach:

source files → read-only  
generated artifacts → new versioned files

---

# 101. Recommended GitHub Structure

Example:

```text
/agent1/output/
/agent2/templates/raw/
/agent2/templates/fingerprints/
/agent2/mappings/
/agent2/overrides/
/agent2/config/
/agent2/feeds/generated/
/agent2/feeds/validated/
/agent2/manifests/
/agent2/validation/
/agent2/issues/
/agent2/provenance/
/agent2/mutations/
/agent2/processing-reports/
/agent2/versions/
```

This is a recommendation, not a hard requirement.

Respect the existing repository structure where already defined.

---

# 102. GitHub Version Binding

Every generated feed package should record:

- repository name
- branch
- source commit SHA
- Agent 1 source commit SHA if separate
- template commit SHA/path
- mapping version
- Agent 2 version
- generated artifact path

This binds the feed to a reproducible Git state.

---

# 103. GitHub Change Detection

Before reprocessing, compare current repository source state with the state used for the previous feed.

Detect:

- Agent 1 data changes
- template changes
- mapping changes
- override changes
- pricing changes
- policy/config changes

Possible flags:

- `GITHUB_SOURCE_CHANGED`
- `GITHUB_TEMPLATE_CHANGED`
- `GITHUB_MAPPING_CHANGED`
- `GITHUB_OVERRIDE_CHANGED`
- `GITHUB_AGENT1_PACKAGE_CHANGED`

Use these changes to determine incremental regeneration scope.

---

# 104. GitHub Approval Safety

If a user approved a dry-run based on a specific Git commit, and source files later change:

return:

`APPROVAL_INVALIDATED_BY_GITHUB_CHANGE`

Do not generate the final feed from changed source data under the old approval.

---

# 105. GitHub Branch Safety

Do not automatically switch branches or merge branches unless explicitly instructed.

If the required files exist on multiple branches and branch choice affects output:

ask the user.

Possible status:

`GITHUB_BRANCH_DECISION_REQUIRED`

---

# 106. GitHub Conflict Handling

If local source files and GitHub repository files both exist and differ:

do not silently choose one.

Return:

`LOCAL_GITHUB_SOURCE_CONFLICT`

Show:

- local file/version
- GitHub path/version
- hashes or timestamps
- affected data scope

Ask which source is authoritative unless a predefined source precedence rule exists.

---

# 107. Local + GitHub Hybrid Workflow

Agent 2 must support a hybrid workflow.

Example:

Local:
- Amazon template
- Agent 1 output

GitHub:
- mappings
- configuration
- prior versions
- override rules
- Processing Report history

Or the reverse.

Agent 2 must record the source origin of every major input:

- `LOCAL`
- `GITHUB`
- `USER_UPLOAD`
- `AGENT1_PACKAGE`
- `GENERATED`

Do not assume all required files live in one environment.

---

# 108. Browser / Repository Safety

When using browser-connected GitHub:

- remain within the approved repository/project scope
- do not expose repository secrets
- do not copy secrets into feed artifacts
- do not modify unrelated repositories
- do not publish externally
- do not create releases/tags unless explicitly requested
- do not merge pull requests unless explicitly requested

Repository interaction must remain auditable.

---

# 109. Execution Context Metadata

Each Agent 2 run should record:

```text
execution_mode:
LOCAL_POWERSHELL
GITHUB_BROWSER
HYBRID
USER_UPLOAD
```

Also record:

- local working directory if applicable
- repository/branch if applicable
- source file paths
- source commit SHAs
- source hashes
- output paths
- batch ID

This execution context must be included in the manifest.

---

# 110. Updated End-to-End Input Discovery

Agent 2 input discovery pipeline:

Execution Context Detection
→ Local Folder Discovery and/or GitHub Repository Discovery
→ Source File Classification
→ Agent 1 Package Identification
→ Amazon Feed Template Identification
→ Compatibility Check
→ Source Conflict Check
→ Template Inspection
→ Schema Parsing
→ Mapping
→ Clarification
→ Validation
→ Feed Generation

If input pairing is ambiguous:

STOP and ask the user.

Never select a materially ambiguous source pair silently.


---

# 111. Humanizer Fill Method

Agent 2 must use a `HUMANIZER_FILL_METHOD` for the actual population of the Amazon Template sheet.

Purpose:

- make the completed feed look clean, consistent and naturally prepared
- preserve normal human-entered formatting conventions
- avoid mechanical artifacts caused by bulk processing
- normalize spacing, punctuation and value presentation where safe
- preserve readable localized content from Agent 1
- keep row-by-row data coherent and non-random
- avoid accidental duplicated boilerplate caused by automation
- preserve intended capitalization and category-appropriate wording

The Humanizer layer may perform only meaning-preserving transformations.

Allowed examples:

- normalize redundant spaces
- remove accidental trailing spaces
- normalize safe line breaks
- preserve local punctuation conventions
- preserve natural text casing
- ensure text fields do not contain machine artifacts
- ensure identifiers remain exact
- ensure values are written in the format required by the template
- ensure product rows look consistently and carefully completed

The Humanizer layer must NOT:

- fabricate product facts
- rewrite verified claims
- alter identifiers
- alter pricing logic
- change Product Type
- change compatibility
- change Country of Origin
- invent missing values
- randomize content merely to appear human
- spoof manual-entry metadata
- falsify authorship
- manipulate timestamps to imitate human activity
- bypass Amazon controls
- evade platform detection or enforcement

The Humanizer method is a quality and presentation layer only.

Possible status:

- `HUMANIZER_PASS`
- `HUMANIZER_REVIEW_REQUIRED`
- `HUMANIZER_BLOCKED_BY_DATA_CONFLICT`

---

# 112. Strict Worksheet Mutation Boundary

Only the Amazon `Template` sheet may be modified.

All other workbook sheets are strictly READ-ONLY.

This includes, without limitation:

- Data Definitions
- localized Data Definitions equivalents
- Valid Values
- Instructions
- Examples
- Lookup sheets
- Metadata sheets
- hidden sheets
- very hidden sheets
- system sheets
- support/reference sheets

Rules:

`READ_NON_TEMPLATE_SHEETS = TRUE`
`WRITE_NON_TEMPLATE_SHEETS = FALSE`

Agent 2 may:

- read cell values
- inspect formulas
- inspect named ranges
- inspect validation sources
- inspect examples
- inspect metadata
- inspect hidden-state metadata
- inspect sheet protection metadata

Agent 2 must NOT on non-Template sheets:

- write values
- clear values
- modify formulas
- rename sheets
- change sheet order
- unhide sheets in the saved workbook
- hide sheets
- change visibility state
- change formatting
- change row heights
- change column widths
- modify validations
- modify named ranges
- modify protection
- insert rows
- delete rows
- insert columns
- delete columns
- merge/unmerge cells
- alter print settings
- alter filters
- alter freeze panes
- alter comments/notes
- alter hyperlinks
- alter any workbook-owned metadata belonging to those sheets

Non-Template sheets are for reading and analysis only.

---

# 113. Template-Only Write Rule

Agent 2 may modify only intended product-entry cells on the `Template` sheet.

Configured row boundary:

- Rows 1–6: READ-ONLY
- Row 6: usually Amazon example/reference product row
- Product entry starts at row 7
- Rows 7 onward: writable only where the template defines valid product-input cells

Agent 2 must not modify Template cells outside the intended product-entry region.

If a formula, locked cell, system field, lookup cell or non-input region exists on Template:

do not write to it.

Allowed write scope:

`Template!<valid product input cells from row 7 downward>`

Everything else is read-only.

---

# 114. Non-Destructive Structural Analysis

Agent 2 must analyze hidden columns, grouped columns, hidden rows and workbook structures without permanently changing workbook state.

Preferred method:

- read hidden/grouping metadata programmatically
- inspect hidden columns/rows directly
- read values without unhide operations
- preserve visibility state exactly

Do not unhide other sheets or alter their visibility merely for inspection.

On the Template sheet, if analysis requires logical expansion, perform it in memory or in a temporary analysis copy, not in the final source workbook.

Final workbook must preserve original structure except for intended product values inserted into Template rows 7+.

---

# 115. Worksheet Integrity Check

Before finalizing the feed, compare all non-Template sheets byte/logical structure where practical.

Verify that there were no unintended changes to:

- values
- formulas
- styles
- dimensions
- validations
- named ranges
- visibility
- protection
- merged cells
- metadata

If any non-Template sheet changed:

`NON_TEMPLATE_SHEET_MODIFIED`

The feed must be blocked.

For Template verify:

- rows 1–6 unchanged
- row 6 unchanged
- only approved rows 7+ changed
- only approved input cells changed
- no unintended formulas/styles/metadata modified

If violation detected:

`TEMPLATE_WRITE_SCOPE_VIOLATION`

---

# 116. Humanizer + Template Fill Sequence

The write sequence must be:

1. Read Agent 1 canonical data
2. Read and study all relevant non-Template sheets
3. Build schema and mapping
4. Resolve clarifying questions
5. Run dry-run validation
6. Apply Humanizer meaning-preserving cleanup
7. Write values only into Template row 7+
8. Save to a new output file
9. Reopen output file
10. Verify rows 1–6 unchanged
11. Verify all non-Template sheets unchanged
12. Verify only intended Template input cells changed
13. Mark READY_FOR_UPLOAD only if all checks pass

---

# 117. Final Mutation Policy

Hard rule:

**READ EVERYTHING NEEDED. MODIFY ONLY TEMPLATE PRODUCT CELLS FROM ROW 7 DOWNWARD.**

All other workbook content is immutable.

Any attempt or accidental change outside the permitted write scope is a blocking error.


---

# 118. Final Readiness Gate

After the feed file is generated, Agent 2 must perform a complete final integrity and correctness audit before the file can be considered upload-ready.

There are only two final file-level readiness states:

- `READY_FOR_AMAZON_UPLOAD`
- `NOT_READY_FOR_AMAZON_UPLOAD`

If ANY hard rule, required condition, structural rule, data rule, mapping rule, validation rule, workbook-integrity rule, identifier rule, pricing rule, enum rule, or user-approved condition is violated:

the entire file status must become:

`NOT_READY_FOR_AMAZON_UPLOAD`

There is no partial "ready" state for the final file.

---

# 119. Mandatory Post-Generation Full Audit

After the workbook is written and saved, Agent 2 must:

1. Close the generated workbook
2. Reopen the generated workbook
3. Re-read the entire relevant Template data area
4. Re-check workbook integrity
5. Re-check all non-Template sheets for unintended changes
6. Re-check rows 1–6
7. Re-check row 6 example/reference integrity
8. Re-check every populated row from row 7 onward
9. Re-check every populated field
10. Re-check all required fields
11. Re-check all conditionally required fields
12. Re-check all enums
13. Re-check all identifiers
14. Re-check all prices and currencies
15. Re-check all dates
16. Re-check all units
17. Re-check all content fields
18. Re-check all operation-intent semantics
19. Re-check all cross-field dependencies
20. Re-check formula injection protection
21. Re-check row uniqueness
22. Re-check product-to-row alignment
23. Re-check mapping provenance
24. Re-check template fingerprint / structure
25. Re-check approval hash where approval is required

This is the final mandatory QA gate.

---

# 120. Final Audit Scope

The final audit must validate at minimum:

## Workbook Integrity
- workbook opens successfully
- correct file type preserved
- macros preserved where applicable
- no corruption
- no missing sheets
- no renamed sheets
- no reordered sheets if prohibited
- no unintended visibility changes
- no broken formulas
- no broken named ranges
- no broken validations
- no altered protection outside intended scope

## Non-Template Sheet Integrity
- no values changed
- no formulas changed
- no formatting changed
- no validation changed
- no named ranges changed
- no visibility changed
- no protection changed
- no structural mutation

## Template Integrity
- rows 1–6 unchanged
- row 6 unchanged
- row 6 still treated as Amazon example/reference row
- only approved input cells from row 7 downward changed
- no unintended formatting or system-cell changes
- no row drift
- no accidental overwrites

## Data Integrity
- correct SKU
- correct EAN / UPC / GTIN / ASIN handling
- correct GTIN exemption behavior
- correct Product Type
- correct marketplace
- correct currency
- correct country of origin
- correct compatibility
- correct content
- correct pricing
- correct quantity tiers
- correct operation intent

## Schema Compliance
- required fields populated
- conditionally required fields satisfied
- valid data types
- accepted enums
- valid units
- valid lengths
- valid occurrence counts
- valid dependencies
- valid update semantics

## Agent 1 Handoff Integrity
- no unauthorized meaning changes
- source values mapped correctly
- changed_fields respected
- locked fields respected
- blocked records not inserted as upload-ready
- approval scope respected

---

# 121. Any Violation = NOT READY

If one or more violations are found:

Set:

`file_status = NOT_READY_FOR_AMAZON_UPLOAD`

Do not present the file as final or upload-ready.

Do not silently correct meaning-critical issues.

Do not hide violations.

Do not downgrade a hard violation to a warning merely to complete the file.

---

# 122. Violation Report

When the file is NOT READY, Agent 2 must produce a detailed violation report.

For every violation include where applicable:

- Severity
- Error Code
- SKU
- Amazon Row
- Worksheet
- Column Letter
- Column Header
- Amazon Field
- Cell Coordinate
- Current Value
- Expected / Allowed Value
- Agent 1 Source Path
- Source Value
- Violation Description
- Why It Matters
- Proposed Correction
- Correction Type
- Whether Meaning Changes
- Whether User Confirmation Is Required

Example structure:

| Severity | SKU | Row | Column | Field | Current Value | Issue | Proposed Fix |
|---|---|---:|---|---|---|---|---|
| BLOCKER | ABC123 | 14 | K | item_name | ... | Title exceeds limit | Shorten title |
| BLOCKER | ABC124 | 15 | B | external_product_id | 12345 | Invalid EAN length | User input required |
| BLOCKER | ABC125 | 16 | AQ | country_of_origin | blank | Required field missing | Provide country |

---

# 123. Violation Grouping

For large batches, Agent 2 should group similar violations.

Examples:

- 47 rows missing Country of Origin
- 18 rows with invalid enum in the same column
- 7 rows with duplicate GTIN
- 3 rows with sale date errors

Provide:

- summary by issue type
- affected row range / SKU list
- detailed report artifact

Avoid asking the same correction question dozens of times.

---

# 124. Correction Approval Workflow

If the file is NOT READY:

1. Agent 2 displays the violations
2. Agent 2 proposes corrections
3. Agent 2 identifies which corrections are safe and which require user decision
4. Agent 2 waits for user confirmation for any correction that requires approval
5. Agent 2 applies only approved corrections
6. Agent 2 regenerates the affected file/rows
7. Agent 2 reruns the FULL final audit
8. Agent 2 produces a new file version

No file becomes upload-ready merely because corrections were applied.

The corrected file must pass the entire audit again.

---

# 125. Safe vs Approval-Required Corrections

## Safe corrections may include:

- exact enum normalization
- exact unit formatting
- exact date formatting
- whitespace cleanup
- safe decimal formatting
- safe boolean formatting
- formula-injection neutralization
- preserving leading zeros
- restoration of intended cell text type
- restoration of workbook state where no product meaning changes

## User approval required for:

- Product Type change
- identifier correction
- GTIN / UPC / EAN replacement
- Country of Origin
- model change
- compatibility change
- pack quantity change
- claim change
- content meaning change
- price logic change
- operation intent change
- variation structure change
- catalog conflict resolution
- destructive action

If uncertain whether meaning changes:

treat correction as approval-required.

---

# 126. Correction Versioning

Every correction cycle must create a new version.

Example:

`Feed_DE_B20261006_v1.xlsx`
→ NOT READY

after approved correction:

`Feed_DE_B20261006_v2.xlsx`

Store:

- prior version
- correction reason
- corrected fields
- user approval reference
- new hashes
- new validation result

Never overwrite the prior failed version silently.

---

# 127. Revalidation After Correction

After every correction cycle, rerun:

- L1 Workbook Integrity
- L2 Template Schema
- L3 Field/Data Validation
- L4 Cross-Field Business Logic
- Full Post-Generation Audit

Do not run only a partial check on the corrected field.

A correction may create a downstream conflict.

---

# 128. Final Ready State

Only after zero unresolved hard violations remain may Agent 2 set:

`file_status = READY_FOR_AMAZON_UPLOAD`

Final summary should include:

- Total rows checked
- Total SKUs checked
- Hard violations: 0
- Unresolved required fields: 0
- Invalid enums: 0
- Identifier conflicts: 0
- Price conflicts: 0
- Workbook scope violations: 0
- Non-Template mutations: 0
- Rows 1–6 modifications: 0
- Template integrity: PASS
- Data integrity: PASS
- Final audit: PASS

---

# 129. Final File Delivery Rule

Agent 2 must never label or deliver a file as ready for Amazon upload before the full audit passes.

If violations exist:

deliver the file only as:

`NOT_READY_FOR_AMAZON_UPLOAD`

and accompany it with:

- violation report
- proposed fixes
- required user confirmations
- affected rows/columns/cells

After user confirmation and corrections:

produce a NEW corrected file
→ rerun full audit
→ only then mark READY_FOR_AMAZON_UPLOAD if all checks pass.

---

# 130. Final QA Loop

Final mandatory loop:

Generate Feed
→ Save
→ Close
→ Reopen
→ Full Integrity Audit
→ Full Data Audit
→ Violations?

YES
→ NOT_READY_FOR_AMAZON_UPLOAD
→ Show exact rows / columns / cells / values / issues
→ Ask for required approval
→ Apply approved corrections
→ Create new file version
→ Full audit again

NO
→ READY_FOR_AMAZON_UPLOAD

This loop continues until either:

- the file passes all checks, or
- the user stops the correction process.

