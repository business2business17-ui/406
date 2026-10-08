#!/usr/bin/env python3
"""Agent 1 build for MOBILIUS AirPods cases, Amazon US (batch US-AIRPODS-20261007-001).

Reads the two series files, writes listing content by the rules of SEO-Rules.md, validates every
record with seo_check.py and writes:
  output/jsonl/handoff_US_batch001.jsonl      canonical handoff records (one per SKU)
  output/json/global_product_data_US.json     global product facts per series
  output/xlsx/AirPods_US_Agent1_Review_batch001.xlsx
  output/issues/issues_US_batch001.csv, batch_summary.md, seo_sanitization_report.md
Nothing is invented: price, stock, shipping template and the dangerous goods declaration are
missing in the input and stay DATA_REQUIRED.
"""
import argparse
import csv
import datetime
import hashlib
import json
import os
import re
import sys
from collections import Counter

import openpyxl
from decimal import Decimal, ROUND_HALF_UP, ROUND_CEILING

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import seo_check as sc  # noqa: E402

MARKETPLACE = "US"
LANGUAGE = "en_US"
CURRENCY = "USD"
BATCH_ID = "US-AIRPODS-20261007-001"
GENERATED_AT = "2026-10-07T00:00:00Z"
RECORD_VERSION = "1.6.0"
PREVIOUS_RECORD_VERSION = "1.5.0"
SALE_PRICE_INPUT = Decimal("22.99")  # user input 2026-10-07: Sale Price 22.99 USD
QUANTITY = 1
SHIPPING_TEMPLATE = "Migrated Template"  # user typed "Mirgrated template"; the only valid value of the template
AGENT_VERSION = "agent1-amazon-product-intelligence/2026-10-07"
SCHEMA_VERSION = "1.0.0"
VERSIONS = {
    "product_data_version": "ttx-user-2026-10-06",
    "catalog_source_version": "catalog_406_u001q212_u001q276_2026-09-14",
    "seo_version": "SEO-Rules v1.1 + AirPods_US_SEO.xlsx 2026-09-26 + Helium10 MCP 2026-10-07",
    "seo_source_date": "2026-09-26",
    "pricing_policy_version": None,
    "amazon_policy_version": "title-75/highlights-125 announcement 2026-06-10, effective 2026-07-27",
    "evidence_version": "evidence-2026-10-07",
}

SERIES = {
    "pro": {
        "file": "Airpods pro_Pro2_406516.xlsx",
        "parent_sku": "406516U-PARENT",
        "title_base": "MOBILIUS Case for AirPods Pro 2nd/1st Generation, ",
        "compat_models": ["Apple AirPods Pro", "Apple AirPods Pro (2nd generation)"],
        "compat_generations": ["1st generation", "2nd generation"],
        "validator_series": "pro",
        "bullet1": ("AirPods Pro 2 case cover: Fits Apple AirPods Pro 2nd generation and AirPods Pro 1st generation "
                    "charging cases; the same AirPods Pro case cover fits both generations; earbuds and charging case not included"),
        "fit_phrase": "the AirPods Pro charging case",
        "desc_open": ("MOBILIUS AirPods Pro 2 case cover for AirPods Pro 2nd generation and AirPods Pro 1st generation. "
                      "The same case fits both generations."),
        "backend": "air pod pods airpod airpodpro podspro procase podspro2",
    },
    "airpods4": {
        "file": "Airpods4_406517.xlsx",
        "parent_sku": "406517-PARENT",
        "title_base": "MOBILIUS Case for AirPods 5 and AirPods 4, ",
        "compat_models": ["Apple AirPods (4th generation)", "Apple AirPods (5th generation)"],
        "compat_generations": ["4th generation", "5th generation"],
        "validator_series": "airpods4",
        "bullet1": ("AirPods 5 case cover: Fits Apple AirPods 5th generation and AirPods 4th generation charging cases; "
                    "the same AirPods 4 case cover fits both generations; earbuds and charging case not included"),
        "fit_phrase": "the AirPods 4 and AirPods 5 charging cases",
        "desc_open": ("MOBILIUS AirPods 5 case cover for AirPods 5th generation and AirPods 4th generation. "
                      "The same case fits both generations."),
        "backend": "air pod pods airpod pods4",
    },
}

# Title short names for the Pro series (room for the print name is 25 characters); user rule: unique inside the parent
PRO_SHORT = {
    "q212": "Desert Climbing Stamps", "q220": "Lighthouse Falcon Stamps", "q221": "Blueberries Blue Blossoms",
    "q224": "Reclining Leopard", "q225": "Mosaic Cat Pineapples", "q230": "Spiky Hair Green Flask",
    "q235": "Class Vibes Collage", "q239": "No Risk No Story", "q241": "Good Vibes Lettering",
    "q261": "Stretching Leopard",
}

# Theme (valid values of the template) classified from the print name. None = no clear valid value.
THEME = {
    "q212": "Nature", "q213": "Nature", "q214": "Floral", "q215": "Floral", "q216": None, "q217": "Floral",
    "q218": "Food & Beverage", "q219": "Nature", "q220": "Nature", "q221": "Floral", "q222": "Food & Beverage",
    "q223": "Cartoon", "q224": "Animal", "q225": "Animal", "q226": "Animal", "q227": "Animal", "q228": "Animal",
    "q229": "Animal", "q230": "Cartoon", "q231": "Cartoon", "q232": "Cartoon", "q233": "Animal", "q234": "Music",
    "q235": None, "q236": "Music", "q237": "Animal", "q238": "Animal", "q239": "Alphabet", "q240": "Animal",
    "q241": "Alphabet", "q242": None, "q243": None, "q244": None, "q245": "Animal", "q246": "Animal",
    "q247": "Animal", "q248": None, "q249": "Halloween", "q250": "Halloween", "q251": None, "q252": "Floral",
    "q253": "Nature", "q254": "Animal", "q255": "Animal", "q256": None, "q257": "Animal", "q258": None,
    "q259": "Animal", "q260": "Animal", "q261": "Animal", "q262": "Animal", "q263": "Cartoon", "q264": "Animal",
    "q265": "Cartoon", "q266": None, "q267": "Animal", "q268": "Animal", "q269": "Bird", "q270": None,
    "q271": "Fantasy", "q272": "Animal", "q273": None, "q274": None, "q275": "Halloween", "q276": None,
}
VERIFIED_IMAGE_MATCH = {"q212", "q218", "q222", "q230", "q239", "q246", "q251"}  # checked one by one in the session

FACTS = {  # user-confirmed product facts (TTX), source USER_INPUT
    "brand": "MOBILIUS", "manufacturer": "MOBILIUS", "material": "Thermoplastic Polyurethane",
    "coating": "soft-touch coating", "shell_type": "Soft", "average_thickness_mm": 2.5, "country_of_origin": "China",
    "item_length_mm": 64, "item_width_mm": 48, "item_height_mm": 25, "item_weight_g": 30,
    "package_length_mm": 74, "package_width_mm": 58, "package_height_mm": 35, "package_weight_g": 40,
    "package_contents": "one case and one carabiner keychain", "construction": "two parts, top and base",
    "number_of_items": 1, "fulfillment": "MFN (merchant-fulfilled)",
}


def money(x):
    return float(Decimal(x).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP))


def apply_rule(rule, p, base_fallback=None):
    """rule = {"base": sale_price|standard_price|business_price, "op": discount_pct|markup_pct|fixed_amount, "value": number}"""
    base = p.get(rule["base"])
    if base is None:
        base = base_fallback
    if base is None:
        return None
    b, v = Decimal(str(base)), Decimal(str(rule["value"]))
    if rule["op"] == "discount_pct":
        r = b * (Decimal(100) - v) / Decimal(100)
    elif rule["op"] == "markup_pct":
        r = b * (Decimal(100) + v) / Decimal(100)
    elif rule["op"] == "fixed_amount":
        r = b + v
    else:
        raise ValueError("unknown rule op " + str(rule["op"]))
    return money(r)


def derive_extra_prices(p, policy):
    """Min/max allowed price, business price and quantity tiers: only from the configured policy, never invented."""
    if not policy:
        return
    sale_ref = p["sale_price"] if p["sale_price"] is not None else p["input_value"]
    min_rule = policy.get("min_price_rule")
    if min_rule and min_rule.get("base") != "quantity_tier":
        p["minimum_seller_allowed_price"] = apply_rule(min_rule, p, sale_ref)
    if policy.get("max_price_rule"):
        p["maximum_seller_allowed_price"] = apply_rule(policy["max_price_rule"], p, sale_ref)
    if policy.get("business_price_rule"):
        p["business_price"] = apply_rule(policy["business_price_rule"], p, sale_ref)
    thresholds = policy.get("quantity_tier_thresholds") or []
    if thresholds and not policy.get("quantity_tiers"):
        p["quantity_tier_thresholds"] = thresholds
        p["quantity_tiers_status"] = "RATES_NOT_APPROVED"
    tiers = policy.get("quantity_tiers") or []
    if tiers:
        p["quantity_price_type"] = policy.get("quantity_price_type", "Percent")
        out = []
        base = p["business_price"] if p["business_price"] is not None else p["standard_price"]
        for t in tiers:
            pct = t.get("discount_pct", t.get("value") if p["quantity_price_type"] == "Percent" else None)
            price = money(Decimal(str(base)) * (Decimal(100) - Decimal(str(pct))) / Decimal(100)) if (base is not None and pct is not None) else t.get("value")
            if p["quantity_price_type"] == "Percent":
                out.append({"lower_bound": t["lower_bound"], "discount_pct": pct, "resulting_unit_price": price})
            else:
                e = {"lower_bound": t["lower_bound"], "fixed_price": price, "resulting_unit_price": price}
                if pct is not None:
                    e["discount_pct_of_business_price"] = pct
                out.append(e)
        p["quantity_tiers"] = out
        if min_rule and min_rule.get("base") == "quantity_tier":  # minimum = resulting unit price of the named tier
            hit = [t for t in out if t["lower_bound"] == min_rule["lower_bound"]]
            p["minimum_seller_allowed_price"] = hit[0]["resulting_unit_price"] if hit else None
    p["policy_rules"] = {k: policy[k] for k in ("min_price_rule", "max_price_rule", "business_price_rule", "quantity_price_type", "quantity_tiers", "quantity_tier_thresholds") if policy.get(k)}
    # order checks: min <= sale <= standard <= max; tier prices strictly decreasing and not below the minimum price
    msgs = []
    std = p["standard_price"]
    if p["minimum_seller_allowed_price"] is not None and p["minimum_seller_allowed_price"] > sale_ref:
        msgs.append("minimum allowed price is above the sale price")
    if p["maximum_seller_allowed_price"] is not None and std is not None and p["maximum_seller_allowed_price"] < std:
        msgs.append("maximum allowed price is below the standard price")
    if p["minimum_seller_allowed_price"] is not None and p["maximum_seller_allowed_price"] is not None \
            and p["minimum_seller_allowed_price"] > p["maximum_seller_allowed_price"]:
        msgs.append("minimum allowed price is above the maximum allowed price")
    if p["business_price"] is not None and p["business_price"] > sale_ref:
        msgs.append("business price is above the sale price (policy: business_price <= sale_price < standard_price)")
    if p["business_price"] is not None and std is not None and p["business_price"] > std:
        msgs.append("business price is above the standard price")
    last = p["business_price"] if p["business_price"] is not None else None
    bounds = [t["lower_bound"] for t in p.get("quantity_tiers", [])]
    if bounds != sorted(set(bounds)):
        msgs.append("quantity lower bounds must be ascending and unique")
    for t in p.get("quantity_tiers", []):
        up = t["resulting_unit_price"]
        if up is None:
            continue
        if last is not None and up >= last:
            msgs.append(f"quantity tier {t['lower_bound']} price {up} is not below the previous level {last}")
        if p["minimum_seller_allowed_price"] is not None and up < p["minimum_seller_allowed_price"]:
            msgs.append(f"quantity tier {t['lower_bound']} price {up} is below the minimum allowed price")
        last = up
    if msgs:
        p["policy_conflicts"] = msgs
        p["status"] = "PRICE_POLICY_CONFLICT"


def price_block(a):
    """Pricing layer. The user gave one price and the default input field is sale_price.
    Other price fields are derived only from an explicit pricing policy; nothing is invented."""
    p = {"input_field": "sale_price", "input_value": money(SALE_PRICE_INPUT), "currency": CURRENCY,
         "sale_price": money(SALE_PRICE_INPUT), "standard_price": None, "list_price": 0, "map_price": None,
         "minimum_seller_allowed_price": None, "maximum_seller_allowed_price": None, "business_price": None,
         "sale_start_date": a.sale_start, "sale_end_date": a.sale_end, "pricing_policy_version": None,
         "formula": None, "raw_result": None, "rounding": None, "missing": [], "status": "PRICE_DATA_REQUIRED"}
    if a.pricing_mode == "standard_equals_sale":
        p.update(standard_price=money(SALE_PRICE_INPUT), sale_price=None, sale_start_date=None, sale_end_date=None,
                 pricing_policy_version="STANDARD_EQUALS_INPUT_v1", formula="standard_price = input price; no promotion", rounding="2_DECIMALS")
    elif a.pricing_mode == "explicit_standard":
        p.update(standard_price=money(Decimal(str(a.standard_price))), pricing_policy_version=a.pricing_policy_version or "EXPLICIT_STANDARD_USER",
                 formula="standard_price given by the user", rounding="2_DECIMALS")
    elif a.pricing_mode == "reverse_discount":
        raw = SALE_PRICE_INPUT / Decimal(str(a.discount_factor))
        if a.rounding == "END_99":
            val = raw.to_integral_value(rounding=ROUND_CEILING) - Decimal("0.01")
            if val < raw:
                val += Decimal("1")
        else:
            val = raw
        p.update(standard_price=money(val), pricing_policy_version=a.pricing_policy_version or "REVERSE_DISCOUNT_" + str(a.discount_factor),
                 formula=f"standard_price = sale_price / {a.discount_factor}", raw_result=float(raw), rounding=a.rounding,
                 check_standard_times_factor=money(Decimal(str(money(val))) * Decimal(str(a.discount_factor))))
    else:
        p["missing"].append("standard_price (pricing policy not provided)")
    if p["sale_price"] is not None:
        if not p["sale_start_date"]:
            p["missing"].append("sale_start_date")
        if not p["sale_end_date"]:
            p["missing"].append("sale_end_date")
        if p["sale_start_date"] and p["sale_end_date"]:
            d0 = datetime.date.fromisoformat(p["sale_start_date"])
            d1 = datetime.date.fromisoformat(p["sale_end_date"])
            if d1 < d0:
                p["status"] = "PRICE_CONFLICT"
                p["missing"].append("sale window: end date is before the start date")
    if p["standard_price"] is not None and p["sale_price"] is not None and p["standard_price"] <= p["sale_price"]:
        p["status"] = "PRICE_CONFLICT"
    elif not p["missing"] and p["status"] != "PRICE_CONFLICT":
        p["status"] = "PRICE_VALID"
    if p["status"] == "PRICE_VALID":
        derive_extra_prices(p, a.policy)
    # shared policy 2026-10-08-v2: handoff fields and the calculation audit
    p["price_input_type"] = "sale_price"
    p["pricing_basis"] = "SALE"
    if a.policy.get("business_price_rule"):
        r_ = a.policy["business_price_rule"]
        p["business_discount_rate"] = r_["value"] / 100
        p["business_price_basis"] = "SALE" if r_["base"] == "sale_price" else r_["base"].upper()
        p["business_price_status"] = "CALCULATED" if p["business_price"] is not None else "NOT_CALCULATED"
    else:
        p["business_price_status"] = "NOT_APPROVED"
    audit = [{"field": "sale_price", "input": float(SALE_PRICE_INPUT), "formula": "preserved unchanged", "rounded": p["input_value"]}]
    if p["standard_price"] is not None and p.get("raw_result") is not None:
        audit.append({"field": "standard_price", "input": p["input_value"], "policy": p["pricing_policy_version"], "formula": p["formula"],
                      "unrounded": p["raw_result"], "rounded": p["standard_price"], "rounding": "ROUND_HALF_UP to 0.01"})
    if p["business_price"] is not None:
        audit.append({"field": "business_price", "input": p["input_value"], "policy": p["pricing_policy_version"],
                      "formula": "business_price = sale_price x (1 - %s)" % (p["business_discount_rate"]),
                      "unrounded": float(Decimal(str(p["input_value"])) * (Decimal(1) - Decimal(str(p["business_discount_rate"])))),
                      "rounded": p["business_price"], "rounding": "ROUND_HALF_UP to 0.01"})
    for fld in ("minimum_seller_allowed_price", "maximum_seller_allowed_price"):
        if p[fld] is None:
            audit.append({"field": fld, "status": "NOT_APPROVED: needs its own guardrail policy"})
    p["pricing_calculations"] = audit
    return p


def sha(obj):
    return hashlib.sha256(json.dumps(obj, sort_keys=True, ensure_ascii=False).encode("utf-8")).hexdigest()


def load_series(key):
    ws = openpyxl.load_workbook(os.path.join(HERE, SERIES[key]["file"]), read_only=True)["Sheet"]
    rows = list(ws.iter_rows(values_only=True))
    hdr = rows[0]
    out = []
    for r in rows[1:]:
        if not r[0]:
            continue
        d = dict(zip(hdr, r))
        out.append({"sku": str(d["Артикул"]), "color": str(d["Color / Pattern"]).strip(),
                    "model": str(d["Модель"]), "image_desc": str(d["Image Description"]),
                    "amazon_desc": str(d["Amazon Description"]),
                    "photos": [d.get(f"Фото {i}") for i in range(1, 7)]})
    return out


def build_content(key, row):
    s = SERIES[key]
    q = row["sku"][-4:]
    name = row["color"].split(" / ", 1)[1]
    short = PRO_SHORT.get(q, name) if key == "pro" else name
    title = s["title_base"] + short
    highlight = "TPU Soft-Touch Coating, Two-Piece Design, Carabiner Keychain Included, Average 2.5 mm Thickness"
    bullets = [
        s["bullet1"],
        "TPU material: Made from TPU with a soft-touch coating; average thickness 2.5 mm",
        f"Print design: {name} printed on the front of the black case",
        f"Two-piece design: Top and base parts fit around {s['fit_phrase']}; opening for the charging cable",
        "Carabiner keychain included: One case and one carabiner keychain in the package; attach it to a bag, backpack, or belt loop",
    ]
    description = (f"{s['desc_open']} {name} is printed on the front of the black case. "
                   "The case is made from TPU with a soft-touch coating and has an average thickness of 2.5 mm. "
                   "It consists of a top part and a base part, with an opening for the charging cable. "
                   "The package contains one case and one carabiner keychain. "
                   "The earbuds and the charging case are not included.")
    return {"title": title, "item_highlights": highlight, "bullet_points": bullets, "description": description,
            "backend_search_terms": s["backend"], "backend_bytes": len(s["backend"].encode("utf-8")),
            "print_name": name, "title_short_name": short}


def validate(key, row, content):
    listing = {"sku": row["sku"], "series": SERIES[key]["validator_series"], "title": content["title"],
               "highlight": content["item_highlights"], "bullets": content["bullet_points"],
               "description": content["description"], "backend": content["backend_search_terms"]}
    return sc.check(listing)


def attributes(key, row, content, price):
    s = SERIES[key]
    q = row["sku"][-4:]
    theme = THEME[q]
    A = []

    def add(attr, value, req, source, conf, status, note=""):
        A.append({"attribute": attr, "value": value, "required": req, "source": source, "confidence": conf,
                  "status": status, "note": note})
    add("product_type", "PORTABLE_ELECTRONIC_DEVICE_COVER", "Required", "TEMPLATE", "HIGH", "VALID", "locked")
    add("item_name", content["title"], "Required", "CALCULATED", "HIGH", "VALID")
    add("brand", FACTS["brand"], "Required", "USER_INPUT", "HIGH", "VALID")
    add("manufacturer", FACTS["manufacturer"], "Conditionally Required", "USER_INPUT", "HIGH", "VALID")
    add("product_id_type", "GTIN Exempt", "Required", "USER_INPUT", "HIGH", "VALID", "exemption approved by the user")
    add("item_type_keyword", "headphone-cases", "Optional", "TEMPLATE", "HIGH", "VALID", "single valid value")
    add("product_description", content["description"], "Required", "CALCULATED", "HIGH", "VALID")
    add("bullet_points", " | ".join(content["bullet_points"]), "Required", "CALCULATED", "HIGH", "VALID")
    add("generic_keyword", content["backend_search_terms"], "Optional", "CALCULATED", "HIGH", "VALID")
    add("title_differentiation", content["item_highlights"], "Recommended", "CALCULATED", "HIGH", "VALID")
    add("material", FACTS["material"], "Recommended", "USER_INPUT", "HIGH", "VALID")
    add("shell_type", FACTS["shell_type"], "Conditionally Required", "USER_INPUT", "HIGH", "VALID")
    add("color", row["color"], "Conditionally Required", "TTX_FILE", "HIGH", "VALID", "print name; variations are not used (user decision 2026-10-07)")
    add("number_of_items", FACTS["number_of_items"], "Conditionally Required", "USER_INPUT", "HIGH", "VALID")
    add("form_factor", "Case", "Conditionally Required", "DERIVED_FROM_PRODUCT_TYPE", "MEDIUM", "WARNING", "valid value Case; confirm")
    add("compatible_headphone_models", "; ".join(s["compat_models"]), "Conditionally Required", "USER_INPUT", "HIGH", "VALID", "official valid values")
    add("compatible_devices", "Headphones", "Conditionally Required", "DERIVED_FROM_BROWSE_NODE", "MEDIUM", "WARNING", "valid value; confirm")
    add("theme", theme, "Conditionally Required", "CLASSIFIED_FROM_PRINT_NAME", "MEDIUM" if theme else "LOW",
        "WARNING" if theme else "DATA_REQUIRED", "no clear valid value for this print" if not theme else "classification from the print name; review")
    add("special_features", None, "Conditionally Required", "USER_INPUT", "HIGH", "VALID", "left empty by decision (no claims, Key Ring not added)")
    add("style", None, "Conditionally Required", "NOT_PROVIDED", "LOW", "DATA_REQUIRED", "condition not resolvable from the template text; Agent 2 resolves with the Product Type Definition")
    add("coverage", None, "Conditionally Required", "NOT_PROVIDED", "LOW", "DATA_REQUIRED", "same as style")
    add("item_length_mm", FACTS["item_length_mm"], "Recommended", "USER_INPUT", "HIGH", "VALID", "average size, also used for AirPods 4")
    add("item_width_mm", FACTS["item_width_mm"], "Recommended", "USER_INPUT", "HIGH", "VALID")
    add("item_height_mm", FACTS["item_height_mm"], "Recommended", "USER_INPUT", "HIGH", "VALID")
    add("item_weight_g", FACTS["item_weight_g"], "Recommended", "USER_INPUT", "HIGH", "VALID")
    add("item_package_length_mm", FACTS["package_length_mm"], "Conditionally Required", "USER_INPUT", "HIGH", "VALID", "case size + 5 mm each side")
    add("item_package_width_mm", FACTS["package_width_mm"], "Conditionally Required", "USER_INPUT", "HIGH", "VALID")
    add("item_package_height_mm", FACTS["package_height_mm"], "Conditionally Required", "USER_INPUT", "HIGH", "VALID")
    add("package_weight_g", FACTS["package_weight_g"], "Conditionally Required", "USER_INPUT", "HIGH", "VALID", "carabiner included")
    add("country_of_origin", FACTS["country_of_origin"], "Required", "USER_INPUT", "HIGH", "VALID")
    add("dangerous_goods_regulations", "Not Applicable", "Required", "USER_INPUT", "HIGH", "VALID", "confirmed by the user 2026-10-07")
    add("item_condition", "New", "Conditionally Required", "ASSUMED_NEW_PRODUCT", "MEDIUM", "WARNING", "confirm with the offer data")
    add("fulfillment_channel_code", "Fulfillment by Merchant (Default)", "Conditionally Required", "USER_INPUT", "HIGH", "VALID", "MFN")
    add("quantity", QUANTITY, "Conditionally Required", "USER_INPUT", "HIGH", "VALID", "user input 2026-10-07")
    add("shipping_template", SHIPPING_TEMPLATE, "Conditionally Required", "USER_INPUT", "HIGH", "VALID",
        "user typed 'Mirgrated template'; normalized to the only valid value 'Migrated Template'")
    add("sale_price_usd", price["sale_price"] if price["sale_price"] is not None else price["input_value"], "Optional", "USER_INPUT", "HIGH",
        "VALID" if price["sale_price"] is not None else "WARNING",
        "user input Sale Price 22.99 USD" + ("" if price["sale_price"] is not None else "; used as the standard price, no promotion"))
    add("your_price_usd_standard_price", price["standard_price"], "Optional", "CALCULATED" if price["standard_price"] is not None else "NOT_PROVIDED",
        "HIGH" if price["standard_price"] is not None else "LOW", "VALID" if price["standard_price"] is not None else "DATA_REQUIRED",
        price["formula"] or "needs a pricing policy (the template has Your Price and Sale Price as separate fields)")
    add("sale_start_date", price["sale_start_date"], "Optional", "USER_INPUT" if price["sale_start_date"] else "NOT_PROVIDED", "HIGH" if price["sale_start_date"] else "LOW",
        "VALID" if (price["sale_start_date"] or price["sale_price"] is None) else "DATA_REQUIRED", "a sale price needs a start and an end date" if price["sale_price"] is not None else "no promotion")
    add("sale_end_date", price["sale_end_date"], "Optional", "USER_INPUT" if price["sale_end_date"] else "NOT_PROVIDED", "HIGH" if price["sale_end_date"] else "LOW",
        "VALID" if (price["sale_end_date"] or price["sale_price"] is None) else "DATA_REQUIRED", "a sale price needs a start and an end date" if price["sale_price"] is not None else "no promotion")
    add("list_price", 0, "Conditionally Required", "TEMPLATE_RULE", "MEDIUM", "WARNING", "template: enter 0 if unable to provide; not an MSRP")
    for nm, val in (("minimum_seller_allowed_price", price["minimum_seller_allowed_price"]), ("maximum_seller_allowed_price", price["maximum_seller_allowed_price"]),
                    ("business_price", price["business_price"])):
        if val is not None:
            add(nm, val, "Optional", "CALCULATED", "HIGH", "VALID", "from the configured pricing policy " + str(price["pricing_policy_version"]))
    if price.get("quantity_tiers_status") == "RATES_NOT_APPROVED":
        add("quantity_tier_thresholds", ", ".join(str(x) for x in price["quantity_tier_thresholds"]) + " units", "Optional", "USER_INPUT", "HIGH", "WARNING",
            "thresholds given by the user; tier rates are not approved (policy 2026-10-08-v2), so no quantity discount is sent")
    for t in price.get("quantity_tiers", []):
        add(f"quantity_tier_{t['lower_bound']}", json.dumps(t), "Optional", "CALCULATED", "HIGH", "VALID", "quantity price type " + str(price.get("quantity_price_type")))
    return A


def evidence(key, row, content):
    q = row["sku"][-4:]
    conf_img = "HIGH" if q in VERIFIED_IMAGE_MATCH else "MEDIUM"
    s = SERIES[key]
    E = [
        ("Brand and manufacturer", "MOBILIUS", "USER_INPUT", "chat 2026-10-04 / 2026-10-06", "HIGH", "VERIFIED"),
        ("Material", "TPU (thermoplastic polyurethane) with soft-touch coating", "USER_INPUT", "chat 2026-10-04", "HIGH", "VERIFIED"),
        ("Average thickness", "2.5 mm", "USER_INPUT", "chat 2026-10-04", "HIGH", "VERIFIED"),
        ("Package contents", "one case and one carabiner keychain", "USER_INPUT", "chat 2026-10-04 / 2026-10-05", "HIGH", "VERIFIED"),
        ("Compatibility", "; ".join(s["compat_models"]), "USER_INPUT", "chat 2026-10-04 / 2026-10-05", "HIGH", "VERIFIED"),
        ("Item size and weight", "64 x 48 x 25 mm, 30 g (average size, MFN)", "USER_INPUT", "chat 2026-10-06 / 2026-10-07", "HIGH", "VERIFIED"),
        ("Package size and weight", "74 x 58 x 35 mm, 40 g", "USER_INPUT", "chat 2026-10-06", "HIGH", "VERIFIED"),
        ("Country of origin", "China", "USER_INPUT", "chat 2026-10-05", "HIGH", "VERIFIED"),
        ("GTIN exemption", "approved in Seller Central", "USER_INPUT", "chat 2026-10-06", "HIGH", "VERIFIED"),
        ("Construction", "two parts, top and base", "PACKAGING_IMAGE", "Photo 5 (q212 checked)", "MEDIUM", "VERIFIED"),
        ("Print name", content["print_name"], "CATALOG", "catalog thumbnail " + row["sku"][-4:] + " and series file", conf_img,
         "VERIFIED" if conf_img == "HIGH" else "NEEDS_REVIEW"),
    ]
    return [dict(sku=row["sku"], attribute=a, value=v, source=so, evidence_location=loc, confidence=c, status=st)
            for a, v, so, loc, c, st in E]


GLOBAL_CLAIMS = [
    ("ALL", "lightweight / slim protection against everyday scratches and bumps", "series file (removed 2026-10-06)", "none", "UNSUPPORTED_CLAIM", "HIGH", "EXCLUDED", "removed from the source descriptions and never written"),
    ("ALL", "full access to the charging port / precise cut-outs", "series file (removed 2026-10-06)", "none", "UNSUPPORTED_CLAIM", "HIGH", "EXCLUDED", "removed; only 'opening for the charging cable' is stated"),
    ("ALL", "wireless charging supported", "image Photo 4", "no product test", "UNSUPPORTED_CLAIM", "HIGH", "EXCLUDED", "user decision: no claims"),
    ("ALL", "antimicrobial / waterproof / shockproof / scratch resistant / drop tested", "none", "none", "UNSUPPORTED_CLAIM", "HIGH", "EXCLUDED", "feed Special Features stays empty"),
    ("ALL", "DESIGNED FOR A CLOSE FIT (infographic text)", "image Photo 5", "image only", "AMBIGUOUS_CLAIM", "MEDIUM", "ACCEPTED_BY_USER_IN_IMAGE_ONLY", "not used in listing text"),
    ("ALL", "AirPods Pro 3 compatibility", "none", "none", "UNSUPPORTED_CLAIM", "HIGH", "EXCLUDED", "never mentioned"),
    ("ALL", "ANC variant of AirPods 4 case", "none", "none", "UNSUPPORTED_CLAIM", "HIGH", "EXCLUDED", "user: do not mention ANC"),
    ("ALL", "TPU with soft-touch coating, average thickness 2.5 mm, carabiner keychain included", "USER_INPUT", "TTX", "VERIFIED_CLAIM", "HIGH", "USED", ""),
    ("pro", "fits AirPods Pro (1st generation) and AirPods Pro 2", "USER_INPUT", "TTX", "VERIFIED_CLAIM", "HIGH", "USED", "same case dimensions"),
    ("airpods4", "fits AirPods 4 and AirPods 5", "USER_INPUT", "TTX", "VERIFIED_CLAIM", "HIGH", "USED", "same case dimensions"),
    ("q230", "design resembles a known animated character", "catalog thumbnail", "visual impression", "REGULATED_CLAIM", "MEDIUM", "TEXT_NEUTRALIZED", "described only by colors and shapes; rights decision stays with the user"),
    ("q246", "lettering 'Perfect Fit'", "catalog thumbnail", "image", "AMBIGUOUS_CLAIM", "MEDIUM", "RENAMED", "called 'Box Cat Lettering'; the words are not quoted"),
]

KEYWORDS = [  # phrase, series, SV, KS last complete week, tier, placement, status, reason
    ("airpods 5 case", "airpods4", 128552, 1650, "TIER_1_PRIMARY", "title words, bullet 1", "CONFIRMED", "SV>=500 and KS>=100"),
    ("airpods 4 case", "airpods4", 86564, 1196, "TIER_1_PRIMARY", "title words, bullet 1", "CONFIRMED", "SV>=500 and KS>=100"),
    ("airpod 5 case", "airpods4", 52972, 1262, "TIER_4_SEMANTIC", "backend (air, pod, pods, airpod)", "CONFIRMED", "spelling variant"),
    ("airpod 4 case", "airpods4", 42078, 1381, "TIER_4_SEMANTIC", "backend (air, pod, pods, airpod)", "CONFIRMED", "spelling variant; KS from file"),
    ("airpods 4 case cover", "airpods4", 7735, 299, "TIER_2_SECONDARY", "bullet 1 'AirPods 4 case cover'", "CONFIRMED", "KS from file"),
    ("airpods 5 case cover", "airpods4", 16172, None, "TIER_3_LONG_TAIL", "bullet 1 'AirPods 5 case cover'", "NO_COMPLETE_WEEK_DATA", "KS only for the incomplete week"),
    ("case for airpods 5", "airpods4", 4739, None, "TIER_3_LONG_TAIL", "title 'Case for AirPods 5'", "NO_COMPLETE_WEEK_DATA", ""),
    ("case for airpods 4", "airpods4", 3165, 105, "TIER_2_SECONDARY", "title 'Case for AirPods ... 4'", "CONFIRMED", "KS from file"),
    ("airpods 4th generation case", "airpods4", 663, 16, "TIER_3_LONG_TAIL", "bullet 1 fit statement", "BELOW_THRESHOLD", "fit statement required by product facts"),
    ("airpods 5th generation case", "airpods4", 559, None, "TIER_3_LONG_TAIL", "bullet 1 fit statement", "NO_COMPLETE_WEEK_DATA", "fit statement required by product facts"),
    ("air pods4 case", "airpods4", 4510, 145, "TIER_4_SEMANTIC", "backend (pods4)", "CONFIRMED", "KS from file"),
    ("airpods 5 case keychain", "airpods4", 467, None, "TIER_3_LONG_TAIL", "bullet 5 and highlights (keychain)", "NO_COMPLETE_WEEK_DATA", "keychain is a product fact"),
    ("airpods pro case", "pro", 32497, 796, "TIER_1_PRIMARY", "bullet 1 'AirPods Pro case cover'", "CONFIRMED", "KS from file; includes Pro 3 demand, used only with generation words"),
    ("airpods pro 2 case", "pro", 28847, 443, "TIER_1_PRIMARY", "title words, bullet 1 'AirPods Pro 2 case cover'", "CONFIRMED", "SV>=500 and KS>=100"),
    ("airpod pro case", "pro", 34020, 837, "TIER_4_SEMANTIC", "backend (airpod)", "CONFIRMED", "spelling variant"),
    ("airpods pro 2nd generation case", "pro", 2859, 78, "TIER_3_LONG_TAIL", "title '2nd/1st Generation', bullet 1", "BELOW_THRESHOLD", "fit statement required by product facts"),
    ("airpods pro 1st generation case", "pro", 663, 21, "TIER_3_LONG_TAIL", "title, bullet 1", "BELOW_THRESHOLD", "fit statement required by product facts"),
    ("airpods pro 2 case cover", "pro", 2210, 75, "TIER_3_LONG_TAIL", "bullet 1 exact phrase", "BELOW_THRESHOLD", "natural wording"),
    ("airpods pro case cover", "pro", 3177, 83, "TIER_3_LONG_TAIL", "bullet 1", "BELOW_THRESHOLD", "includes Pro 3 demand"),
    ("airpods 2 pro case; air podspro2 case", "pro", 1246, 26, "TIER_4_SEMANTIC", "backend (podspro2)", "BELOW_THRESHOLD", "spelling variants"),
    ("airpodpro case; air podspro case; airpod procase", "pro", 391, None, "TIER_4_SEMANTIC", "backend (airpodpro, podspro, procase)", "KS_NOT_CHECKED", "spelling variants"),
    ("airpods pro case with keychain; airpods case keychain", "pro", 540, 3, "TIER_3_LONG_TAIL", "bullet 5 and highlights (keychain)", "BELOW_THRESHOLD", "keychain is a product fact"),
    ("airpods pro 3 case", "pro", 202798, None, "EXCLUDE", "never", "EXCLUDED", "not our product"),
    ("airpods 1/2 case", "pro", 476, None, "EXCLUDE", "never", "EXCLUDED", "wrong product: AirPods 1 and 2"),
]


def parse_args():
    cfg = {}
    cfg_path = os.path.join(HERE, "pricing_input.json")
    if os.path.exists(cfg_path):
        cfg = json.load(open(cfg_path, encoding="utf-8"))
    ap = argparse.ArgumentParser(description="Agent 1 build, MOBILIUS AirPods cases, Amazon US. Price inputs come from pricing_input.json; options override it.")
    ap.add_argument("--pricing-mode", choices=["unresolved", "standard_equals_sale", "reverse_discount", "explicit_standard"],
                    default=cfg.get("pricing_mode", "unresolved"))
    ap.add_argument("--discount-factor", type=float, default=cfg.get("discount_factor"), help="reverse_discount: standard = sale / factor")
    ap.add_argument("--standard-price", type=float, default=cfg.get("standard_price"), help="explicit_standard: base price in USD")
    ap.add_argument("--rounding", choices=["2_DECIMALS", "END_99"], default=cfg.get("rounding", "2_DECIMALS"))
    ap.add_argument("--sale-start", default=cfg.get("sale_start_date"), help="YYYY-MM-DD, needed when a sale price is sent")
    ap.add_argument("--sale-end", default=cfg.get("sale_end_date"), help="YYYY-MM-DD")
    ap.add_argument("--pricing-policy-version", default=cfg.get("pricing_policy_version"))
    a = ap.parse_args()
    a.policy = {k: cfg.get(k) for k in ("min_price_rule", "max_price_rule", "business_price_rule", "quantity_price_type", "quantity_tiers", "quantity_tier_thresholds") if cfg.get(k)}
    if a.pricing_mode == "reverse_discount" and not a.discount_factor:
        ap.error("reverse_discount needs --discount-factor")
    if a.pricing_mode == "explicit_standard" and not a.standard_price:
        ap.error("explicit_standard needs --standard-price")
    return a


def main():
    args = parse_args()
    price = price_block(args)
    VERSIONS["pricing_policy_version"] = price["pricing_policy_version"]
    out_dirs = {k: os.path.join(HERE, "output", k) for k in ("json", "jsonl", "xlsx", "issues")}
    for p in out_dirs.values():
        os.makedirs(p, exist_ok=True)
    prev = {}
    prev_path = os.path.join(out_dirs["jsonl"], "handoff_US_batch001.jsonl")
    if os.path.exists(prev_path):
        for line in open(prev_path, encoding="utf-8"):
            r_ = json.loads(line)
            prev[r_["sku"]] = r_
    diffs = Counter()
    records, issues = [], []
    sheets = {n: [] for n in ("Products", "Content", "Pricing", "SEO", "Attributes", "Compatibility", "Claims",
                              "Warnings", "Images", "Versions", "Audit", "Handoff")}
    glob = {}
    for key in ("pro", "airpods4"):
        rows = load_series(key)
        # variations are not used (user decision 2026-10-07): every SKU is a standalone listing, titles must stay unique
        titles = {}
        glob[key] = {"variation": "NOT_USED", "compatibility": SERIES[key]["compat_models"], "facts": FACTS,
                     "pricing": price, "quantity": QUANTITY, "shipping_template": SHIPPING_TEMPLATE, "children": len(rows)}
        for row in rows:
            q = row["sku"][-4:]
            content = build_content(key, row)
            errs, warns = validate(key, row, content)
            t = content["title"].lower()
            if t in titles:
                errs.append(f"title duplicates {titles[t]} inside parent")
            titles[t] = row["sku"]
            attrs = attributes(key, row, content, price)
            ev = evidence(key, row, content)
            unresolved = sorted({a["attribute"] for a in attrs if a["status"] == "DATA_REQUIRED" and a["required"] == "Required"}
                                | set(price["missing"]))
            price_attrs = ("your_price_usd_standard_price", "sale_start_date", "sale_end_date")
            cond_open = sorted(a["attribute"] for a in attrs if a["status"] == "DATA_REQUIRED" and a["required"] != "Required"
                               and a["attribute"] not in price_attrs)
            hard = [f"VALIDATOR: {e}" for e in errs]
            hard += [("PRICE_DATA_REQUIRED: " if u.startswith(("standard_price", "sale")) else "REQUIRED_ATTRIBUTE_MISSING: ") + u for u in unresolved]
            for m_ in price.get("policy_conflicts", []):
                hard.append("PRICE_POLICY_CONFLICT: " + m_)
            if price["status"] == "PRICE_CONFLICT" and price["standard_price"] is not None and price["sale_price"] is not None \
                    and price["standard_price"] <= price["sale_price"]:
                hard.append("PRICE_CONFLICT: standard price is not above the sale price")
            warnings = [f"VALIDATOR: {w}" for w in warns]
            warnings += ["CONDITIONAL_ATTRIBUTE_NOT_DETERMINED: " + c for c in cond_open]
            if not THEME[q]:
                warnings.append("THEME_REVIEW: no clear valid value for this print")
            if q not in VERIFIED_IMAGE_MATCH:
                warnings.append("IMAGE_SKU_MATCH_MEDIUM: thumbnail viewed, not itemized")
            if price.get("quantity_tiers_status") == "RATES_NOT_APPROVED":
                warnings.append("QUANTITY_TIERS_PENDING: thresholds " + ", ".join(str(x) for x in price["quantity_tier_thresholds"]) + " units given; discount rates need an approved tier policy")
            if q == "q230":
                warnings.append("POLICY_RISK_REVIEW: print resembles a known character; rights decision with the user")
            if errs:
                status = "BLOCKED"
            elif price["status"] == "PRICE_CONFLICT":
                status = "PRICE_CONFLICT"
            elif price["status"] == "PRICE_POLICY_CONFLICT":
                status = "NEEDS_REVIEW"
            elif unresolved:
                status = "DATA_REQUIRED"
            else:
                status = "READY_WITH_WARNINGS"
            pricing = dict(price)
            catalog = {a["attribute"]: {"value": a["value"], "status": a["status"], "source": a["source"], "confidence": a["confidence"]}
                       for a in attrs if a["attribute"] not in ("item_name", "product_description", "bullet_points", "generic_keyword", "title_differentiation")}
            source_in = {"sku": row["sku"], "color": row["color"], "series": key, "facts": FACTS}
            rec = {
                "handoff_schema_version": SCHEMA_VERSION, "batch_id": BATCH_ID, "generated_at": GENERATED_AT,
                "generated_by_agent_version": AGENT_VERSION, "internal_product_id": "MOBILIUS-" + row["sku"],
                "sku": row["sku"], "marketplace": MARKETPLACE, "language": LANGUAGE, "record_version": RECORD_VERSION,
                "operation_intent": "CREATE", "publish_status": status, "identifier_mode": "GTIN_EXEMPT",
                "identifiers": {"ean": None, "upc": None, "gtin": None, "asin": None, "gtin_exempt": True, "status": "GTIN_EXEMPT"},
                "product_type": {"value": "PORTABLE_ELECTRONIC_DEVICE_COVER", "status": "CATEGORY_CONFIRMED", "confidence": "HIGH",
                                 "browse_node": "headphone-cases", "locked": True},
                "variation": {"status": "NOT_USED", "reason": "user decision 2026-10-07: variations are not needed yet",
                              "parent_sku": None, "theme": None, "color": row["color"]},
                "catalog": catalog,
                "content": {"title": content["title"], "item_highlights": content["item_highlights"],
                            "bullet_points": content["bullet_points"], "description": content["description"],
                            "backend_search_terms": content["backend_search_terms"], "backend_bytes": content["backend_bytes"]},
                "pricing": pricing,
                "compatibility": {"compatible_brand": "Apple", "compatible_model": SERIES[key]["compat_models"],
                                  "compatible_generation": SERIES[key]["compat_generations"], "compatible_year": None,
                                  "compatible_device": "Headphones", "not_compatible_with": None,
                                  "status": "COMPATIBILITY_VERIFIED", "source": "USER_INPUT"},
                "claims": [c for c in GLOBAL_CLAIMS if c[0] in ("ALL", key, q)],
                "evidence": ev,
                "changed_fields": [],
                "unresolved_required_fields": unresolved, "hard_blockers": hard, "warnings": warnings,
                "versions": VERSIONS,
                "audit": {"generated_from": [SERIES[key]["file"], "SEO-Rules.md v1.1", "Feed AirPods Cases.xlsm"],
                          "source_types": ["USER_INPUT", "TTX", "CATALOG", "SEO", "CALCULATED"]},
            }
            old = prev.get(row["sku"])
            if old:
                def flat(r_):
                    d = {"content." + k: v for k, v in r_["content"].items()}
                    d.update({"pricing." + k: v for k, v in r_["pricing"].items() if k != "missing"})
                    d.update({"catalog." + k: (v["value"], v["status"]) if isinstance(v, dict) else v for k, v in r_["catalog"].items()})
                    d["variation.status"] = r_["variation"].get("status")
                    d["publish_status"] = r_["publish_status"]
                    return d
                fo, fn = flat(old), flat(rec)
                for k in sorted(set(fo) | set(fn)):
                    if fo.get(k) != fn.get(k):
                        diffs[(k, json.dumps(fo.get(k), ensure_ascii=False)[:90], json.dumps(fn.get(k), ensure_ascii=False)[:90])] += 1
                rec["changed_fields"] = sorted(k for k in set(fo) | set(fn) if fo.get(k) != fn.get(k))
            rec["hashes"] = {"source_hash": sha(source_in), "content_hash": sha(rec["content"]), "pricing_hash": sha(pricing)}
            rec["hashes"]["catalog_hash"] = sha(rec["catalog"])
            rec["hashes"]["record_hash"] = sha({k: v for k, v in rec.items() if k != "hashes"})
            rec["idempotency_key"] = sha([rec["internal_product_id"], MARKETPLACE, "CREATE", rec["hashes"]["content_hash"],
                                          rec["hashes"]["pricing_hash"], rec["hashes"]["catalog_hash"]])[:32]
            rec["rollback"] = ({"previous_record_version": old["record_version"], "previous_content_hash": old["hashes"]["content_hash"],
                                "previous_pricing_hash": old["hashes"]["pricing_hash"]} if old else
                               {"previous_record_version": None, "previous_content_hash": None, "previous_pricing_hash": None})
            records.append(rec)
            for h in hard:
                issues.append((row["sku"], "HARD_BLOCKER", h))
            for w in warnings:
                issues.append((row["sku"], "WARNING", w))
            # sheets
            sheets["Products"].append([rec["internal_product_id"], row["sku"], None, None, None, True, None, "MOBILIUS",
                                       content["title"], row["model"], "PORTABLE_ELECTRONIC_DEVICE_COVER", MARKETPLACE, "China", status])
            sheets["Content"].append([row["sku"], MARKETPLACE, LANGUAGE, content["title"], content["item_highlights"], *content["bullet_points"],
                                      content["description"], content["backend_search_terms"], content["backend_bytes"]])
            if price.get("quantity_tiers"):
                tier_cells = [f"{t['lower_bound']}+ units: " + (f"fixed {t['fixed_price']}" + (f" ({t['discount_pct_of_business_price']}% off business price)" if "discount_pct_of_business_price" in t else "")
                                                               if "fixed_price" in t else f"{t['discount_pct']}% off = {t['resulting_unit_price']}")
                              for t in price["quantity_tiers"]][:4]
            else:
                tier_cells = [f"{x}+ units: rate not approved" for x in price.get("quantity_tier_thresholds", [])][:4]
            tier_cells += [None] * (4 - len(tier_cells))
            sheets["Pricing"].append([row["sku"], MARKETPLACE, CURRENCY, price["sale_price"], price["standard_price"], price["list_price"],
                                      price["map_price"], price["minimum_seller_allowed_price"], price["maximum_seller_allowed_price"],
                                      price["business_price"]] + tier_cells + [price["pricing_policy_version"], price["status"]])
            for a in attrs:
                sheets["Attributes"].append([row["sku"], a["attribute"], a["value"], a["source"], a["confidence"], a["required"], a["status"], a["note"]])
                sheets["Audit"].append([row["sku"], a["attribute"], a["value"], a["source"], VERSIONS["product_data_version"], a["confidence"], a["status"], GENERATED_AT])
            sheets["Compatibility"].append([row["sku"], "Apple", "; ".join(SERIES[key]["compat_models"]), "; ".join(SERIES[key]["compat_generations"]),
                                            None, "Headphones", None, "USER_INPUT", "HIGH"])
            for c in GLOBAL_CLAIMS:
                if c[0] in ("ALL", key, q):
                    sheets["Claims"].append([row["sku"], c[1], c[2], c[3], c[4], c[5], c[6], c[7]])
            for typ, sev, msg in [("HARD_BLOCKER", "HIGH", h) for h in hard] + [("WARNING", "LOW", w) for w in warnings]:
                sheets["Warnings"].append([row["sku"], typ, sev, "", msg, ""])
            for i, url in enumerate(row["photos"], 1):
                fixed = (key == "pro" and i == 5)
                sheets["Images"].append([row["sku"], f"Photo {i}", "MAIN" if i == 1 else "OTHER", row["sku"],
                                         "HIGH" if q in VERIFIED_IMAGE_MATCH else "MEDIUM",
                                         "captions front/back corrected locally: upload fixed_images/pro_photo5/" + row["sku"] + "_5.jpg" if fixed else "",
                                         "Required" if i == 1 else "Optional", "IMAGE_SUFFICIENT", url])
            sheets["Versions"].append([row["sku"], MARKETPLACE, RECORD_VERSION, VERSIONS["seo_version"], VERSIONS["product_data_version"],
                                       price["pricing_policy_version"], VERSIONS["amazon_policy_version"], rec["hashes"]["source_hash"], rec["hashes"]["content_hash"], GENERATED_AT])
            sheets["Handoff"].append([SCHEMA_VERSION, BATCH_ID, rec["internal_product_id"], row["sku"], MARKETPLACE, RECORD_VERSION, "CREATE", status,
                                      "GTIN_EXEMPT", "PORTABLE_ELECTRONIC_DEVICE_COVER", "LOCKED", ", ".join(rec["changed_fields"]),
                                      ", ".join(unresolved), " | ".join(hard), " | ".join(warnings), rec["hashes"]["source_hash"],
                                      rec["hashes"]["content_hash"], rec["hashes"]["pricing_hash"], rec["hashes"]["record_hash"],
                                      rec["idempotency_key"], GENERATED_AT, AGENT_VERSION])
    for k, ser, sv, ks, tier, place, st, reason in KEYWORDS:
        sheets["SEO"].append(["ALL_" + ser.upper(), MARKETPLACE, k, sv, tier, place, st, reason, "2026-09-26 / 2026-10-07"])

    with open(os.path.join(out_dirs["jsonl"], "handoff_US_batch001.jsonl"), "w", encoding="utf-8") as f:
        for r in records:
            f.write(json.dumps(r, ensure_ascii=False, sort_keys=True) + "\n")
    if diffs:
        with open(os.path.join(out_dirs["issues"], f"diff_batch001_v{PREVIOUS_RECORD_VERSION}_to_v{RECORD_VERSION}.csv"), "w", newline="", encoding="utf-8") as f:
            w = csv.writer(f)
            w.writerow(["field", "old", "new", "records_changed"])
            for (k, o, n), c in sorted(diffs.items()):
                w.writerow([k, o, n, c])
    json.dump(glob, open(os.path.join(out_dirs["json"], "global_product_data_US.json"), "w", encoding="utf-8"), indent=2, ensure_ascii=False)
    with open(os.path.join(out_dirs["issues"], "issues_US_batch001.csv"), "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["sku", "severity", "issue"])
        w.writerows(issues)

    heads = {
        "Products": ["Internal Product ID", "SKU", "EAN", "UPC", "GTIN", "GTIN Exempt", "ASIN", "Brand", "Product Name", "Model", "Product Type", "Marketplace", "Country of Origin", "Publish Status"],
        "Content": ["SKU", "Marketplace", "Language", "Title", "Item Highlights", "Bullet 1", "Bullet 2", "Bullet 3", "Bullet 4", "Bullet 5", "Description", "Backend Search Terms", "Backend Bytes"],
        "Pricing": ["SKU", "Marketplace", "Currency", "Sale Price", "Standard Price", "List Price", "MAP", "Min Seller Allowed Price", "Max Seller Allowed Price", "Business Price", "Quantity Tier 1", "Quantity Tier 2", "Quantity Tier 3", "Quantity Tier 4", "Pricing Policy Version", "Status"],
        "SEO": ["Group", "Marketplace", "Keyword", "Search Volume", "Tier", "Placement", "Status", "Reason", "SEO Source Date"],
        "Attributes": ["SKU", "Attribute", "Value", "Source", "Confidence", "Required", "Status", "Note"],
        "Compatibility": ["SKU", "Compatible Brand", "Compatible Model", "Generation", "Year", "Device", "Not Compatible With", "Source", "Confidence"],
        "Claims": ["SKU", "Claim", "Source", "Evidence", "Claim Type", "Risk", "Status", "Action"],
        "Warnings": ["SKU", "Issue Type", "Severity", "Field", "Issue", "Recommended Action"],
        "Images": ["SKU", "Image", "Image Type", "Matched Product", "Match Confidence", "Evidence Extracted", "Required / Optional", "Status", "URL"],
        "Versions": ["SKU", "Marketplace", "Listing Version", "SEO Version", "Product Data Version", "Pricing Policy Version", "Amazon Policy Version", "Source Hash", "Content Hash", "Last Updated"],
        "Audit": ["SKU", "Field", "Value", "Source", "Source Version", "Confidence", "Status", "Last Updated"],
        "Handoff": ["Handoff Schema Version", "Batch ID", "Internal Product ID", "SKU", "Marketplace", "Record Version", "Operation Intent", "Publish Status", "Identifier Mode", "Product Type", "Product Type Status", "Changed Fields", "Unresolved Required Fields", "Hard Blockers", "Warnings", "Source Hash", "Content Hash", "Pricing Hash", "Record Hash", "Idempotency Key", "Generated At", "Generated By Agent Version"],
    }
    wb = openpyxl.Workbook()
    wb.remove(wb.active)
    from openpyxl.styles import Font, PatternFill, Alignment
    for name in heads:
        ws = wb.create_sheet(name)
        ws.append(heads[name])
        for r in sheets[name]:
            ws.append([("" if v is None else v) for v in r])
        for c in ws[1]:
            c.font = Font(bold=True, color="FFFFFF")
            c.fill = PatternFill("solid", fgColor="1F3A5F")
            c.alignment = Alignment(wrap_text=True, vertical="top")
        ws.freeze_panes = "A2"
        for i, h in enumerate(heads[name], 1):
            width = 14
            if h in ("Title", "Item Highlights", "Description", "Value", "Issue", "Claim", "Warnings", "Hard Blockers", "Bullet 1", "Bullet 2", "Bullet 3", "Bullet 4", "Bullet 5", "URL"):
                width = 48
            ws.column_dimensions[openpyxl.utils.get_column_letter(i)].width = width
    xlsx = os.path.join(out_dirs["xlsx"], "AirPods_US_Agent1_Review_batch001.xlsx")
    wb.save(xlsx)

    tiers = Counter(k[4] for k in KEYWORDS)
    sr = ["# SEO sanitization report, US, batch " + BATCH_ID, "",
          "Source: AirPods_US_SEO.xlsx (Helium 10 Magnet / Cerebro / Niche, snapshot 2026-09-26) plus Helium 10 MCP additions of 2026-10-07.",
          "Marketplace check: US data for the US marketplace (SEO_MARKETPLACE_MISMATCH: none).", "",
          "| Item | Count |", "|---|---|",
          "| Magnet rows (3 seed queries) | 23,817 |", "| Cerebro rows (20 competitor ASINs) | 37,489 |",
          "| Unique phrases after de-duplication | 20,636 |",
          "| Phrases with SV >= 500 in the case topic that were excluded | 291 |",
          "| Selected in the SEO file (SV >= 500, KS >= 100, organic confirmed) | 20 |",
          f"| Phrase groups in this batch's keyword table | {len(KEYWORDS)} |",
          f"| TIER_1_PRIMARY | {tiers.get('TIER_1_PRIMARY', 0)} |", f"| TIER_2_SECONDARY | {tiers.get('TIER_2_SECONDARY', 0)} |",
          f"| TIER_3_LONG_TAIL | {tiers.get('TIER_3_LONG_TAIL', 0)} |", f"| TIER_4_SEMANTIC | {tiers.get('TIER_4_SEMANTIC', 0)} |",
          f"| EXCLUDE | {tiers.get('EXCLUDE', 0)} |", "",
          "Excluded 291 phrases by reason (from the file): Keyword Sales < 100 per week only 137; color, extra property or audience plus low KS 108; "
          "charging case, replacement or ambiguous intent plus color plus low KS 24; charging case, replacement or ambiguous plus low KS 13; "
          "ambiguous model 'Pro 4' plus low KS 5; other 4.", "",
          "Competitor brand terms: none used. Forbidden terms: 'pro 3' (not compatible), '1/2' (AirPods 1 and 2), claim words (see SEO-Rules.md section 4.1).",
          "Semantic duplicate clusters used as backend spelling variants: airpod / airpods, air pod / air pods, airpodpro / podspro / procase / podspro2, pods4.",
          "", "Keyword Sales is the weekly sales for the last complete week 2026-09-13 to 2026-09-19 (see SEO-Rules.md section 1).",
          "New phrases for AirPods 5 and keychain were added on 2026-10-07 from Helium 10 MCP; the SEO file of 2026-09-26 has no AirPods 5 phrases."]
    open(os.path.join(out_dirs["issues"], "seo_sanitization_report.md"), "w", encoding="utf-8").write("\n".join(sr) + "\n")

    status_counts = Counter(r["publish_status"] for r in records)
    hb = Counter(i[2].split(":")[0] + ":" + i[2].split(":")[1].split("(")[0].strip()[:40] for i in issues if i[1] == "HARD_BLOCKER")
    summary = [f"# Batch summary {BATCH_ID}", "", f"Total SKUs: {len(records)} (65 Pro, 65 AirPods 4/5), marketplace {MARKETPLACE}", ""]
    for s_ in ("READY_TO_PUBLISH", "READY_WITH_WARNINGS", "NEEDS_REVIEW", "DATA_REQUIRED", "BLOCKED", "POLICY_RISK", "PRICE_CONFLICT"):
        summary.append(f"- {s_}: {status_counts.get(s_, 0)}")
    summary += ["", f"Pricing: input Sale Price {price['input_value']} {CURRENCY}; mode {args.pricing_mode}; price status {price['status']}"
                + (f"; missing: {', '.join(price['missing'])}" if price["missing"] else ""),
                "Quantity 1, shipping template 'Migrated Template', Dangerous Goods Regulations 'Not Applicable' (user, 2026-10-07).",
                "Variations: not used (user decision); every SKU is a standalone listing.",
                "Note: 65 standalone listings per series share the same keyword set and compete for the same phrases (cannibalization).",
                "", "Hard blockers (count of records):"] + [f"- {k}: {v}" for k, v in sorted(hb.items())]
    open(os.path.join(out_dirs["issues"], "batch_summary.md"), "w", encoding="utf-8").write("\n".join(summary) + "\n")
    print("\n".join(summary))
    print("xlsx:", xlsx)
    return records


if __name__ == "__main__":
    main()
