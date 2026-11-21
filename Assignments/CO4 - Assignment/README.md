# CSA08 Python Programming — Assignment 4 (CO4)
Robust data processing with files, exceptions, modules and packages

| | |
|---|---|
| Name | ______________ |
| Register number | ______________ |
| Python version | 3.13 (any Python 3.10+ should work) |
| Libraries | standard library only (see `requirements.txt`) |

## How to run (from this folder)

| Task | Command | What it shows |
|---|---|---|
| 1 | `cd Task01 && python3 make_sample.py` | creates `mess_oct.txt` and the 50,000-line `mess_big.txt` |
| 1 | `python3 original_script.py` | the poor script: prints total 1800 (correct is 5151.25) |
| 1 | `python3 repaired_script.py` (or `... nofile.txt`) | repaired script, rejected-line list, missing-file handling |
| 1 | `python3 read_vs_iterate.py` | alternative concept: memory of `read()` vs iteration |
| 2 | `cd Task02 && python3 generate_data.py && python3 attendance.py` | sample files, monthly report, below-75 list, damaged-line log |
| 2 | `python3 reread_vs_accumulate.py` | alternative concept: O(s·f·l) vs O(f·l) |
| 3 | `cd Task03 && python3 complete_code.py` | Complete-the-Code (expected output reproduced) |
| 3 | `python3 complete_code_missing_file.py` | missing file handled in `summarise()` |
| 3 | `python3 processor.py` / `failure_table.py` / `misuse_experiment.py` / `lbyl_vs_eafp.py` | try/except/else/finally, `raise ... from`, failure table, misuse experiment, EAFP vs LBYL |
| 4 | `cd Task04 && python3 buggy_library.py` / `fixed_library.py` / `manual_vs_with.py` | defects, repair, try/finally vs with |
| 5 | `cd Task05 && ./run_all.sh` | the four organisations (a)-(d) with the new report |
| 5 | `python3 import_forms_demo.py` | the three import forms, sys.modules cache |
| 6 | `cd Task06 && python3 run_festreg.py` | fest package on the sample input (one department file is missing on purpose) |
| 6 | `python3 test_festreg.py` / `python3 set_vs_list.py` | 7 asserted scenarios; set vs list |
| all | `./run_everything.sh` | runs every program; output saved in `<Task>/outputs/` |

`Task05/_before/` is the snapshot of the four organisations before the new "three consecutive absences" report was added; it is used only to count changed files with `diff -rq`.

## Result of each task (short note)
1. Original script prints 1800 for a file whose correct total is 5151.25 (paise amounts silently dropped). Repaired version gives 5151.25 and lists rejected lines. `read()` used ~5.4 MB against ~21 KiB for line iteration on 50,000 lines.
2. Monthly report, below-75 list (192311003, 192311006) and a damaged-line log with file name and line number. One pass over the files is ~80x faster than re-reading per student.
3. Complete-the-Code output matches expected: `(1, 1, [(3, 'expected 3 fields, found 2'), (4, "invalid status 'L'")])`. The misuse experiment shows `except Exception: pass` hiding a typing error.
4. Each defect reproduced (earlier days lost, titles joined, file left open, error not saved), then repaired.
5. Four organisations give identical output; the new report changed 1, 2, 3 and 3 files respectively.
6. The fest package handles a duplicate, invalid e-mails, a damaged line and a missing file; counts reconcile (13 lines = 8 unique + 1 duplicate + 4 rejected).

## Git (do this yourself, one commit per task)
```
git init && git branch -M main
git add Task01 && git commit -m "Task 1: diagnose and repair mess-bill script"
git add Task02 && git commit -m "Task 2: attendance processor"
...
git remote add origin https://github.com/<you>/CSA08-<RegisterNumber>-Assignment4.git
git push -u origin main
```
