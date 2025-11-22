import pandas as pd
import csv
from typing import Dict, List, Any, Sequence
from langchain.tools import BaseTool
from pydantic import BaseModel, Field
import os
from datetime import datetime
import json
import uuid
from langchain.agents import create_react_agent
from langchain_core.runnables import RunnableConfig
from langchain_core.language_models.base import LanguageModelLike
from langchain_openai import OpenAI



class CSVDataInput(BaseModel):
    data: str = Field(description="Данные для сохранения в CSV в формате JSON")
    filename: str = Field(description="Имя файла для сохранения")


class CSVExportTool(BaseTool):
    tool_name: str = "csv_exporter"
    tool_description: str = "Экспорт данных в CSV файл. Сохраняет структурированные данные для дальнейшего использования."
    args_schema: type[BaseModel] = CSVDataInput

    def _run(self, data: str, filename: str) -> str:
        """Сохраняет данные в CSV файл"""
        try:
            # Парсим JSON данные
            data_dict = json.loads(data)

            # Генерация имени файла с timestamp
            if not filename.endswith('.csv'):
                filename += '.csv'

            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename_with_ts = f"{filename.split('.')[0]}_{timestamp}.csv"
            filepath = os.path.join("exports", filename_with_ts)

            # Создаем директорию если не существует
            os.makedirs("exports", exist_ok=True)

            # Сохраняем в CSV
            if isinstance(data_dict, list):
                # Если данные в виде списка
                df = pd.DataFrame(data_dict)
            elif isinstance(data_dict, dict):
                # Если данные в виде словаря
                if all(isinstance(val, list) for val in data_dict.values()):
                    # Словарь со списками
                    df = pd.DataFrame(data_dict)
                else:
                    # Одиночный словарь
                    df = pd.DataFrame([data_dict])
            else:
                return "❌ Неподдерживаемый формат данных"

            df.to_csv(filepath, index=False, encoding='utf-8-sig')

            return f"✅ Данные успешно экспортированы в: {filepath}"

        except json.JSONDecodeError:
            return "❌ Ошибка: Неверный формат JSON данных"
        except Exception as e:
            return f"❌ Ошибка экспорта в CSV: {str(e)}"


class DataProcessingInput(BaseModel):
    query: str = Field(description="Запрос для обработки данных")


class DataProcessingTool(BaseTool):
    tool_name: str = "data_processor"
    tool_description: str = "Обработка и структурирование данных из промпта пользователя. Собирает информацию о контрагенте и работах."
    args_schema: type[BaseModel] = DataProcessingInput

    def _run(self, query: str) -> str:
        """Обрабатывает данные из промпта и сохраняет в CSV"""
        try:
            # Собираем данные через функцию data_from_prompt
            structured_data = data_from_prompt()

            # Сохраняем основные данные в CSV
            csv_tool = CSVExportTool()

            # Сохраняем данные контрагента
            customer_csv = csv_tool._run(
                data=json.dumps([structured_data["customer"]], ensure_ascii=False),
                filename="customer_data"
            )

            # Сохраняем данные по работам
            jobs_csv = csv_tool._run(
                data=json.dumps(structured_data["jobs"], ensure_ascii=False),
                filename="jobs_data"
            )

            # Сохраняем полные данные
            full_data_csv = csv_tool._run(
                data=json.dumps(structured_data, ensure_ascii=False),
                filename="full_invoice_data"
            )

            return f"""
✅ Данные успешно обработаны и сохранены:

{customer_csv}
{jobs_csv}
{full_data_csv}

📊 Собранные данные:
• Контрагент: {structured_data['customer']['name']}
• ИНН: {structured_data['customer']['INN']}
• Количество работ: {len(structured_data['jobs'])}
• Общая сумма: {sum(job['price'] for job in structured_data['jobs'])} руб.
"""

        except Exception as e:
            return f"❌ Ошибка обработки данных: {str(e)}"


def data_from_prompt() -> Dict[str, Any]:
    """
    Функция для сбора данных от пользователя через промпт
    Возвращает структурированные данные для документов
    """
    print("\n📋 Сбор данных для документов:")

    data = {
        "customer": {},
        "jobs": []
    }

    # Данные контрагента
    print("\n👤 Введите данные контрагента:")
    data["customer"]["name"] = input("Название компании: ").strip()
    data["customer"]["INN"] = input("ИНН: ").strip()
    data["customer"]["OGRN"] = input("ОГРН: ").strip()

    # Работы/услуги
    print("\n💼 Введите работы/услуги (для завершения введите 'готово'):")
    while True:
        task_name = input("Наименование работы/услуги: ").strip()
        if task_name.lower() == 'готово':
            break
        if not task_name:
            continue

        # Проверка на курс
        if any(keyword in task_name.lower() for keyword in ['курс', 'обучение', 'training']):
            task_name = "Обучение одного сотрудника на курсе «Хардкорная веб-разработка»"
            price = 170000
            print(f"🎓 Автоматически установлена работа: {task_name}")
            print(f"💰 Стоимость: {price} руб.")
        else:
            try:
                price = int(input("Стоимость (руб): ").strip())
            except ValueError:
                print("❌ Ошибка: введите числовое значение")
                continue

        data["jobs"].append({
            "task": task_name,
            "price": price
        })

        add_more = input("Добавить еще работу? (да/нет): ").strip().lower()
        if add_more != 'да':
            break

    return data


# Заглушки для отсутствующих функций (замените на реальные)
def generate_pdf_act(*args, **kwargs):
    return "PDF акт сгенерирован"


def generate_pdf_invoice(*args, **kwargs):
    return "PDF счет сгенерирован"


REQUISITES_FILE = "requisites.txt"  # Замените на реальный файл


# Модифицированный класс LLMAgent
class LLMAgent:
    def __init__(self, model: LanguageModelLike, tools: Sequence[BaseTool]):
        self._model = model
        self._agent = create_react_agent(
            model,
            tools=tools,
            checkpointer=InMemorySaver())
        self._config: RunnableConfig = {
            "configurable": {"thread_id": uuid.uuid4().hex}}

    def upload_file(self, file):
        print(f"upload file {file} to LLM")
        # Заглушка для загрузки файла
        return "file_uploaded_id"

    def invoke(
            self,
            content: str,
            attachments: list[str] | None = None,
            temperature: float = 0.1
    ) -> str:
        """Отправляет сообщение в чат"""
        message: dict = {
            "role": "user",
            "content": content,
            **({"attachments": attachments} if attachments else {})
        }
        # Заглушка для вызова агента
        return f"Агент получил: {content}"


def print_agent_response(llm_response: str) -> None:
    print(f"\033[35m{llm_response}\033[0m")


def get_user_prompt() -> str:
    return input("\nТы: ")


def main():
    model = OpenAI(
        model="GigaChat-2-Max",
        api_key="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",
        base_url="https://openrouter.ai/api/v1"
    )

    # Добавляем инструмент обработки данных в CSV
    agent = LLMAgent(model, tools=[
        # generate_pdf_act,  # Раскомментируйте когда будут реальные функции
        # generate_pdf_invoice,
        DataProcessingTool(),  # Новый инструмент
        CSVExportTool()  # Инструмент для экспорта
    ])

    system_prompt = (
        "Твоя задача спросить у пользователя, что он хочет сгенерировать — акт или счёт или оба документа. "
        "Затем нужно сгенерировать акт или счёт, для этого тебе надо взять реквизиты "
        "контрагента из приложенного файла, а также запроси работы для включения в "
        "акт (наименования задач и их стоимость), работ может быть несколько. "
        "Если пользователь указывает в качестве работы курс, то для документов берём одну работу, в точности такую "
        "\"Обучение одного сотрудника на курсе «Хардкорная веб-разработка»\", стоимостью 170 тыс руб."
        "Никакие данные не придумывай, всё необходимое строго запроси у "
        "пользователя. Мои реквизиты не запрашивай, они есть в моём коде. "
        "Имя и отчество подписанта сокращаем до одной первой буквы, "
        "например, Иванов А.Е. "
        "Название компании оборачиваем в кавычки ёлочкой, например, "
        "ООО «Рога и копыта», то есть до названия компании ставим « и после названия "
        "ставим »."
        "Также ты можешь использовать инструмент data_processor для сбора структурированных данных "
        "и сохранения их в CSV файлы для дальнейшего использования."
    )

    # file_uploaded_id = agent.upload_file(open(REQUISITES_FILE, "rb"))  # Раскомментируйте когда будет файл
    agent_response = agent.invoke(content=system_prompt)  # , attachments=[file_uploaded_id])

    while True:
        print_agent_response(agent_response)
        user_input = get_user_prompt()

        # Автоматический вызов обработки данных при определенных командах
        if any(cmd in user_input.lower() for cmd in ['собрать данные', 'обработать данные', 'data', 'csv']):
            processing_tool = DataProcessingTool()
            result = processing_tool._run(user_input)
            print_agent_response(result)
            continue

        agent_response = agent.invoke(user_input)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nдосвидули!")