from autogen import AssistantAgent, UserProxyAgent, GroupChat, GroupChatManager

# Архитектор
architect = AssistantAgent(
    name="Architect",
    system_message="Ты архитектор ПО. Проанализируй запрос пользователя и, если нужно, задай ему уточняющие вопросы. Затем предложи архитектуру системы.",
)

# Разработчик
developer = AssistantAgent(
    name="Developer",
    system_message="Ты Python-разработчик. Напиши код по архитектуре, предложенной архитектором.",
)

# Тестировщик
tester = AssistantAgent(
    name="Tester",
    system_message="Ты инженер по тестированию. Напиши unit-тесты и проверь работоспособность системы.",
)

# DevOps
devops = AssistantAgent(
    name="DevOps",
    system_message="Ты DevOps-инженер. Настрой Docker, CI/CD и окружение для деплоя приложения.",
)

# UserProxyAgent с возможностью диалога (human-in-the-loop)
user_proxy = UserProxyAgent(
    name="ProductOwner",
    human_input_mode="ALWAYS",  # теперь агент будет задавать тебе вопросы
    system_message="Ты представляешь интересы пользователя и обязан уточнять детали у него, если это необходимо."
)

# Группа агентов
group_chat = GroupChat(
    agents=[user_proxy, architect, developer, tester, devops],
    messages=[],
    max_round=20
)

# Менеджер
manager = GroupChatManager(
    groupchat=group_chat,
    llm_config={"config_list": [{"model": "gpt-4", "api_key": "YOUR_OPENAI_API_KEY"}]},
)

def start_autogen_process(user_input):
    user_proxy.initiate_chat(manager, message=user_input)
