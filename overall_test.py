import cocotb
from cocotb.triggers import Timer, RisingEdge
from cocotb.clock import Clock

test_vectors = [
    {"inputs": {"a": 6, "b": 3, "c": 2,}, "expected": {"add1_a_monitor": 6}},
    {"inputs": {"a": 6, "b": 3, "c": 2,}, "expected": {"add1_b_monitor": 3}},
    {"inputs": {"a": 6, "b": 3, "c": 2,}, "expected": {"add1_o_sum_monitor": 9,}},
    {"inputs": {"a": 6, "b": 3, "c": 2,}, "expected": {"sub1_a_monitor": 6}},
    {"inputs": {"a": 6, "b": 3, "c": 2,}, "expected": {"sub1_b_monitor": 2}},
    {"inputs": {"a": 6, "b": 3, "c": 2,}, "expected": {"sub1_diff_monitor": 4,}},
    {"inputs": {"a": 6, "b": 3, "c": 2, "s": 0}, "expected": {"mux1_a_monitor": 9}},
    {"inputs": {"a": 6, "b": 3, "c": 2, "s": 0}, "expected": {"mux1_b_monitor": 4}},
    {"inputs": {"a": 6, "b": 3, "c": 2, "s": 0}, "expected": {"out": 9}},
    {"inputs": {"a": 6, "b": 3, "c": 2, "s": 1}, "expected": {"out": 4}},
]

async def generate_clock(dut, period_ns=2):
    cocotb.start_soon(Clock(dut.clk, period_ns // 2, units="ns").start())

async def run_single_test(dut, vector, idx):
    await generate_clock(dut)

    # Initial reset sequence
    dut.reset.value = 1
    await Timer(1, units="ns")
    await RisingEdge(dut.clk)
    dut.reset.value = 0
    await Timer(1, units="ns")
    await RisingEdge(dut.clk)
    dut.reset.value = 1
    await Timer(1, units="ns")
    await RisingEdge(dut.clk)

    # Apply inputs
    for sig, val in vector.get("inputs", {}).items():
        getattr(dut, sig).value = val

    await RisingEdge(dut.clk)
    await Timer(1, units="ns")
    await RisingEdge(dut.clk)

    # Check expected outputs
    for sig, expected_val in vector["expected"].items():
        actual_val = getattr(dut, sig).value
        val_str = actual_val.binstr.lower()

        if expected_val == "x":
            return  # skip this signal

        if 'x' in val_str or 'z' in val_str:
            raise ValueError(f"Test {idx+1}: Signal {sig} is undefined ('x/z'), expected {expected_val}")

        actual_int = int(actual_val)
        assert actual_int == expected_val, (
            f"Test {idx+1}: {sig} expected {expected_val:#x}, got {actual_int:#x}"
        )

    dut._log.info(f"Test {idx+1} passed with inputs {vector['inputs']} and outputs {vector['expected']}")

# Dynamically create one @cocotb.test for each test vector
for idx, vector in enumerate(test_vectors):
    test_func = lambda dut, v=vector, i=idx: run_single_test(dut, v, i)
    test_name = f"test_vector_{idx+1}"
    globals()[test_name] = cocotb.test()(test_func)
