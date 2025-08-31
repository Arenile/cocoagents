import os
import openai
from pathlib import Path
from tools.verilog_verifier import verilog_verifier_runner
import json 

openai.api_key = os.environ.get("OPENAI_API_KEY")


class VerificationAgent:
    """
    Conversational agent for running ewuivalence checking and generating structured JSON reports.
    """
    def __init__(self, sample, golden, support):
        self.sample = sample
        self.golden = golden
        self.support = support
        self.log_file = Path("logs/verify.log")
        self.chat_history = []

    def run_equivalence_checking(self):
        print("Running equivalence checking...")
        verilog_verifier_runner(self.sample, self.golden, self.support)
        

    def summarize_log_json(self):
        """
        Uses LLM to generate a structured JSON report from the verify.log,
        focusing on failing points and detailed conclusions.
        """
        # Read Verilog code
        verilog_code = ""
        for file in self.support:
            with open( file, "r") as f:
                verilog_code += f.read() + "\n"
        with open( self.sample[0], "r") as f:
                verilog_code += f.read() + "\n"
        # Read simulation log
        with open(self.log_file, "r") as f:
            log_text = f.read()

        prompt = f"""
You are a hardware verification assistant. Analyze the following Formality simulation log
and produce a **structured JSON report**. Follow these instructions:

1. Overview: brief summary of the design, verification status, total compare points.
2. Verification summary: include total compare points, passing, failing, aborted, unmatched, matched by name/signature/topology.
3. Failing points: summarize ranges where consecutive ports fail (e.g., "out[0]-out[7]") rather than listing each individually. Include reference port, implementation port, type, and issue.
4. Error candidates: list recommended and alternate candidates with descriptions.
5. Unmatched cone inputs: for each unmatched cone input, list reference and implementation cone and affected compare points (also aggregate ranges when possible).
6. Conclusion: detailed summary of root causes and recommendations for next investigation steps.

Return ONLY valid JSON — no extra text, no markdown. Structure example:

{{
    "overview": "...",
    "verification_summary": {{ ... }},
    "failing_points": [
        {{
            "ref_port_range": "r:/WORK/golden/out[0]-out[7]",
            "impl_port_range": "i:/WORK/top/out[0]-out[7]",
            "type": "Port",
            "issue": "not equivalent"
        }}
    ],
    "error_candidates": [ ... ],
    "unmatched_cone_inputs": [ ... ],
    "conclusion": detailed string with recommendations for what to investigate next
}}

Verilog design:
{verilog_code}

Verification log:
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