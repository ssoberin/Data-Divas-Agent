from operator import truediv

from openai import OpenAI


API_KEY = "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"

def snow_height_analyse(url:str)->bool:
    client = OpenAI(
        api_key=API_KEY,
        base_url="https://openrouter.ai/api/v1"
    )

    completion = client.chat.completions.create(
    extra_body={},
    max_tokens=3000,
    model="openai/gpt-5-image-mini",
    messages=[
        {
        "role": "user",
        "content": [
            {
            "type": "text",
            "text": '''если снега на дороге > 8 сантиметров, ответь мне: да. Иначе: нет'''
            },
            {
            "type": "image_url",
            "image_url": {
                "url": url
            }
            }
        ]
        }
    ]
    )
    resp = completion.choices[0].message.content
    if resp=="да":
        return True
    else: return False