from agents.sim_agent import SimulationAgent
import json

files = ["test_new_top.v", "Adder.v", "Subtractor.v", "Mux.v"]

top = "top"
tb = "overall_test"


agent = SimulationAgent(files, top, tb)

# Step 1: Run simulation
agent.run_simulation()

# Step 2: Get full intelligent report
report = agent.summarize_log_json()
if isinstance(report, dict):
    print(json.dumps(report, indent=4))
else:
    print(report)

