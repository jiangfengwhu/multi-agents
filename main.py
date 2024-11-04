from src.agents import (
    code_writer_agent,
    code_executor_agent,
    user_agent,
    tool_assistant,
    adder_agent,
    multiplier_agent,
    subtracter_agent,
    divider_agent,
    number_agent,
)
import datetime
from autogen import GroupChat, runtime_logging, GroupChatManager
from src.config import llm_config

logging_session_id = runtime_logging.start(config={"dbname": "logs.db"})
print("Logging session ID: " + str(logging_session_id))

# today = datetime.datetime.now().strftime("%Y-%m-%d")
# chat_result = code_executor_agent.initiate_chat(
#     code_writer_agent,
#     message=f"Today is {today}. Write Python code to plot TSLA's and META's "
#     "stock price gains YTD, and save the plot to a file named 'stock_gains.png'.",
# )

# user_agent.initiate_chat(
#     tool_assistant,
#     message="(1423 - 123) / 3 + (32 + 23) * 5等于多少",
# )

allowed_transitions = {
    number_agent: [adder_agent, number_agent],
    adder_agent: [multiplier_agent, number_agent],
    subtracter_agent: [divider_agent, number_agent],
    multiplier_agent: [subtracter_agent, number_agent],
    divider_agent: [adder_agent, number_agent],
}
group_chat = GroupChat(
    agents=[
        adder_agent,
        multiplier_agent,
        subtracter_agent,
        divider_agent,
        number_agent,
    ],
    messages=[],
    max_round=12,
    send_introductions=True,
    allowed_or_disallowed_speaker_transitions=allowed_transitions,
    speaker_transitions_type="allowed",
)
group_chat_manager = GroupChatManager(
    groupchat=group_chat,
    llm_config=llm_config,
    is_termination_msg=lambda x: x.get("content", "").strip().endswith("10"),
)
chat_result = number_agent.initiate_chat(
    group_chat_manager,
    message="My number is 3, I want to turn it into 10. Once I get to 10, keep it there.",
    summary_method="reflection_with_llm",
)
print(chat_result.summary)


runtime_logging.stop()
