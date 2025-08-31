import os
import openai
from tools.testbench_runner import test_my_design_runner as run_simulation
from pathlib import Path
import json 

openai.api_key = os.environ.get("OPENAI_API_KEY")

class SimulationAgent:
    """
    Conversational agent for running simulation and generating structured JSON reports.
    Only failing tests are included in detailed_tests.
    """
    def __init__(self, source_files, top_module, test_module):
        self.source_files = source_files
        self.top_module = top_module
        self.test_module = test_module
        self.log_file = Path("logs/sim.log")
        self.chat_history = []

    def run_simulation(self):
        print("Running simulation...")
        results, log_file = run_simulation(
            self.source_files, self.top_module, self.test_module, log_file=self.log_file
        )
        print("Simulation finished. Log saved to:", log_file)
        return log_file

    def summarize_log_json(self):
        """
        Uses LLM to generate a structured JSON report from the sim.log,
        focusing on failing tests and detailed conclusions.
        """
        # Read Verilog code
        verilog_code = ""
        for file in self.source_files:
            with open( file, "r") as f:
                verilog_code += f.read() + "\n"

        # Read simulation log
        with open(self.log_file, "r") as f:
            log_text = f.read()

        prompt = f"""
You are a hardware verification assistant. Analyze the following Cocotb simulation log along side the given Verilog design
and provide a structured JSON report focusing **only on failing tests**. Include:

- "overview": brief string summarizing simulation
- "test_summary": {{
    "total_tests": int,
    "pass_count": int,
    "fail_count": int,
    "skip_count": int
}}
- "detailed_tests": [ 
    {{
        "test_number": int,
        "inputs": dict,
        "expected_outputs": dict,
        "actual_outputs": dict,
        "failure_reason": string
    }} 
]  # Include only failing tests
- "conclusion": detailed string with recommendations for what to investigate next

Verilog design:
{verilog_code}

Simulation log:
{log_text}

Return ONLY a valid JSON object.
"""

        response = openai.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            temperature=0
        )

        json_text = response.choices[0].message.content

        # Try to parse the JSON
        try:
            report = json.loads(json_text)
        except json.JSONDecodeError:
            print("Warning: Could not parse JSON. Returning raw LLM output.")
            report = json_text

        return report