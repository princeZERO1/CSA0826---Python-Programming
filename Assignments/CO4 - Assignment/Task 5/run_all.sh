#!/bin/sh
# Runs the four organisations (from their own folders so imports resolve).
cd "$(dirname "$0")"
echo "== (a) one script";          (cd a_single  && python3 attendance_single.py)
echo "== (b) module + main";       (cd b_module  && python3 main_b.py)
echo "== (c) three modules";       (cd c_three   && python3 main_c.py)
echo "== (d) package";             (cd d_package && python3 main_d.py)
