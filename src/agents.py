import os
from autogen import ConversableAgent, register_function
from .prompts import code_writer_system_message, tool_assistant_system_message
from .config import llm_config
from autogen.coding import LocalCommandLineCodeExecutor
from .tools.calculator import calculator

code_writer_agent = ConversableAgent(
    "code_writer_agent",
    system_message=code_writer_system_message,
    llm_config=llm_config,
    code_execution_config=False,  # Turn off code execution for this agent.
)

executor = LocalCommandLineCodeExecutor(
    timeout=10,  # Timeout for each code execution in seconds.
    work_dir="./code_run",  # Use the temporary directory to store the code files.
)

# Create an agent with code executor configuration.
code_executor_agent = ConversableAgent(
    "code_executor_agent",
    llm_config=False,  # Turn off LLM for this agent.
    code_execution_config={
        "executor": executor
    },  # Use the local command line code executor.
    human_input_mode="ALWAYS",  # Always take human input for this agent for safety.
)


# tools agents
tool_assistant = ConversableAgent(
    "tool_assistant",
    system_message=tool_assistant_system_message,
    llm_config=llm_config,
)

user_agent = ConversableAgent(
    "user_agent",
    llm_config=False,
    is_termination_msg=lambda x: "TERMINATE" in x.get("content", ""),
    human_input_mode="NEVER",
)

register_function(
    calculator,
    caller=tool_assistant,
    executor=user_agent,
    name="calculator",
    description="一个简单的计算器",
)

##### group chat #####
# The Number Agent always returns the same numbers.
number_agent = ConversableAgent(
    name="Number_Agent",
    system_message="You return me the numbers I give you.",
    llm_config=llm_config,
    human_input_mode="NEVER",
    is_termination_msg=lambda x: x.get("content", "").strip().endswith("10"),
)

# The Adder Agent adds 1 to each number it receives.
adder_agent = ConversableAgent(
    name="Adder_Agent",
    system_message="You add 1 to each number I give you and return me the new numbers.",
    llm_config=llm_config,
    human_input_mode="NEVER",
)

# The Multiplier Agent multiplies each number it receives by 2.
multiplier_agent = ConversableAgent(
    name="Multiplier_Agent",
    system_message="You multiply each number I give you by 2 and return me the new numbers.",
    llm_config=llm_config,
    human_input_mode="NEVER",
)

# The Subtracter Agent subtracts 1 from each number it receives.
subtracter_agent = ConversableAgent(
    name="Subtracter_Agent",
    system_message="You subtract 1 from each number I give you and return me the new numbers.",
    llm_config=llm_config,
    human_input_mode="NEVER",
)

# The Divider Agent divides each number it receives by 2.
divider_agent = ConversableAgent(
    name="Divider_Agent",
    system_message="You divide each number I give you by 2 and return me the new numbers.",
    llm_config=llm_config,
    human_input_mode="NEVER",
)

adder_agent.description = "Add 1 to each input number."
multiplier_agent.description = "Multiply each input number by 2."
subtracter_agent.description = "Subtract 1 from each input number."
divider_agent.description = "Divide each input number by 2."
number_agent.description = "Return the numbers given."
