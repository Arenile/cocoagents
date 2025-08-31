import os
import subprocess

fm_shell_cmd = [
    "fm_shell", 
    "-f", "master_check.tcl", 
    "-work_path", "./fm_work"
]

def generate_check_tcl(original, golden, top_orig, top_gold, support):
        golden_reads = "\n".join([f"read_verilog -r {golden}"] + [f"read_verilog -r {f}" for f in support])
        original_reads = "\n".join([f"read_verilog -i {original}"] + [f"read_verilog -i {f}" for f in support])

        tcl_script = f"""
# Verification for {original} vs {golden}
{golden_reads}

set_top {top_gold}

{original_reads}
set_top {top_orig}

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
    """
        return tcl_script.strip()


def verilog_verifier_runner(sample, golden, support):
    base_path = os.getcwd()
    master_check_path = os.path.join(base_path, "master_check.tcl")
    tcl_output = generate_check_tcl(sample[0], golden[0], sample[1], golden[1], support)

    with open(master_check_path, "w") as master_file:
        master_file.write(tcl_output)

    with open("logs/verify.log", "w") as logfile:
        process = subprocess.run(fm_shell_cmd, stdout=logfile, stderr=subprocess.STDOUT)

