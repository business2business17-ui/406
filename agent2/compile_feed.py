"""Agent 2 compiler: writes Agent 1 handoff rows into a copy of the Amazon template by direct XML injection into the
Template sheet (every other zip part stays byte-identical). Rows 1-6 are never touched."""
import collections, hashlib, json, os, re, sys, zipfile
from decimal import Decimal
from xml.sax.saxutils import escape
import openpyxl
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import feed_mapping as fm
from template_rules import TemplateRules

ROOT = os.path.dirname(fm.HERE)
TPL = os.path.join(fm.HERE, "templates", "raw", "PORTABLE_ELECTRONIC_DEVICE_COVER_2026-10-08.xlsm")  # template uploaded by the user 2026-10-08
BATCH = "US-AIRPODS-20261007-001"
OUT = os.path.join(fm.HERE, "feeds", "generated")
NUMERIC = {"EX", "EY", "AV", "DN", "DS", "ER", "EV", "EZ", "FE", "FK", "FL", "FM", "FN", "FV", "FX", "FZ", "GB", "GD", "GF", "GH"}
SKIP_ENUM = {"C", "EV", "FE", "EX", "EY", "FF", "FG"}  # C: record_action list checked separately; EV/FE dropdown only holds the delete marker


def colnum(c):
    n = 0
    for ch in c: n = n * 26 + ord(ch) - 64
    return n


def load_photos():
    ws = openpyxl.load_workbook(os.path.join(ROOT, "output/xlsx/AirPods_US_Agent1_Review_batch001.xlsx"), read_only=True)["Images"]
    d = collections.defaultdict(list)
    for r in list(ws.iter_rows(values_only=True))[1:]:
        if r[8] and r[7] == "IMAGE_SUFFICIENT": d[r[0]].append((r[1], r[8]))
    return {k: [u for _, u in sorted(v, key=lambda x: int(x[0].split()[-1]))] for k, v in d.items()}


def cell_xml(col, row, val):
    ref = f"{col}{row}"
    if col in NUMERIC:
        return f'<c r="{ref}"><v>{Decimal(str(val)).normalize():f}</v></c>'
    s = str(val)
    if s[:1] in "=+-@": raise ValueError(f"formula-injection risk {ref}: {s[:20]}")
    return f'<c r="{ref}" t="inlineStr"><is><t xml:space="preserve">{escape(s)}</t></is></c>'


def main():
    cols = fm.load_columns(); cmap = {c["col"]: c for c in cols}
    dl = fm.DropdownLists(TPL, cols); tr = TemplateRules(TPL)
    recs = [json.loads(l) for l in open(os.path.join(ROOT, "output/jsonl/handoff_US_batch001.jsonl"), encoding="utf-8")]
    photos = load_photos()
    rows, prov, issues, mut = [], [], [], []
    for i, rec in enumerate(recs):
        r = 7 + i
        ph = photos.get(rec["sku"], [])
        if rec["sku"].startswith("406516"):  # user decision 2026-10-08: Pro series Photo 5 is not used
            ph = [u for u in ph if not u.endswith("_5.jpg")]
        rec["photos"] = ph
        v, pv = fm.build_row(rec)
        # Item Type Keyword: the exact string offered by THIS template's dropdown (it differs between template versions)
        itk = dl.by_col.get("L") or []
        assert len(itk) == 1 and "headphone-cases" in itk[0], itk
        v["L"] = itk[0]; pv["L"] = ("catalog.item_type_keyword.value", "ENUM_MAPPED")
        for col, val in v.items():
            if col not in SKIP_ENUM and dl.by_col.get(col) is not None and str(val) not in [str(x) for x in dl.by_col[col]]:
                issues.append({"sku": rec["sku"], "row": r, "col": col, "code": "ENUM_INVALID", "value": str(val)})
            if col == "C" and val not in dl.record_action:
                issues.append({"sku": rec["sku"], "row": r, "col": col, "code": "ENUM_INVALID", "value": val})
        for c in tr.required_columns(v):
            issues.append({"sku": rec["sku"], "row": r, "col": c, "key": cmap[c]["key"], "label": cmap[c]["label"], "code": "MISSING_REQUIRED_ATTRIBUTE_USER_DECISION"})
        for col, val in v.items():
            path, t = pv[col]
            prov.append({"sku": rec["sku"], "sheet": "Template", "cell": f"{col}{r}", "key": cmap[col]["key"], "source": path, "value": val, "transformation": t})
            if t != "DIRECT": mut.append({"cell": f"{col}{r}", "transformation": t, "meaning_changed": "NO"})
        rows.append((r, v))
    xml_rows = "".join(f'<row r="{r}" spans="1:316">' + "".join(cell_xml(c, r, v[c]) for c in sorted(v, key=colnum)) + "</row>" for r, v in rows)
    z = zipfile.ZipFile(TPL)
    sheet = z.read("xl/worksheets/sheet5.xml").decode("utf8")
    assert "</sheetData>" in sheet and '<row r="7"' not in sheet
    sheet = sheet.replace("</sheetData>", xml_rows + "</sheetData>", 1)
    sheet = re.sub(r'<dimension ref="A1:LD6"/>', f'<dimension ref="A1:LD{6 + len(rows)}"/>', sheet, 1)
    os.makedirs(OUT, exist_ok=True)
    name = f"AmazonFeed_US_PORTABLE_ELECTRONIC_DEVICE_COVER_{BATCH}_002.xlsm"
    path = os.path.join(OUT, name)
    with zipfile.ZipFile(path, "w") as zo:
        for info in z.infolist():
            data = z.read(info.filename)
            if info.filename == "xl/worksheets/sheet5.xml": data = sheet.encode("utf8")
            zi = zipfile.ZipInfo(info.filename, info.date_time); zi.compress_type = info.compress_type; zi.external_attr = info.external_attr
            zo.writestr(zi, data)
    json.dump({"file": name, "rows": len(rows), "issues": issues, "provenance": prov, "mutations": mut, "template_sha256": hashlib.sha256(open(TPL, "rb").read()).hexdigest(),
               "feed_sha256": hashlib.sha256(open(path, "rb").read()).hexdigest()}, open(os.path.join(OUT, "compile_result.json"), "w"), ensure_ascii=False)
    print(name, len(rows), "rows;", len(prov), "cells;", collections.Counter(i["code"] + ":" + i.get("col", "") for i in issues))


if __name__ == "__main__":
    main()
