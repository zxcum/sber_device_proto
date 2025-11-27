from langchain_core.prompts import PromptTemplate


CHOOSE_OPTION_TEMPLATE = """ 
Пользователь выбирает опцию: 'аналитика' или 'викторина'.
Определи, какую функцию из двух он выберет из его сообщения
Например твои ответы: {{"response": true}} - в случае выбора 'викторина', 
{{"response": false}} - в случае выбора 'аналитика', {{"response": none}}

Сообщение пользователя: {user_text}

"""

choose_option_prompt = PromptTemplate.from_template(
    template=CHOOSE_OPTION_TEMPLATE)


QUESTION_VERIFY_TEMPLATE = """
Возвращай ответ в виде строки со словарем.
В случае если вопрос на логику - Твоя задача проверить правильность ответа пользователя по смыслу на заданный ему вопрос. 
Если задается вопрос про личные данные пользователя, то всегда возвращай {{"response": true}}
Например твои ответы: {{"response": true}} - в случае правильного ответа на вопрос, 
{{"response": false}} - в случае выбора неправильного ответа на вопрос
###
Вопрос: {question_text}
###
Правильный ответ: {right_answer}
###
Ответ пользователя: {user_text}

"""
question_verify_prompt = PromptTemplate.from_template(
    template=QUESTION_VERIFY_TEMPLATE)


YES_NO_TEMPLATE = """ 
У пользователя справшивается согласие на продолжение.
Определи, какую функцию из двух он выберет из его сообщения
Например твои ответы: {{"response": true}} - в случае положительного выбора (да, давай), 
{{"response": false}} - в случае выбора отрицательного выбора, не согласия

Сообщение пользователя: {user_text}

"""
yes_no_prompt = PromptTemplate.from_template(
    template=YES_NO_TEMPLATE)


GETTING_NAME_TEMPLATE = """
Пользователь должен сказать, как его зовут.
Определи из данной фразы пользователя его имя.
Нужно только имя человека с большой буквы
Твои ответы: {{"response": <имя человека>}} - в случае предоставления пользователем имени
{{"response": False}} если пользователь не предоставил свое имя

Сообщение пользователя: {user_text}

"""

getting_name_prompt = PromptTemplate.from_template(
    template=GETTING_NAME_TEMPLATE)

GETTING_AGE_TEMPLATE = """
Пользователь должен сказать его возраст в годах целым числом.
Определи из данной фразы пользователя возраст.
Нужно только возраст человека целым числом
Твои ответы: {{"response": <возраст человека>}} - в случае предоставления пользователем возраста
{{"response": False}} если пользователь не предоставил свой возраст

Сообщение пользователя: {user_text}

"""

getting_age_prompt = PromptTemplate.from_template(
    template=GETTING_AGE_TEMPLATE)


CHOOSE_THEME_TEMPLATE = """ 
Пользователь выбирает тему для викторины.
Определи, выбрал ли он одну из доступных тем: {themes}
Структура твоих ответов: {{"response": true, "theme": "выбранная тема из списка"}}
или {{"response": false}} если тема не подходит. "
###
Сообщение пользователя: {user_text}

"""

choose_theme_prompt = PromptTemplate.from_template(
    template=CHOOSE_THEME_TEMPLATE)
