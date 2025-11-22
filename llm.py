from typing import Dict, Any, List
from openai import OpenAI, APITimeoutError
import json

# OpenRouter
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key="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"
)

ENGINE_NAME = "qwen/qwen3-235b-a22b-2507"

def call_model_api(prompt: Dict[str, Any]) -> Dict[str, Any]:
    """
    Отправляет промпт в ИИ и получает строго JSON-ответ.
    prompt — это dict, который содержит все данные:
    - system_context
    - available_resources
    - weather
    - goals
    и т.д.
    """

    # Формируем system и user сообщения
    messages: List[Dict[str, str]] = [
        {
            "role": "system",
            "content": (
        "system_context": {
            "role": "Ты - система оптимизации вывоза снега для Казани. Твоя задача - создать оптимальный суточный план уборки снега с учетом всех доступных ресурсов и условий.",
            "constraints": [
                "Уборка начинается при накопленных осадках >=5 см",
                "Техника должна использоваться рационально с учетом ее вместимости",
                "Бригады распределяются по сменам (дневная/ночная)",
                "Нагрузка на снегоплавильные станции должна быть сбалансирована",
                "Сухие свалки используются только при перегрузке станций"
            ]
            )
        },
        {
            "role": "user",
            "content": json.dumps(prompt, ensure_ascii=False)
        }
    ]

    try:
        completion = client.chat.completions.create(
            model=ENGINE_NAME,
            messages=messages,
            max_tokens=4000,
            temperature=0.2,
            timeout=15  # увеличил на случай долгих расчётов
        )
        raw = completion.choices[0].message.content

        # Попытка распарсить в JSON
        return json.loads(raw)

    except APITimeoutError:
        raise RuntimeError("⏱️ Таймаут: модель ответила слишком долго")

    except json.JSONDecodeError:
        raise RuntimeError("❌ Модель вернула невалидный JSON. Нужен строгий JSON.")

    except Exception as e:
        raise RuntimeError(f"🔥 Ошибка при запросе к ИИ: {str(e)}")
