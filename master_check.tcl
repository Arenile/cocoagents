# Verification for test_new_top.v vs golden.v
read_verilog -r golden.v
read_verilog -r Adder.v
read_verilog -r Subtractor.v
read_verilog -r Mux.v

set_top golden

read_verilog -i test_new_top.v
read_verilog -i Adder.v
read_verilog -i Subtractor.v
read_verilog -i Mux.v
set_top top

match
verify
diagnose
report_failing_points
report_aborted_points
report_unmatched_points
report_black_boxes
report_error_candidates
report_constants
analyze_points -failing
exit