from http import HTTPStatus
from urllib.parse import urlparse, unquote
from pathlib import PurePosixPath
import requests
from dashscope import ImageSynthesis
from .config import api_key

model = "flux-schnell"
prompt = "Eagle flying freely in the blue sky and white clouds"
prompt_cn = "一只飞翔在蓝天白云的鹰"


def sample_block_call(input_prompt):
    rsp = ImageSynthesis.call(
        model=model, prompt=input_prompt, size="1024*1024", api_key=api_key
    )
    if rsp.status_code == HTTPStatus.OK:
        print(rsp.output)
        print(rsp.usage)
        # save file to current directory
        for result in rsp.output.results:
            file_name = PurePosixPath(unquote(urlparse(result.url).path)).parts[-1]
            with open("./%s" % file_name, "wb+") as f:
                f.write(requests.get(result.url).content)
    else:
        print(
            "Failed, status_code: %s, code: %s, message: %s"
            % (rsp.status_code, rsp.code, rsp.message)
        )


def sample_async_call(input_prompt):
    rsp = ImageSynthesis.async_call(
        model=model, prompt=input_prompt, size="1024*1024", api_key=api_key
    )
    if rsp.status_code == HTTPStatus.OK:
        print(rsp.output)
        print(rsp.usage)
    else:
        print(
            "Failed, status_code: %s, code: %s, message: %s"
            % (rsp.status_code, rsp.code, rsp.message)
        )
    status = ImageSynthesis.fetch(rsp)
    if status.status_code == HTTPStatus.OK:
        print(status.output.task_status)
    else:
        print(
            "Failed, status_code: %s, code: %s, message: %s"
            % (status.status_code, status.code, status.message)
        )

    rsp = ImageSynthesis.wait(rsp)
    if rsp.status_code == HTTPStatus.OK:
        print(rsp.output)
    else:
        print(
            "Failed, status_code: %s, code: %s, message: %s"
            % (rsp.status_code, rsp.code, rsp.message)
        )


def ex2():
    sample_block_call(prompt)
