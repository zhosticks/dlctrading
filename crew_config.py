from crewai import Agent, Task, Crew
from langchain_openai import ChatOpenAI
import os

# Создаём LLM, совместимый с sk-proj ключом
llm = ChatOpenAI(
    model="gpt-4",
    temperature=0.3,
    openai_api_key=os.getenv("OPENAI_API_KEY"),
    openai_api_base="https://api.openai.com/v1"  # Явно указываем endpoint
)

# Агентская команда
architect = Agent(
    role="Архитектор",
    goal="Разработать архитектуру системы",
    backstory="Финтех-архитектор с опытом построения масштабируемых решений",
    llm=llm
)

developer = Agent(
    role="Разработчик",
    goal="Реализовать архитектуру системы на Python",
    backstory="Backend-инженер, пишущий телеграм-ботов и API",
    llm=llm
)

tester = Agent(
    role="Тестировщик",
    goal="Покрыть код тестами",
    backstory="Обеспечивает стабильность и покрытие unit-тестами",
    llm=llm
)

strategist = Agent(
    role="Стратег",
    goal="Построить стратегию на основе рисков и горизонта",
    backstory="Финансовый аналитик по крипте и фондовому рынку",
    llm=llm
)

analyst = Agent(
    role="Аналитик",
    goal="Добавить рыночные данные и индикаторы",
    backstory="Следит за новостями, рынками, RSI и MACD",
    llm=llm
)

risk_manager = Agent(
    role="Риск-менеджер",
    goal="Ограничить потери, задать лимиты",
    backstory="Контролирует просадки и допустимые риски",
    llm=llm
)

executor = Agent(
    role="Исполнитель сделок",
    goal="Интегрировать торговлю с биржей",
    backstory="Обеспечивает исполнение сигналов через API",
    llm=llm
)

auto_deployer = Agent(
    role="Авто-деплой",
    goal="Автоматически задеплоить систему",
    backstory="DevOps инженер, работает с Docker и CI/CD",
    llm=llm
)

dialog_agent = Agent(
    role="Диалоговый агент",
    goal="Сообщить результат, спросить уточнение при необходимости",
    backstory="Управляет интерфейсом общения",
    llm=llm
)

# Построение задач
def build_tasks(user_input):
    return [
        Task(
            description=f"На основе запроса '{user_input}' предложи архитектуру",
            expected_output="Архитектура системы или запрос уточнения",
            agent=architect
        ),
        Task(
            description="Реализуй архитектуру на Python",
            expected_output="Готовый код или комментарий по затруднению",
            agent=developer
        ),
        Task(
            description="Напиши unit-тесты",
            expected_output="Юнит-тесты",
            agent=tester
        ),
        Task(
            description="Создай стратегию по входным параметрам",
            expected_output="Описанная стратегия или вопрос пользователю",
            agent=strategist
        ),
        Task(
            description="Добавь рыночные данные и технический анализ",
            expected_output="Индикаторы RSI/MACD и прогноз",
            agent=analyst
        ),
        Task(
            description="Проверь риск и предложи ограничения",
            expected_output="Стоп-лоссы и риск-параметры",
            agent=risk_manager
        ),
        Task(
            description="Напиши код для исполнения сделок через API",
            expected_output="Код отправки ордеров",
            agent=executor
        ),
        Task(
            description="Собери Docker и CI/CD пайплайн",
            expected_output="Dockerfile и .github/workflows",
            agent=auto_deployer
        ),
        Task(
            description="Выведи результат пользователю",
            expected_output="Сводка и рекомендации",
            agent=dialog_agent
        ),
    ]

crew = Crew(
    agents=[
        architect, developer, tester, strategist, analyst,
        risk_manager, executor, auto_deployer, dialog_agent
    ],
    tasks=[],
    verbose=True
)

def run_crew(user_input: str):
    try:
        crew.tasks = build_tasks(user_input)
        return crew.kickoff(inputs={"user_input": user_input})
    except Exception as e:
        return f"❌ Ошибка при работе команды: {e}"
