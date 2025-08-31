import os
from pathlib import Path
from cocotb.runner import get_runner, get_results

os.environ["COCOTB_LOG_LEVEL"] = "INFO"

def test_my_design_runner(
    source_files: list[str], 
    top_module: str, 
    test_module: str, 
    sim: str = "icarus",
    log_file: Path | str = None
):
    """
    Run a Cocotb testbench on the given Verilog sources.

    Args:
        source_files: List of Verilog files to compile
        top_module: Top-level module to simulate
        test_module: Testbench module name
        sim: Simulator to use (default "icarus")
        log_file: Path to write simulation log (optional)

    Returns:
        dict: Parsed results from results.xml
    """
    proj_path = Path(__file__).resolve().parent.parent

    sources = [proj_path  / f for f in source_files]

    runner = get_runner(sim)
    runner.build(
        sources=sources,
        hdl_toplevel=top_module,
    )

    if log_file is None:
        log_file = proj_path / "logs"/ "sim.log"

    runner.test(
        hdl_toplevel=top_module, 
        test_module=test_module, 
        log_file=log_file
    )

    xml_file = proj_path / "sim_build" / "results.xml"
    results = get_results(xml_file)

    return results, log_file
