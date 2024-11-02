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
