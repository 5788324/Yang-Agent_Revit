# Hermes Round 1 - Sandbox Runbook Feature Review

Branch:
- hermes/read-only-checks

Changed files:
- docs/drafts/hermes-feature-review-sandbox-runbook.md (this file)

---

## Checks Run

```
python tools/run_sandbox_preflight.py --write-report
```

Result: 7/7 PASS — compile offline tools, pyRevit extension layout, static checks, all 4 CSV fixture validations.

---

## Summary

Reviewed `docs/sandbox-pyrevit-mvp-runbook.md` against `docs/next-steps.md`, `docs/testing-and-qa.md`, `docs/troubleshooting.md`, and `docs/handoff-new-chat-2026-06-07.md`.

The runbook is structurally sound as live-Revit guidance. The 34-step validation sequence covers all 13 pyRevit buttons plus language switching and Undo testing. All four reference docs are consistently reflected. The "first blocker" rule is well-placed.

Improvements identified: 5 missing feedback fields, 3 steps easily skipped, apply/Undo steps insufficiently distinguished from read-only steps, and no compact operator checklist.

---

## Review Conclusions

### Steps Clear Enough for a Human Operator Now

- Offline preflight command (L25) — single command, clear expected output
- Install/refresh (L44-48) — standard Force-ClearCache pattern
- Read-only + preview buttons (steps 5–25) — consistent "run → confirm file" loop
- Language switch (steps 32–34) — clear sequence
- First blocker rule (L107-114) — unambiguous stop-and-report

### Steps Easy to Skip or Misread

| Step | Risk | Suggested Fix |
|------|------|---------------|
| L57 "Open a sandbox/test model" | Operator may use a real project | Add: "File name should contain `_sandbox` or `_test`" |
| L60 "Set or confirm report export directory" | No path suggestion given | Add: "Suggested: `C:\Temp\YangAgent_Sandbox_Output\`" |
| L78 "Apply ... on a reviewed CSV" | "Reviewed" is vague | Add explicit check: "Open the CSV in Excel and verify suggested_mark values before proceeding" |
| L82/L84 "Immediately test one Revit Undo" | Operator may forget after seeing success | Add **bold warning**: "Do not continue to the next step until Undo is confirmed" |

### Missing Feedback Fields

`What To Record` (L91-99) lists 7 fields. These 5 are missing:

| Missing Field | Why Needed |
|---------------|------------|
| Step number (1–34) | Same button may appear at multiple steps |
| Language setting at time of failure | Error messages differ between zh/en |
| Export directory path | Needed to locate output files |
| CSV filename (if apply failed) | Critical for Codex to diagnose -001/-007 |
| Retry count | Distinguish first failure from repeated |

### Steps Still Dependent on Live Revit

The following cannot be verified without an actual Revit session:

- Steps 55–56: pyRevit/YangAgent tab visibility
- Steps 61–87: All button execution
- Steps 82–84: Revit Undo behavior
- Steps 88–89: English output after language switch

None of these are runbook defects — the runbook is by design a live-session guide. The improvement is to label these steps with `[live Revit required]` inline.

### Apply Steps Need Clearer Separation

Steps 26–31 (apply + Undo) are the highest-risk steps in the sequence but are visually indistinguishable from the 25 read-only steps that precede them. An operator scanning quickly may treat apply with the same confidence as the read-only buttons.

Suggested: insert a separator line and a short safety block before step 26:

```
--- RISK ELEVATION: steps 26-31 modify the model ---
```

---

## Optional Appendix: Compact Operator Checklist

Derived from the runbook's 34-step sequence. Each line leaves space for ✓ or failure notes.

```
□ [ ] 1.  Revit open, pyRevit tab visible
□ [ ] 2.  YangAgent tab visible
□ [ ] 3.  Sandbox model open (filename contains _sandbox or _test)
□ [ ] 4.  System Settings → 中文
□ [ ] 5.  Export path set (e.g. C:\Temp\YangAgent_Sandbox_Output\)
□ [ ] 6.  Export Model Snapshot → files created
□ [ ] 7.  Model Health Report → .md created
□ [ ] 8.  Export Regression Checklist → .md created
□ [ ] 9.  Export AI Review Prompt → .md created
□ [ ] 10. Preview Missing Marks → .md + .csv created
□ [ ] 11. Preview Missing Room Numbers → .md + .csv created
□ [ ] 12. Preview Duplicate Room Numbers → .md + .csv created
□ [ ] 13. Preview Unplaced Views → .md + .csv created
□ [ ] 14. Preview View Naming Rules → .md + .csv created
□ [ ] 15. [CSV reviewed?] Open missing_door_window_marks_*.csv in Excel, check values
□ [ ] 16. Apply Door Window Marks → log files created
□ [ ] 17. Ctrl+Z Undo → visually confirm elements reverted
□ [ ] 18. [CSV reviewed?] Open missing_room_numbers_*.csv in Excel, check values
□ [ ] 19. Apply Room Numbers → log files created
□ [ ] 20. Ctrl+Z Undo → visually confirm elements reverted
□ [ ] 21. System Settings → English
□ [ ] 22. Re-run one report button → English output confirmed
```

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
| Compact checklist → standalone file | 2026-06-11 | Created `docs/sandbox-pyrevit-mvp-checklist.md`. The appendix below is retained as historical reference only. |
| Remove Marks L51 `"bad_csv"` dead code | 2026-06-11 | Not repurposed. Recorded here for cross-report traceability. Full detail in `hermes-code-review-apply-tools.md`. |
| 5 missing feedback fields → feedback template | 2026-06-11 | Codex landed them in `docs/sandbox-pyrevit-mvp-feedback-template.md`. Not added to the main runbook's "What To Record". |

---

## Questions for Codex

- (no truly open questions remain for this review — the 5 feedback fields decision is recorded above)
