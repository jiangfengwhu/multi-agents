import os
from openai import OpenAI

from swarm import Swarm, Agent
from .config import api_key, base_url

base_client = OpenAI(
    api_key=api_key,
    base_url=base_url,
)
client = Swarm(
    client=base_client,
)
model = "qwen-plus"


def transfer_to_add():
    print("返回Add Agent")
    return add_agent


def transfer_to_multiply():
    print("返回Multiply Agent")
    return multiply_agent


def transfer_to_subtract():
    print("返回Subtract Agent")
    return subtract_agent


def transfer_to_divide():
    print("返回Divide Agent")
    return divide_agent


def transfer_to_number():
    """执行完毕将返回数字"""
    print("返回Number Agent")
    return number_agent


def add_one(number: int):
    print(f"Add Agent执行完毕：{number + 1}")
    return f"现在数字是{number + 1}"


def subtract_one(number: int):
    print(f"Subtract Agent执行完毕：{number - 1}")
    return f"现在数字是{number - 1}"


def multiply_two(number: int):
    print(f"Multiply Agent执行完毕：{number * 2}")
    return f"现在数字是{number * 2}"


def divide_two(number: int):
    print(f"Divide Agent执行完毕：{number / 2}")
    return f"现在数字是{number / 2}"


number_agent = Agent(
    name="Number Agent",
    instructions="你是一个数字转换器，你的任务是将给定数字转换成目标数字，你可以调用四种运算，分别为加1（transfer_to_add），减1（transfer_to_subtract），乘2（transfer_to_multiply），除2（transfer_to_divide），要求尽量快的进行转换，请选择接下来要执行的运算",
    model=model,
    functions=[
        transfer_to_add,
        transfer_to_multiply,
        transfer_to_subtract,
        transfer_to_divide,
    ],
)
add_agent = Agent(
    name="Add Agent",
    instructions="将数字加1并返回现在的数字, 如果数字已经等于目标数字，则返回目标数字，否则调用transfer_to_number继续下一步的转换",
    model=model,
    functions=[transfer_to_number, add_one],
)
multiply_agent = Agent(
    name="Multiply Agent",
    instructions="将数字乘以2并返回现在的数字, 如果数字已经等于目标数字，则返回目标数字，否则调用transfer_to_number继续下一步的转换",
    model=model,
    functions=[transfer_to_number, multiply_two],
)
divide_agent = Agent(
    name="Divide Agent",
    instructions="将数字除以2并返回现在的数字, 如果数字已经等于目标数字，则返回目标数字，否则调用transfer_to_number继续下一步的转换",
    model=model,
    functions=[transfer_to_number, divide_two],
)
subtract_agent = Agent(
    name="Subtract Agent",
    instructions="将数字减1并返回现在的数字, 如果数字已经等于目标数字，则返回目标数字，否则调用transfer_to_number继续下一步的转换",
    model=model,
    functions=[transfer_to_number, subtract_one],
)


def ex1():
    messages = [{"role": "user", "content": "使用最少的操作路径把数字3变成13"}]
    response = client.run(agent=number_agent, messages=messages)
    print(response.messages[-1]["content"])
