import os
from autogen import LLMConfig, ConversableAgent
# Main file for configuring LLM Agents 

# LLM setup 
llm_config = LLMConfig(
    api_type="openai",
    model="gpt-4o-mini",
    api_key=os.environ["OPENAI_API_KEY"],
    temperature=0.5
)

# Agent setup
connection_agent = ConversableAgent(
    name="connection_agent", 
    system_message="You are a computer engineer working with Verilog", 
    llm_config=llm_config
)

test_response = connection_agent.run(
    message="How many stages should I have in a simple pipelined processor in RISC-V?", 
    max_turns=2,
    user_input=True
)

test_response.process()

# Tool registration 
    # Verilog Connection Manipulation Tool
    # Testbench Runner Tool
    # Formality Runner Tool 

