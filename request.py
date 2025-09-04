import base64
import requests
import mimetypes  # 用于自动识别图片类型

# 1. 设置 API 地址和本地图片路径
VLLM_API_URL = "http://10.10.185.1:61801/v1/chat/completions"
# 将这里替换成你自己的本地图片路径
LOCAL_IMAGE_PATH = "/Users/hanrui/Desktop/Haojing/pycharmproject/LLaMA-Factory/docchain/1.png" 
# 例如: "/home/hanrui/images/my_cat.jpg" 或 "C:\\Users\\Hanrui\\Pictures\\my_cat.jpg"

# 2. 编写一个函数将图片编码为 Base64 字符串
def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")

# 3. 构建请求体 (Payload)
# 调用函数获取 Base64 编码和 MIME 类型
base64_image = encode_image(LOCAL_IMAGE_PATH)

headers = {
    "Content-Type": "application/json"
}

payload = {
    "model": "qwen",  # 这是你启动服务时 --served-model-name 指定的名字
    "messages": [
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": "这张图片里有什么？请详细描述。"
                },
                {
                    "type": "image_url",  # 使用 "image" 类型
                    "image_url": {"url": f"data:image/png;base64,{base64_image}"}, 
                }
            ]
        }
    ],
}

# 4. 发送 POST 请求
try:
    response = requests.post(VLLM_API_URL, headers=headers, json=payload)
    response.raise_for_status()  # 如果请求失败 (例如 4xx 或 5xx 错误), 会抛出异常

    # 5. 打印结果
    result = response.json()
    print(result['choices'][0]['message']['content'])

except requests.exceptions.RequestException as e:
    print(f"An error occurred: {e}")
    # 如果有响应内容，也打印出来方便排查
    if e.response is not None:
        print(f"Error details: {e.response.text}")
