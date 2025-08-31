from agents.verify_agent import VerificationAgent
import json

sample = ["test_new_top.v", "top"]
golden = ["golden.v", "golden"]
support = [ "Adder.v", "Subtractor.v", "Mux.v"]


agent = VerificationAgent(sample, golden, support)

# Step 1: Run simulation
agent.run_equivalence_checking()

# Step 2: Get full intelligent report
report = agent.summarize_log_json()
if isinstance(report, dict):
    print(json.dumps(report, indent=4))
else:
    print(report)

