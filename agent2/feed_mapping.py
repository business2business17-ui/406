"""Agent 2: mapping of an Agent 1 handoff record to Amazon template columns (US, PORTABLE_ELECTRONIC_DEVICE_COVER).

Every mapping goes through the template's machine key (row 5), never through header similarity.
Values are the exact accepted strings of the template's dropdown lists.
"""
import html
import json
import os
import re
import zipfile

HERE = os.path.dirname(os.path.abspath(__file__))
PT = "PORTABLE_ELECTRONIC_DEVICE_COVER"


def clean_key(key):
    return re.sub(r"[\[\]=#]", "", key)


class DropdownLists:
    """Valid values per template column, resolved the way the template does it (INDIRECT on defined names)."""

    def __init__(self, xlsm_path, columns):
        z = zipfile.ZipFile(xlsm_path)
        wb = html.unescape(z.read("xl/workbook.xml").decode("utf8"))
        names = dict(re.findall(r'<definedName name="([^"]*)"[^>]*>([^<]*)</definedName>', wb))
        ss = z.read("xl/sharedStrings.xml").decode("utf8")
        shared = ["".join(re.findall(r"<t[^>]*>(.*?)</t>", si, re.S)) for si in re.findall(r"<si>(.*?)</si>", ss, re.S)]
        shared = [html.unescape(s) for s in shared]
        sheet = z.read("xl/worksheets/sheet9.xml").decode("utf8")
        cells = {}
        for m in re.finditer(r'<c r="([A-Z]+)(\d+)"([^>]*?)(?:/>|>(.*?)</c>)', sheet, re.S):
            col, row, attrs, inner = m.group(1), int(m.group(2)), m.group(3), m.group(4) or ""
            v = re.search(r"<v>(.*?)</v>", inner, re.S)
            if not v:
                continue
            t = re.search(r't="([a-z]+)"', attrs)
            cells[(col, row)] = shared[int(v.group(1))] if (t and t.group(1) == "s") else html.unescape(v.group(1))
        self.cells, self.names, self.by_col = cells, names, {}
        for c in columns:
            nm = PT + clean_key(c["key"])
            if nm in names:
                self.by_col[c["col"]] = self._range(names[nm])
        self.record_action = self._range(names["record_action"]) if "record_action" in names else None

    def _range(self, ref):
        ref = html.unescape(ref)
        m = re.fullmatch(r"'Dropdown Lists'!\$([A-Z]+)\$(\d+)(?::\$([A-Z]+)\$(\d+))?", ref)
        c, r1 = m.group(1), int(m.group(2))
        r2 = int(m.group(4)) if m.group(4) else r1
        return [self.cells[(c, r)] for r in range(r1, r2 + 1) if (c, r) in self.cells]


def load_columns():
    return json.load(open(os.path.join(HERE, "mapping", "template_columns.json"), encoding="utf-8"))


# Agent 1 source path -> template column(s). Keys are the machine keys of row 5 (checked by the build).
def build_row(rec, series_theme=None):
    """Return (values: dict col->value, provenance: dict col->(agent1 path, transformation))."""
    c, cat, p = rec["content"], rec["catalog"], rec["pricing"]
    v, prov = {}, {}

    def put(col, value, path, tr="DIRECT"):
        if value is None or value == "":
            return
        v[col] = value
        prov[col] = (path, tr)

    put("A", rec["sku"], "sku")
    put("B", rec["product_type"]["value"], "product_type.value")
    put("C", {"CREATE": "Create or Replace (Full Update)"}[rec["operation_intent"]], "operation_intent", "OPERATION_MAPPED")
    put("G", c["title"], "content.title")
    put("H", c["item_highlights"], "content.item_highlights")
    put("I", cat["brand"]["value"], "catalog.brand.value")
    put("J", "GTIN Exempt" if rec["identifier_mode"] == "GTIN_EXEMPT" else None, "identifier_mode", "ENUM_MAPPED")
    put("L", "Cell Phones & Accessories > Accessories > Headphones, Earbuds & Accessories > Cases (headphone-cases)", "catalog.item_type_keyword.value", "ENUM_MAPPED")
    put("Q", cat["manufacturer"]["value"], "catalog.manufacturer.value")
    photos = rec.get("photos") or []
    for col, url in zip(["T", "U", "V", "W", "X", "Y"], photos):
        put(col, url, "photos", "DIRECT")
    put("AD", c["description"], "content.description")
    for col, b in zip(["AE", "AF", "AG", "AH", "AI"], c["bullet_points"]):
        put(col, b, "content.bullet_points")
    put("AJ", c["backend_search_terms"], "content.backend_search_terms")
    put("AQ", cat["material"]["value"], "catalog.material.value")
    put("AV", cat["number_of_items"]["value"], "catalog.number_of_items.value")
    put("AY", cat["color"]["value"], "catalog.color.value")
    theme = cat["theme"]["value"]
    put("BB", theme, "catalog.theme.value", "CLASSIFIED_FROM_PRINT_NAME")
    put("BG", cat["shell_type"]["value"], "catalog.shell_type.value")
    put("BL", cat["form_factor"]["value"], "catalog.form_factor.value")
    put("BP", cat["compatible_devices"]["value"], "catalog.compatible_devices.value")
    for col, m in zip(["CP", "CQ", "CR", "CS", "CT"], cat["compatible_headphone_models"]["value"].split("; ")):
        put(col, m, "catalog.compatible_headphone_models.value")
    put("DN", cat["item_weight_g"]["value"], "catalog.item_weight_g.value", "UNIT_PAIR")
    put("DO", "Grams", "catalog.item_weight_g.unit", "UNIT_PAIR")
    put("DQ", cat["item_condition"]["value"], "catalog.item_condition.value")
    put("DS", p["list_price"], "pricing.list_price", "TEMPLATE_RULE_ZERO_IF_UNKNOWN")
    put("EQ", cat["fulfillment_channel_code"]["value"], "catalog.fulfillment_channel_code.value")
    put("ER", cat["quantity"]["value"], "catalog.quantity.value")
    put("EV", p["standard_price"], "pricing.standard_price", "POLICY_2026-10-08-v2")
    put("EZ", p["sale_price"], "pricing.sale_price", "POLICY_2026-10-08-v2")
    put("FA", p["sale_start_date"], "pricing.sale_start_date")
    put("FB", p["sale_end_date"], "pricing.sale_end_date")
    put("FE", p["business_price"], "pricing.business_price", "POLICY_2026-10-08-v2")
    tiers = p.get("quantity_tiers") or []
    if tiers:
        put("FJ", p["quantity_price_type"], "pricing.quantity_price_type", "ENUM_MAPPED")
        for (cth, cpr), t in zip([("FK", "FL"), ("FM", "FN"), ("FO", "FP"), ("FQ", "FR"), ("FS", "FT")], tiers):
            put(cth, t["lower_bound"], "pricing.quantity_tiers.lower_bound")
            put(cpr, t["fixed_price"] if p["quantity_price_type"] == "Fixed" else t["discount_pct"], "pricing.quantity_tiers", "POLICY_2026-10-08-v2")
    put("FU", cat["shipping_template"]["value"], "catalog.shipping_template.value")
    put("FV", cat["item_length_mm"]["value"], "catalog.item_length_mm.value", "UNIT_PAIR")
    put("FW", "Millimeters", "catalog.item_length_mm.unit", "UNIT_PAIR")
    put("FX", cat["item_width_mm"]["value"], "catalog.item_width_mm.value", "UNIT_PAIR")
    put("FY", "Millimeters", "catalog.item_width_mm.unit", "UNIT_PAIR")
    put("FZ", cat["item_height_mm"]["value"], "catalog.item_height_mm.value", "UNIT_PAIR")
    put("GA", "Millimeters", "catalog.item_height_mm.unit", "UNIT_PAIR")
    put("GB", cat["item_package_length_mm"]["value"], "catalog.item_package_length_mm.value", "UNIT_PAIR")
    put("GC", "Millimeters", "catalog.item_package_length_mm.unit", "UNIT_PAIR")
    put("GD", cat["item_package_width_mm"]["value"], "catalog.item_package_width_mm.value", "UNIT_PAIR")
    put("GE", "Millimeters", "catalog.item_package_width_mm.unit", "UNIT_PAIR")
    put("GF", cat["item_package_height_mm"]["value"], "catalog.item_package_height_mm.value", "UNIT_PAIR")
    put("GG", "Millimeters", "catalog.item_package_height_mm.unit", "UNIT_PAIR")
    put("GH", cat["package_weight_g"]["value"], "catalog.package_weight_g.value", "UNIT_PAIR")
    put("GI", "Grams", "catalog.package_weight_g.unit", "UNIT_PAIR")
    put("GM", cat["country_of_origin"]["value"], "catalog.country_of_origin.value")
    put("HO", cat["dangerous_goods_regulations"]["value"], "catalog.dangerous_goods_regulations.value")
    return v, prov
