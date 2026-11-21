#!/bin/sh
# Runs every program and stores its output in <Task>/outputs/ (used to build the report).
cd "$(dirname "$0")"
run() { dir=$1; out=$2; shift 2; mkdir -p "$dir/outputs"; (cd "$dir" && "$@") > "$dir/outputs/$out.txt" 2>&1 || echo "FAILED: $dir $*"; }
run Task01 make_sample              python3 make_sample.py
run Task01 original_script          python3 original_script.py
run Task01 repaired_script          python3 repaired_script.py
run Task01 repaired_missing_file    sh -c 'python3 repaired_script.py nofile.txt; true'
run Task01 read_vs_iterate          python3 read_vs_iterate.py
run Task02 generate_data            python3 generate_data.py
run Task02 attendance               python3 attendance.py
run Task02 reread_vs_accumulate     python3 reread_vs_accumulate.py
run Task03 complete_code            python3 complete_code.py
run Task03 complete_code_missing    python3 complete_code_missing_file.py
run Task03 processor                python3 processor.py
run Task03 failure_table            python3 failure_table.py
run Task03 misuse_experiment        python3 misuse_experiment.py
run Task03 lbyl_vs_eafp             python3 lbyl_vs_eafp.py
run Task04 buggy_library            python3 buggy_library.py
run Task04 fixed_library            python3 fixed_library.py
run Task04 manual_vs_with           python3 manual_vs_with.py
run Task05 organisations_after      ./run_all.sh
run Task05 import_forms_demo        python3 import_forms_demo.py
run Task06 test_festreg             python3 test_festreg.py
run Task06 run_festreg              python3 run_festreg.py
run Task06 set_vs_list              python3 set_vs_list.py
find . -name __pycache__ -prune -exec rm -rf {} +
echo "done"
