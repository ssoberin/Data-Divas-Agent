import csv
import os
from datetime import date
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.tools import tool
from langchain_core.messages import AIMessage, HumanMessage

CSV_FILENAME = "plan_technics.csv"
API_KEY = "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"

llm = ChatOpenAI(
    model="qwen/qwen3-235b-a22b-2507",
    temperature=0.3,
    api_key=API_KEY,
    base_url="https://openrouter.ai/api/v1"
)

@tool
def add_technic_entry(
        area:str,
        resp:str,
        phone:str,
        mode:str,
        time:str,
        techtype:str,
        amount:str,
        plan:str,
        worktype:str
)->str:
    """Функция для добавления записи в CSV файл или для его создания, если файла не существует"""
    data={
            "участок": area,
            "ответственный": resp,
            "телефон": phone,
            "режим": mode,
            "время": time,
            "тип_техники": techtype,
            "количество": amount,
            "плановое_задание": plan,
            "вид_работ": worktype
    }

    file_exists = os.path.isfile(CSV_FILENAME)

    try:

        with open(CSV_FILENAME, "a", newline="", encoding="utf-8-sig") as f:
            writer = csv.writer(f, delimiter=";")
            if not file_exists:
                writer.writerow([
            "Участок", "Ответственный", "Телефон", "Режим",
            "Время", "Тип техники", "Кол-во", "Плановое задание", "Вид работ"
                ])
            writer.writerow([
                data["участок"],
                data["ответственный"],
                data["телефон"],
                data["режим"],
                data["время"],
                data["тип_техники"],
                data["количество"],
                data["плановое_задание"],
                data["вид_работ"]
            ])
            return("✅ Запись добавлена.")
    except FileNotFoundError:
        return("filenotfound")

@tool
def list_all_entries() -> str:
    """Функция для вывода всех данных файла CSV"""
    if not os.path.exists(CSV_FILENAME):
        return "❌ Файл с планом ещё не создан."

    rows = []
    with open(CSV_FILENAME, "r", encoding="utf-8") as f:
        reader = csv.reader(f)
        header = next(reader)
        rows.append(header)
        for row in reader:
            rows.append(row)

    maxlength = [max(len(str(row[i])) for row in rows) for i in range(len(header))]
    lines = []
    for i, row in enumerate(rows):
        line = " | ".join(str(cell).ljust(maxlength[j]) for j, cell in enumerate(row))
        lines.append(line)
        if i == 0:
            lines.append("-" * len(line))
    return "\n".join(lines)

@tool
def search_entries(query: str) -> str:
    """Функция для поиска строки по запросу пользователя из файла CSV"""
    if not os.path.exists(CSV_FILENAME):
        return "❌ Файл с планом ещё не создан."

    matches = []
    with open(CSV_FILENAME, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            if any(query.lower() in str(val).lower() for val in row.values()):
                matches.append(row)

    if not matches:
        return f"🔍 Ничего не найдено по запросу: *{query}*"

    res = [f"🔍 Найдено {len(matches)} записей по '{query}':"]
    for m in matches[:5]:
        res.append(f"- {m['Участок']} | {m['Тип техники']} ({m['Кол-во']}) | {m['Вид работ']} | {m['Плановое задание']}")
    if len(matches) > 5:
        res.append(f"... и ещё {len(matches)-5} записей.")
    return "\n".join(res)

tools = [add_technic_entry, list_all_entries, search_entries]

prompt = ChatPromptTemplate.from_messages([
    ("system", f"""Сегодня {date.today().strftime('%d.%m.%Y')}. Ты — ассистент по плану техники.
    Твоя задача - использовать заданные тебе функции и по запросу пользователя:
    1. записывать введенные данные в СSV файл, если его нет - создать. Если данных не хватает для заданных столбцов файла - про
си у пользователя дополнить эти данные
    2. выдавать записи из файла по ключевому слову
    3. выдавать список записей из файла"""),
    ("placeholder", "{chat_history}"),
    ("human", "{input}"),
    ("placeholder", "{agent_scratchpad}")
])
from langchain.agents import create_tool_calling_agent, AgentExecutor
agent = create_tool_calling_agent(llm, tools, prompt)
agent_executor = AgentExecutor(
    agent=agent,
    tools=tools,
    verbose=True,
    handle_parsing_errors=True,
    max_iterations=10
)

def main():
    print("⚡ Агент 'План техники' запущен (ReAct-режим).")
    print("Примеры запросов:")
    print("- 'Добавь Камаз на 2 уч с 5:00 до 14:00, 1 шт, вывоз снега'")
    print("- 'Покажи все записи'")
    print("- 'Найди записи по участку 5 уч'")
    print("(Введите 'выход', чтобы завершить)")

    chat_history = []

    while True:
        try:
            user_input = input("\n📝 Вы: ").strip()
            if user_input.lower() in ("выход", "exit", "quit"):
                print("👋 До свидания!")
                break

            result = agent_executor.invoke({
                "input": user_input,
                "chat_history": chat_history
            })

            response = result["output"]
            print(f"🤖 Агент: {response}")

            chat_history.extend([
                HumanMessage(content=user_input),
                AIMessage(content=response)
            ])

        except KeyboardInterrupt:
            print("\n👋 Прервано.")
            break
        except Exception as e:
            print(f"❌ Ошибка: {e}")

if __name__ == "__main__":
    main()