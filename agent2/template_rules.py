"""Evaluator of the Amazon template's own requirement rules (Agent 2).

The template stores its "required" logic as Excel formulas on defined names, used by the conditional
formatting of the Template sheet (the red highlight). This module reads those names and evaluates them
for one row of values, so Agent 2 knows which cells the template itself considers required.
Only read access to the workbook XML is needed. Supported functions: AND, OR, NOT, IF, COUNTIF, LEN.
"""
import html
import re
import zipfile

FUNCS = {"AND", "OR", "NOT", "IF", "COUNTIF", "LEN", "TRUE", "FALSE"}


class TemplateRules:
    def __init__(self, xlsm_path, template_sheet_part="xl/worksheets/sheet5.xml", lists_sheet_part="xl/worksheets/sheet7.xml"):
        z = zipfile.ZipFile(xlsm_path)
        wb = z.read("xl/workbook.xml").decode("utf8")
        self.names = {n: html.unescape(v) for n, v in re.findall(r'<definedName name="([^"]*)"[^>]*>([^<]*)</definedName>', wb)}
        sheet = z.read(template_sheet_part).decode("utf8")
        # per-column ordered rules from the conditional formatting (Excel evaluates them top to bottom, stopIfTrue)
        self.rules = {}
        for sq, body in re.findall(r'<conditionalFormatting sqref="([^"]*)">(.*?)</conditionalFormatting>', sheet, re.S):
            for part in sq.split():
                m = re.fullmatch(r"(?P<c>[A-Z]{1,3})7:(?P=c)1048576", part)
                if not m:
                    continue
                col = m.group("c")
                lst = []
                for prio, f in re.findall(r'<cfRule type="expression" dxfId="\d+" priority="(\d+)"[^>]*>\s*<formula>(.*?)</formula>', body, re.S):
                    f = html.unescape(f)
                    if re.fullmatch(r"IF\(LEN\([A-Z]+7\)>0,1,0\)", f):
                        lst.append((int(prio), "FILLED", None))
                        continue
                    mm = re.fullmatch(r"IF\(PTList0,((form_rg|only_enf|req_tog|req|for_maxf|for_min)[A-Za-z0-9_.]*),0\)", f)
                    if mm:
                        kind = {"form_rg": "DISABLED", "only_enf": "ONLY_ENFORCED", "req_tog": "RECOMMENDED", "req": "REQUIRED", "for_min": "REQUIRED", "for_maxf": "TOO_MANY"}[mm.group(2)]
                        lst.append((int(prio), kind, mm.group(1)))
                self.rules[col] = [(k, n) for _, k, n in sorted(lst)]
        self.req_name = {c: [n for k, n in r if k == "REQUIRED"][0] for c, r in self.rules.items() if any(k == "REQUIRED" for k, n in r)}
        # condition lists: values of the hidden 'Conditions List' sheet
        shared = []
        ss = z.read("xl/sharedStrings.xml").decode("utf8")
        for si in re.findall(r"<si>(.*?)</si>", ss, re.S):
            shared.append(html.unescape("".join(re.findall(r"<t[^>]*>(.*?)</t>", si, re.S))))
        lst = z.read(lists_sheet_part).decode("utf8")
        cells = {}
        for ref, t, v in re.findall(r'<c r="([A-Z]+[0-9]+)"[^>]*?(?: t="([a-z]+)")?[^>]*>(?:<v>(.*?)</v>)?', lst):
            if v == "":
                continue
            cells[ref] = shared[int(v)] if t == "s" else html.unescape(v)
        self.cells = cells
        self._cache = {}

    # ---- condition lists
    def list_values(self, list_name):
        ref = self.names[list_name]  # 'Conditions List'!$B$2:$B$3
        m = re.fullmatch(r"'Conditions List'!\$([A-Z]+)\$(\d+)(?::\$([A-Z]+)\$(\d+))?", ref)
        c1, r1, c2, r2 = m.group(1), int(m.group(2)), m.group(3) or m.group(1), int(m.group(4) or m.group(2))
        assert c1 == c2
        return [self.cells.get(f"{c1}{r}") for r in range(r1, r2 + 1)]

    # ---- formula translation
    def _translate(self, f):
        f = f.replace("Template!", "")
        f = re.sub(r"\$([A-Z]{1,3})1\b", lambda m: f"CELL('{m.group(1)}')", f)
        f = f.replace("<>", " != ")
        f = re.sub(r"(?<![<>!=])=(?!=)", " == ", f)
        f = re.sub(r"\bTRUE\b", "True", f)
        f = re.sub(r"\bFALSE\b", "False", f)

        def repl_name(m):
            tok = m.group(0)
            if tok in FUNCS or tok in ("True", "False", "CELL") or tok.startswith("CONDITION_LIST_"):
                return tok
            if tok in self.names:
                return f"NAME('{tok}')"
            return tok
        out, i = [], 0
        # leave string literals untouched
        for part in re.split(r'("[^"]*")', f):
            if part.startswith('"'):
                out.append(part)
            else:
                out.append(re.sub(r"[A-Za-z_][A-Za-z0-9_.]*(?![A-Za-z0-9_.(])|[A-Za-z_][A-Za-z0-9_.]*(?=\()", repl_name, part))
        f = "".join(out)
        f = re.sub(r"COUNTIF\((CONDITION_LIST_\d+),", r"COUNTIF('\1',", f)
        return f

    def evaluate(self, name, row):
        """row: dict column letter -> value (str / number / None). Returns bool."""
        key = None

        def CELL(col):
            v = row.get(col)
            return "" if v is None else v

        memo = {}

        def NAME(n):
            if n in memo:
                return memo[n]
            expr = self._translate(self.names[n])
            val = eval(expr, {"__builtins__": {}}, env)
            memo[n] = val
            return val

        def COUNTIF(list_name, x):
            vals = self.list_values(list_name)
            return sum(1 for v in vals if v is not None and str(v) == str(x))

        env = {
            "AND": lambda *a: all(a), "OR": lambda *a: any(a), "NOT": lambda a: not a,
            "IF": lambda c, a, b: a if c else b, "LEN": lambda x: len(str(x)),
            "CELL": CELL, "NAME": NAME, "COUNTIF": COUNTIF,
        }
        return bool(NAME(name))

    def status(self, col, row):
        """Template status of one cell for this row: DISABLED, FILLED, ONLY_ENFORCED, REQUIRED, TOO_MANY or OPEN."""
        for kind, name in self.rules.get(col, []):
            if kind == "FILLED":
                v = row.get(col)
                if v is not None and str(v) != "":
                    return "FILLED"
                continue
            if self.evaluate(name, row):
                return kind
        return "OPEN"

    def required_columns(self, row):
        """Columns that the template shows as required and still empty for this row."""
        return sorted(c for c in self.rules if self.status(c, row) == "REQUIRED")

    def disabled_columns(self, row):
        return sorted(c for c in self.rules if self.status(c, row) == "DISABLED")
