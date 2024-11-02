import os

llm_config = {
    "config_list": [
        {
            "model": "qwen-plus",
            "api_key": os.environ.get("ALI_API_KEY"),
            "base_url": "https://dashscope.aliyuncs.com/compatible-mode/v1",
            "api_type": "openai",
        }
    ]
}
