# Hermes Round 1 - Apply Tools Code Review

Branch:
- hermes/read-only-checks

Changed files:
- docs/drafts/hermes-code-review-apply-tools.md (this file)

---

## Checks Run

```
python tools/static_checks.py --write-report
python tools/validate_apply_csv.py --kind room --csv tests/fixtures/missing_room_numbers_valid.csv
python tools/validate_apply_csv.py --kind mark --csv tests/fixtures/missing_door_window_marks_valid.csv
python tools/validate_apply_csv.py --kind room --csv tests/fixtures/missing_room_numbers_duplicate.csv
python tools/validate_apply_csv.py --kind mark --csv tests/fixtures/missing_door_window_marks_duplicate.csv
```

Results: 0 errors, 11 warnings (all historical/Hermes-audit docs). 4/4 CSV fixtures as expected.

---

## Summary

Reviewed `ApplyMissingDoorWindowMarks.pushbutton/script.py` and `ApplyMissingRoomNumbers.pushbutton/script.py` against `docs/error-codes.md`, `docs/testing-and-qa.md`, and `docs/safety-rules.md`.

Both scripts follow an identical `dry-run CSV → validate → confirm → apply inside Transaction → log` flow. Seven error codes are symmetrically defined and enforced. All safety-rules.md requirements (transaction wrapping, human confirmation, logging) are met.

---

## Review Conclusions

### Issues Already Addressed by Codex

| Issue | Status |
|-------|--------|
| 11 shared functions duplicated across both scripts | ✅ Resolved — extracted to `pyrevit/YangAgent.extension/lib/yang_agent_apply.py` |
| `is_expected_csv_name` hardcoded per tool | ✅ Resolved — now accepts prefix parameter |
| `validate_fields` hardcoded field list | ✅ Resolved — now accepts REQUIRED_FIELDS parameter |
| `collect_apply_rows` embedded row filter | ✅ Resolved — now accepts `is_applicable_row` callback |
| `confirm_apply` directly accessed forms/TEXT | ✅ Resolved — now accepts parameters |
| `write_csv` BOM+DictWriter boilerplate | ✅ Resolved — replaced by `write_utf8_csv` from shared module |
| Dead code: `"bad_csv"` key in TEXT dict (Marks L51) | ✅ Resolved — Codex removed it (not repurposed). `bad_csv_fields` handles field validation. |

### Issues Still Open

| # | Finding | Location | Severity |
|---|---------|----------|----------|
| 1 | Marks' `wrong_csv_name` lacks duplicate-CSV guidance | Marks L50 | Low (Rooms L50 has equivalent: "如果你选择的是 duplicate_room_numbers_*.csv...") |
| 2 | `is_applicable_row` style inconsistency: Marks uses `category not in [...]`, Rooms uses `category != "Room"` | Marks L118 vs Rooms L115 | Low (functionally equivalent) |
| 3 | Markdown detail format asymmetry: Rooms outputs `room_name`, Marks does not output element name | Marks L229 vs Rooms L227 | Low |

### User-Misoperation Risks (All Defended)

| Risk | Defense |
|------|---------|
| Wrong CSV type | File name check (-001) |
| Corrupted CSV fields | Field validation (-002) |
| Invalid element_id | Parse check (-003) |
| Element deleted after dry-run | Element lookup (-004) |
| Missing parameter | Parameter search (-005) |
| Read-only parameter | IsReadOnly check (-006) |
| Duplicate rows | Duplicate check (-007) — blocked **before** confirm dialog |

### Questions That Require Live Revit

1. Does `Revit Undo` actually reverse a full Transaction batch in Revit 2027?
2. Does `param.Set()` on `ALL_MODEL_MARK` work for all Door/Window families?
3. Does `param.Set()` on `ROOM_NUMBER` work for all Room placements?
4. Does `forms.CommandSwitchWindow.show` render and return correctly?
5. Does `get_export_dir()` return a valid path after `导出路径` is set?
6. Does the "Existing mark/number is not blank" skip logic work correctly on elements that already have values?

### Flow Consistency

Both scripts execute this identical sequence: doc check → pick CSV → validate filename → validate fields → filter applicable rows → check duplicates → confirm (dialog with count) → apply (inside `revit.Transaction`) → write Markdown + CSV logs → alert with counts.

**Verdict: flow is fully consistent.** ✅

### Safety Compliance vs `docs/safety-rules.md`

| Rule | Status |
|------|--------|
| Default read-only (no CSV = no modify) | ✅ |
| Dry-run before apply (CSV must match preview button) | ✅ |
| High-risk confirmation (dialog with element count) | ✅ |
| Transaction wrapping (`[Agent] Apply ...`) | ✅ |
| Logging (Markdown + CSV dual output) | ✅ |

**Verdict: fully compliant.** ✅

---

## Safety Confirmation

- I did not edit pyRevit scripts.
- I did not edit C# files.
- I did not edit tools, tests, scripts, or addin templates.
- I did not run install/build scripts.
- I did not run Revit.
- I did not add .rvt or .rfa files.
- I did not run git merge / push / pull.
- My code conclusions are review findings only, not implementation decisions.

---

## Codex Decisions Recorded

| Decision | Date | Detail |
|----------|------|--------|
| Remove Marks L51 `"bad_csv"` dead code | 2026-06-11 | Not repurposed. `bad_csv_fields` is the single canonical path. Low-risk cleanup, no apply-semantic change. |
| Compact checklist → standalone file | 2026-06-11 | Created `docs/sandbox-pyrevit-mvp-checklist.md` as independent operator checklist. Appendix in runbook review retained as historical reference only. |
| 5 missing feedback fields → feedback template | 2026-06-11 | Codex landed them in `docs/sandbox-pyrevit-mvp-feedback-template.md`. Recorded here for cross-report traceability. |

---

## Questions for Codex

- Marks' `wrong_csv_name` (L50): add duplicate-CSV guidance to match Rooms? (still open)
- `is_applicable_row` style difference: normalize or leave as-is? (still open)
- Markdown detail format: add element name to Marks log to match Rooms? (still open)
