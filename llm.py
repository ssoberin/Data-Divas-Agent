from openai import OpenAI, APITimeoutError
import json
from typing import List, Dict, Any
from fastapi import HTTPException
from sqlalchemy.orm import Session
from services import build_ai_prompt  # твой метод сборки промпта

from openai import OpenAI, APITimeoutError

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key="sk-or-ваш_ключ"
)

def generate_snow_plan(session: Session) -> Dict[str, Any]:
    prompt_data = build_ai_prompt(session)

    system_message = {
        "role": "system",
        "content": (
            "Ты — система оптимизации вывоза снега для Казани. "
            "Создай оптимальный суточный план уборки снега с учётом всех ресурсов и условий. "
            "Возвращай строго JSON, без текста вне JSON. "
            "Правила: "
            "• Уборка начинается при накопленных осадках >=5 см. "
            "• Бригады работают по сменам (день/ночь). "
            "• Сначала снегоплавильные станции, сухие свалки — только при перегрузке. "
            "• Максимально оптимизируй пробег техники и распределение по сменам."
        )
    }

    user_message = {"role": "user", "content": prompt_data}

    messages = [system_message, user_message]

    try:
        completion = client.chat.completions.create(
            model="qwen/qwen3-235b-a22b-2507",
            messages=messages,
            max_tokens=4000,
            temperature=0.2,
            timeout=100
        )
        raw = completion.choices[0].message.content
        return json.loads(raw)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка модели: {e}")

