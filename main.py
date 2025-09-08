import os
from autogen import LLMConfig, ConversableAgent
from tools.connection_maker import print_design, get_starting_design, modify_connections
# Main file for configuring LLM Agents 

# LLM setup 
# llm_config = LLMConfig(
#     api_type="openai",
#     model="gpt-4o-mini",
#     api_key=os.environ["OPENAI_API_KEY"],
#     temperature=0.5,
#     arbitrary_types_allowed=True
# )
ollama_config = {
    "model": "deepseek-r1:14b",
    "api_type": "ollama", 
    "client_host": "http://10.0.0.58:11434"
}

designer_system_msg = """
You are a computer hardware engineer. You receive instructions on 
changes to make to a design and then use your available tools to make
changes to the connections in that computer hardware design. 

For each task:
1) Get the current hardware design using the get_starting_design tool
2) Figure our which connections need to be changed to achieve the desired
behavior. 
3) Make those connection changes using the modify_connections tool
4) Report the changes you made
5) List all of the connections in the design using the print_design tool

Provide clear reasoning for the connection changes you make. 
"""

# Agent setup
connection_agent = ConversableAgent(
    name="connection_agent", 
    system_message="You are a computer hardware engineer", 
    llm_config=ollama_config,
    # functions=[modify_connections, print_design, get_starting_design]
)

test_response = connection_agent.run(
    message="How many pipeline stages should I have for my out-of-order RISC-V CPU?", 
    max_turns=2,
    user_input=True
)

test_response.process()

# Tool registration 
    # Verilog Connection Manipulation Tool
    # Testbench Runner Tool
    # Formality Runner Tool 

