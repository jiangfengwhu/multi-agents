from src.agents import (
    code_writer_agent,
    code_executor_agent,
    user_agent,
    tool_assistant,
)

import datetime

# today = datetime.datetime.now().strftime("%Y-%m-%d")
# chat_result = code_executor_agent.initiate_chat(
#     code_writer_agent,
#     message=f"Today is {today}. Write Python code to plot TSLA's and META's "
#     "stock price gains YTD, and save the plot to a file named 'stock_gains.png'.",
# )

user_agent.initiate_chat(
    tool_assistant,
    message="(1423 - 123) / 3 + (32 + 23) * 5等于多少",
)
