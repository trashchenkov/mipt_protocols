---
theme: default
title: "Протоколы взаимодействия AI-агентов"
titleTemplate: '%s — Разработка и внедрение AI-агентов'
author: "Тращенков Сергей"
info: "Курс «Разработка и внедрение AI-агентов» · МФТИ"
colorSchema: dark
fonts:
  sans: 'SB Sans Display'
  local: 'SB Sans Display'
  weights: '300,400,600'
  italic: false
transition: none
layout: corporate-title-bg
bigQr: true
section: 'Введение'
defaults:
  layout: corporate-default-bg
---

# Протоколы взаимодействия AI-агентов

## Тращенков Сергей

<div class="title-course">Разработка и внедрение AI-агентов · МФТИ</div>

<QrPair big class="title-qr" />

---
section: '§ 1'
---

# Карта взаимодействий

<p class="lead">Помощник для поездки обращается к инструментам, другому агенту и пользовательскому приложению.</p><div class="grid3"><div class="panel"><h3>MCP</h3><p>Инструменты и контекст</p></div><div class="panel"><h3>A2A</h3><p>Задачи удалённому агенту</p></div><div class="panel"><h3>AG-UI / A2UI</h3><p>События и интерфейс</p></div></div><p class="takeaway">ACP связывает редактор и агентный процесс. Skills упаковывают инструкции и файлы.</p>

<!-- Методичка: § 1 -->


---
section: '§ 1'
---

# Кто выполняет инструмент

<p class="lead">Host создаёт MCP-клиента и передаёт модели описания tools. Вычисления инструмента выполняются на сервере.</p><div class="figure"><img class="diagram" src="/diagrams/mcp.svg" /></div>

<!-- Методичка: § 1 -->


---
section: '§ 2'
---

# Три основных примитива MCP

<div class="grid3"><div class="panel"><h3>Tools</h3><p>Операции с аргументами и результатом.<br><br><code>search_rail</code></p></div><div class="panel"><h3>Resources</h3><p>Адресуемые данные для приложения.<br><br><code>course://overview</code></p></div><div class="panel"><h3>Prompts</h3><p>Шаблоны сообщений с параметрами.<br><br><code>prepare_lecture_brief</code></p></div></div><p class="takeaway">Приложение получает ресурсы и prompts, собирает контекст и предоставляет tools модели.</p>

<!-- Методичка: § 2 -->


---
section: '§ 2'
---

# Цикл вызова инструмента

<div class="flow"><div class="panel"><h3>Модель</h3><p>Имя tool и аргументы</p></div><div class="arrow">→</div><div class="panel"><h3>Приложение</h3><p>Отправляет MCP-запрос</p></div><div class="arrow">→</div><div class="panel"><h3>Сервер</h3><p>Выполняет операцию</p></div></div><p class="takeaway">Результат возвращается в ToolMessage. Следующий шаг модели использует эти данные.</p>

<!-- Методичка: § 2 -->


---
section: '§ 2, 6'
---

# Ресурс становится контекстом

<div class="flow"><div class="panel"><h3>Resource</h3><p>Описание курса по URI</p></div><div class="arrow">→</div><div class="panel"><h3>Host</h3><p>Читает содержимое</p></div><div class="arrow">→</div><div class="panel"><h3>Сообщение модели</h3><p>Добавляет нужный текст</p></div></div><p class="takeaway">URI определяет источник данных. Решение о включении данных в запрос принимает приложение.</p>

<!-- Методичка: § 2, 6 -->


---
section: '§ 2, 6'
---

# Prompt задаёт структуру задачи

<div class="grid2"><div class="panel"><h3>Аргументы</h3><p><code>topic_name="mcp"</code><br><br><code>audience="студенты"</code></p></div><div class="panel"><h3>Результат сервера</h3><p>Сообщения с задачей подготовки справки и требованиями к ответу</p></div></div><p class="takeaway">Получение prompt формирует сообщения. Запуск модели выполняется отдельным шагом.</p>

<!-- Методичка: § 2, 6 -->


---
section: '§ 6'
---

# Сборка входа модели

<p class="lead">Описание курса, шаблон справки и инструменты чтения учебных файлов участвуют в одном опыте.</p><div class="figure"><img class="diagram" src="/diagrams/context.svg" /></div>

<!-- Методичка: § 6 -->


---
section: '§ 3'
---

# Редакции MCP и версии SDK

<div class="grid2"><div class="panel"><h3>Спецификация</h3><p><code>2025-11-25</code><br>↓<br><code>2026-07-28</code></p></div><div class="panel"><h3>Python SDK</h3><p><code>v1</code> → <code>v2</code><br><br>Отдельная нумерация библиотеки</p></div></div><p class="takeaway">Обновление протокола и обновление Python API обсуждаем отдельно.</p>

<!-- Методичка: § 3 -->


---
section: '§ 3, 7'
---

# Начало обмена в двух редакциях

| 2025-11-25 | 2026-07-28 |
|---|---|
| initialize и согласование возможностей | Версия и возможности в _meta запроса |
| HTTP-сессия Mcp-Session-Id | Явные идентификаторы объектов в аргументах |
| Сведения при инициализации | server/discover и метаданные запроса |
<p class="takeaway">В ноутбуке вызываем tools/call без предварительного initialize, затем пробуем старое рукопожатие.</p>

<!-- Методичка: § 3, 7 -->


---
section: '§ 3'
---

# Дополнительный ввод: MRTR

<div class="flow"><div class="panel"><h3>Сервер</h3><p>Возвращает input_required</p></div><div class="arrow">→</div><div class="panel"><h3>Приложение</h3><p>Получает ввод пользователя</p></div><div class="arrow">→</div><div class="panel"><h3>Повтор запроса</h3><p>Передаёт inputResponses</p></div></div><p class="takeaway">Дополнительно: subscriptions/listen; Tasks как расширение; Roots/Sampling/Logging — устаревающие возможности.</p>

<!-- Методичка: § 3 -->


---
section: '§ 3, 5'
---

# Python SDK v1 → v2

<div class="grid2"><div class="panel"><h3>Сервер</h3><p><code>FastMCP</code> → <code>MCPServer</code><br><br>Параметры транспорта передаются в run()</p></div><div class="panel"><h3>Клиент</h3><p><code>from mcp import Client</code><br><br>Async context manager держит соединение открытым</p></div></div><p class="takeaway">Декораторы tools, resources и prompts сохраняют знакомую структуру.</p>

<!-- Методичка: § 3, 5 -->


---
section: '§ 3'
---

# MCP в экосистеме LangChain

| Прежнее подключение | Используемое подключение |
|---|---|
| langchain-mcp-adapters | langchain[mcp] |
| MultiServerMCPClient | MCPAdapter |
| get_tools() | await adapter.list_tools() |
<p class="takeaway">MCPAdapter работает как async context manager. Resources и prompts читаем клиентом SDK. Новый namespace находится в beta.</p>

<!-- Методичка: § 3 -->


---
section: '§ 4'
---

# Каталог Туту без вызова модели

<div class="flow"><div class="panel"><h3>Подключение</h3><p>URL публичного MCP</p></div><div class="arrow">→</div><div class="panel"><h3>Обнаружение</h3><p>list_tools()</p></div><div class="arrow">→</div><div class="panel"><h3>Проверка</h3><p>Имена, описания, схемы</p></div></div><p class="takeaway">До создания агента приложение уже знает доступные операции и их параметры.</p>

<!-- Методичка: § 4 -->


---
section: '§ 4.1'
---

# JSON Schema связывает клиента и модель

<div class="grid2"><div class="panel"><h3>Обязательные поля</h3><p>Города, дата и другие условия задаются схемой конкретного инструмента</p></div><div class="panel"><h3>Необязательные поля</h3><p><code>anyOf: [integer, null]</code><br><br>Совместимость проверяется на всём пути к API</p></div></div><p class="takeaway">В примерах включён GigaChat API v2. Исходные схемы MCP передаются без упрощения.</p>

<!-- Методичка: § 4.1 -->


---
section: '§ 4.2'
---

# Сборка и запуск Deep Agent

```python
tools = await adapter.list_tools()
agent = create_deep_agent(model=model, tools=tools)
result = await agent.ainvoke({"messages": messages})
```
<p class="takeaway">Приложение предоставляет инструменты. Во время запуска модель выбирает конкретные вызовы.</p>

<!-- Методичка: § 4.2 -->


---
section: '§ 4.3'
---

# История одного поиска

<div class="flow"><div class="panel"><h3>AIMessage</h3><p>search_rail и аргументы</p></div><div class="arrow">→</div><div class="panel"><h3>ToolMessage</h3><p>Ответ Туту</p></div><div class="arrow">→</div><div class="panel"><h3>AIMessage</h3><p>Поезд, время и цена</p></div></div><p class="takeaway">Проверяем дату, направление, прямой маршрут и соответствие ответа полученным данным.</p>

<!-- Методичка: § 4.3 -->


---
section: '§ 5'
---

# Свой сервер учебных материалов

<div class="grid3"><div class="panel"><h3>Resources</h3><p>Описание курса<br>Сведения о темах</p></div><div class="panel"><h3>Prompt</h3><p>Справка по теме<br>Заданная аудитория</p></div><div class="panel"><h3>Tools</h3><p>Список файлов<br>Чтение начала файла</p></div></div><p class="takeaway">Один сервер демонстрирует все три примитива на данных одной учебной папки.</p>

<!-- Методичка: § 5 -->


---
section: '§ 5.1'
---

# stdio: сервер как дочерний процесс

<div class="flow"><div class="panel"><h3>MCP-клиент</h3><p>Запускает Python</p></div><div class="arrow">→</div><div class="panel"><h3>stdin / stdout</h3><p>Сообщения JSON-RPC</p></div><div class="arrow">→</div><div class="panel"><h3>Сервер</h3><p>Читает учебные файлы</p></div></div><p class="takeaway">Async context manager управляет соединением и завершением дочернего процесса.</p>

<!-- Методичка: § 5.1 -->


---
section: '§ 6'
---

# Полный опыт: справка по теме

<div class="flow"><div class="panel"><h3>До запуска</h3><p>Resource + prompt</p></div><div class="arrow">→</div><div class="panel"><h3>Во время запуска</h3><p>Список файлов → чтение</p></div><div class="arrow">→</div><div class="panel"><h3>После запуска</h3><p>Справка и история</p></div></div><p class="takeaway">На экране видны сформированные входные сообщения и tool calls агента.</p>

<!-- Методичка: § 6 -->


---
section: '§ 7'
---

# HTTP: тот же набор возможностей

<p class="lead">Публикуем тот же сервер через Streamable HTTP и рассматриваем фактический запрос.</p><div class="grid2"><div class="panel"><h3>Запрос</h3><p>Метод tools/call<br>Аргументы операции<br>Версия и возможности в _meta</p></div><div class="panel"><h3>Ответ</h3><p>Результат операции<br>resultType<br>Метаданные сервера</p></div></div><p class="takeaway">Streamable HTTP может передавать SSE. Отдельный старый транспорт HTTP+SSE помечен устаревающим.</p>

<!-- Методичка: § 7 -->


---
section: '§ 8'
---

# Один агент и два MCP-сервера

<div class="figure"><img class="diagram" src="/diagrams/dualmcp.svg" /></div><p class="takeaway">Координатор сам выбирает инструменты поиска поездки и продуктов.</p>

<!-- Методичка: § 8 -->


---
section: '§ 8.1'
---

# Данные между инструментами ВкусВилла

<div class="flow"><div class="panel"><h3>Поиск</h3><p>Названия и id продуктов</p></div><div class="arrow">→</div><div class="panel"><h3>Выбор</h3><p>3–4 позиции перекуса</p></div><div class="arrow">→</div><div class="panel"><h3>Корзина</h3><p>products: id + количество</p></div></div><p class="takeaway">Получаем ссылку на корзину. Оформление и оплата заказа в опыте не выполняются.</p>

<!-- Методичка: § 8.1 -->


---
section: '§ 8.2'
---

# OAuth: разрешение пользователя

<div class="flow"><div class="panel"><h3>Приложение</h3><p>Зарегистрированный OAuth-клиент</p></div><div class="arrow">→</div><div class="panel"><h3>Пользователь</h3><p>Подтверждает доступ</p></div><div class="arrow">→</div><div class="panel"><h3>Сервис</h3><p>Выдаёт ограниченный доступ</p></div></div><p class="takeaway">OAuth 2.0 + PKCE. Персональные сведения требуют согласия; в практике используются публичные операции.</p>

<!-- Методичка: § 8.2 -->


---
section: '§ 8.2'
---

# Практика: расширить свой сервер

<div class="grid2"><div class="panel"><h3>Добавить</h3><p>Tool подсчёта учебных файлов по формату</p></div><div class="panel"><h3>Проверить</h3><p>list_tools → ручной вызов → вызов агентом</p></div></div><p class="takeaway">Доступ к файлам остаётся ограничен папкой data/course.</p>

<!-- Методичка: § 8.2 -->


---
layout: corporate-section-bg
section: '§ 9–17'
---

# Взаимодействие агентов и приложений

<p>Продолжение · 45 минут</p>

<!-- Методичка: § 9–17 -->


---
section: '§ 9, 12'
---

# Два агента с разной ответственностью

<div class="figure"><img class="diagram" src="/diagrams/a2a.svg" /></div><p class="takeaway">Удалённый агент самостоятельно ищет поездку. Координатор объединяет результат с подбором продуктов.</p>

<!-- Методичка: § 9, 12 -->


---
section: '§ 9, 10'
---

# Agent Card: как обратиться к агенту

<div class="grid3"><div class="panel"><h3>Идентичность</h3><p>Имя и описание<br>Версия реализации</p></div><div class="panel"><h3>Интерфейс</h3><p>URL<br>JSONRPC, protocolVersion</p></div><div class="panel"><h3>Возможности</h3><p>Skills<br>Форматы сообщений<br>Capabilities</p></div></div><p class="takeaway">Skills в Agent Card описывают возможности агента. Пакеты SKILL.md рассматриваются отдельно.</p>

<!-- Методичка: § 9, 10 -->


---
section: '§ 10.1'
---

# Сообщение, задача и artifact

<div class="flow"><div class="panel"><h3>SendMessage</h3><p>Запрос пользователя</p></div><div class="arrow">→</div><div class="panel"><h3>Task</h3><p>Статус выполнения</p></div><div class="arrow">→</div><div class="panel"><h3>Artifacts</h3><p>Полученные результаты</p></div></div><p class="takeaway">В примере ждём завершённую задачу. Историю, отмену и все режимы A2A отдельно не сравниваем.</p>

<!-- Методичка: § 10.1 -->


---
section: '§ 10–11'
---

# Одна фабрика — два способа публикации

<div class="grid2"><div class="panel"><h3>Общая логика</h3><p>Deep Agents + GigaChat<br>Один system prompt<br>Одинаковые MCP tools Туту</p></div><div class="panel"><h3>Две реализации</h3><p>Сервер на a2a-sdk<br><br>LangGraph Agent Server</p></div></div><p class="takeaway">Изменяется серверная обвязка. Запрос и клиент остаются одинаковыми.</p>

<!-- Методичка: § 10–11 -->


---
section: '§ 10'
---

# Способ A: a2a-sdk

<div class="flow"><div class="panel"><h3>Agent Card</h3><p>Описываем интерфейс</p></div><div class="arrow">→</div><div class="panel"><h3>AgentExecutor</h3><p>Запускаем общий граф</p></div><div class="arrow">→</div><div class="panel"><h3>TaskUpdater</h3><p>Статус и artifact</p></div></div><p class="takeaway">Код сервера явно показывает перевод A2A-задачи в запуск агента и обратно.</p>

<!-- Методичка: § 10 -->


---
section: '§ 11'
---

# Способ B: LangGraph Agent Server

```python
from agents.travel import travel_graph

graph = travel_graph
```

```json
{"graphs": {"travel": "./servers/agent_server.py:graph"}}
```
<p class="takeaway">langgraph dev предоставляет A2A endpoint и управление запуском. Фабрика держит MCP-соединение открытым.</p>

<!-- Методичка: § 11 -->


---
section: '§ 11.1'
---

# Сравнение одинаковой задачи

| Проверяем | Оба варианта |
|---|---|
| Фабрика агента | Одна и та же функция |
| Источник данных | MCP Туту |
| Вход | Одинаковый запрос о поездке |
| Выход | Завершённая задача и текстовый artifact |
<p class="takeaway">Цена и текст могут отличаться между запросами. Сравниваем выполнение задачи и корректность данных.</p>

<!-- Методичка: § 11.1 -->


---
section: '§ 11.2'
---

# Клиент и сервер: совместимость форматов

<div class="grid2"><div class="panel"><h3>Наблюдение</h3><p>Строгий protobuf-клиент отклоняет дополнительное поле kind у Agent Server</p></div><div class="panel"><h3>Учебный клиент</h3><p>Явный JSON-RPC<br>Читает статус и текстовый artifact обоих серверов</p></div></div><p class="takeaway">Совпадение номера версии в карточке проверяем реальным обменом.</p>

<!-- Методичка: § 11.2 -->


---
section: '§ 12'
---

# Координатор переключается между серверами

<div class="flow"><div class="panel"><h3>travel_agent</h3><p>A2A-запрос о поездке</p></div><div class="arrow">→</div><div class="panel"><h3>MCP ВкусВилла</h3><p>Поиск и ссылка на корзину</p></div><div class="arrow">→</div><div class="panel"><h3>Ответ</h3><p>Поезд + перекус</p></div></div><p class="takeaway">Меняется карточка подключения удалённого агента. Логика координатора сохраняется.</p>

<!-- Методичка: § 12 -->


---
section: '§ 13'
---

# AG-UI: события для приложения

<div class="figure"><img class="diagram" src="/diagrams/agui.svg" /></div><p class="takeaway">Ноутбук играет роль клиента. HTTP-сервер с агентом запускается отдельным процессом.</p>

<!-- Методичка: § 13 -->


---
section: '§ 13.1'
---

# Что показывает поток событий

| Событие | Действие клиента |
|---|---|
| RUN_STARTED | Индикатор работы |
| TOOL_CALL_START / RESULT | Операция и полученные сведения |
| TEXT_MESSAGE_CONTENT | Дописывание текста |
| RUN_FINISHED / ERROR | Завершение или сообщение об ошибке |


<!-- Методичка: § 13.1 -->


---
section: '§ 14'
---

# A2UI: описание интерфейса

<div class="figure"><img class="diagram" src="/diagrams/a2ui.svg" /></div><p class="takeaway">Агент выбирает компоненты из каталога. Клиент отвечает за их отображение и обработку действий.</p>

<!-- Методичка: § 14 -->


---
section: '§ 14.1'
---

# Карточка поезда в JSON

<div class="grid2"><div class="panel"><h3>Структура</h3><p>createSurface<br>updateComponents<br>root → Card → Text</p></div><div class="panel"><h3>Данные</h3><p>Номер поезда<br>Отправление и прибытие<br>Цена</p></div></div><p class="takeaway">В опыте используется v0.9. Ноутбук показывает JSON и статический просмотр базовых компонентов.</p>

<!-- Методичка: § 14.1 -->


---
section: '§ 15'
---

# ACP: редактор и агентный процесс

<div class="figure"><img class="diagram" src="/diagrams/acp.svg" /></div><p class="takeaway">В демонстрации ноутбук выполняет роль минимального клиента. Сетевой порт не требуется.</p>

<!-- Методичка: § 15 -->


---
section: '§ 15'
---

# Сессия ACP по шагам

<div class="flow"><div class="panel"><h3>initialize</h3><p>Версия и возможности</p></div><div class="arrow">→</div><div class="panel"><h3>session/new</h3><p>Рабочий каталог</p></div><div class="arrow">→</div><div class="panel"><h3>session/prompt</h3><p>Запрос пользователя</p></div></div><p class="takeaway">Поступают session/update, затем stopReason=end_turn. stdout содержит JSON-RPC, диагностика идёт в stderr.</p>

<!-- Методичка: § 15 -->


---
section: '§ 16'
---

# Коммерция: участники и разрешения

<div class="flow"><div class="panel"><h3>Пользователь</h3><p>Задаёт условия и согласие</p></div><div class="arrow">→</div><div class="panel"><h3>Агент и продавец</h3><p>Уточняют покупку</p></div><div class="arrow">→</div><div class="panel"><h3>Платёжная сторона</h3><p>Проверяет разрешение</p></div></div><p class="takeaway">Разбор теоретический. Финансовые операции в ноутбуке не выполняются.</p>

<!-- Методичка: § 16 -->


---
section: '§ 16'
---

# Разные части коммерческого процесса

| Протокол | Назначение в обзоре |
|---|---|
| Agentic Commerce Protocol | Checkout между агентом и продавцом |
| UCP | Поиск, корзина, оформление, работа с заказом |
| AP2 | Проверяемые полномочия и разрешение оплаты |
| x402 | Оплата доступа к HTTP-ресурсу |
<p class="takeaway">Agent Client Protocol и Agentic Commerce Protocol имеют одинаковую аббревиатуру ACP.</p>

<!-- Методичка: § 16 -->


---
section: '§ 17'
---

# Контрольные вопросы

<div class="grid2"><div class="panel"><h3>Инструменты и контекст</h3><p>Кто читает resource?<br>Что возвращает prompt?<br>Где исполняется tool?</p></div><div class="panel"><h3>Агенты и приложение</h3><p>Кто выполняет поиск по A2A?<br>Кто рисует A2UI?<br>Что передаёт stdout ACP?</p></div></div>

<!-- Методичка: § 17 -->


---
layout: corporate-section-bg
section: '§ 18'
---

# Skills: дополнительный материал

<p>Инструкции, вспомогательные файлы и проверяемый результат</p>

<!-- Методичка: § 18 -->


---
section: '§ 18'
---

# Папка навыка

<div class="grid2"><div class="panel"><h3>SKILL.md</h3><p>Имя и описание<br>Процедура выполнения<br>Требования</p></div><div class="panel"><h3>Файлы</h3><p>qr_generate.py<br>qr_read.py<br>Метаданные источника</p></div></div><p class="takeaway">Агент выбирает навык по описанию, затем читает подробные инструкции.</p>

<!-- Методичка: § 18 -->


---
section: '§ 18.1–18.2'
---

# QR: результат можно проверить

<div class="figure"><img class="diagram" src="/diagrams/qr.svg" /></div><p class="takeaway">Агент читает SKILL.md, запускает оба скрипта и сравнивает строки. Python независимо повторяет проверку.</p>

<!-- Методичка: § 18.1–18.2 -->


---
section: '§ 18.3'
---

# Загрузка навыка в LangChain

<div class="flow"><div class="panel"><h3>list_skills</h3><p>Краткие описания</p></div><div class="arrow">→</div><div class="panel"><h3>load_skill</h3><p>Полный SKILL.md</p></div><div class="arrow">→</div><div class="panel"><h3>Агент</h3><p>План выполнения</p></div></div><p class="takeaway">Во втором примере показываем выбор и загрузку инструкции. Исполнение скриптов разбирается через Deep Agents.</p>

<!-- Методичка: § 18.3 -->


---
section: '§ 18.1 · README'
---

# QR-зависимости на разных ОС

| ОС | Нативная библиотека |
|---|---|
| Windows x64 | DLL в pyzbar; при ошибке — Visual C++ Runtime 2013 x64 |
| macOS | brew install zbar |
| Debian/Ubuntu | apt-get install libzbar0 |
<p class="takeaway">uv sync устанавливает Python-пакеты. check_env.py --qr проверяет создание и чтение до запуска модели.</p>

<!-- Методичка: § 18.1 · README -->


---
section: '§ 1–15'
---

# Источники спецификаций

<div class="sources">
<div class="source-card"><strong>MCP и инструменты</strong>
<a href="https://modelcontextprotocol.io/specification/2026-07-28">Спецификация MCP</a>
<a href="https://py.sdk.modelcontextprotocol.io/whats-new/">MCP Python SDK v2</a>
<a href="https://docs.langchain.com/oss/python/migrate/langchain-mcp-adapters">MCP в LangChain</a></div>
<div class="source-card"><strong>Агенты и интерфейсы</strong>
<a href="https://a2a-protocol.org/latest/specification/">Agent2Agent</a>
<a href="https://docs.ag-ui.com/">AG-UI</a>
<a href="https://a2ui.org/">A2UI</a>
<a href="https://agentclientprotocol.com/overview/introduction">Agent Client Protocol</a></div></div>

<!-- Методичка: § 1–15 -->


---
section: '§ 16'
---

# Источники коммерческого обзора

<div class="sources">
<div class="source-card"><a href="https://www.agenticcommerce.dev/">Agentic Commerce Protocol</a><a href="https://ucp.dev/">Universal Commerce Protocol</a></div>
<div class="source-card"><a href="https://ap2-protocol.org/">Agent Payments Protocol</a><a href="https://x402.org/">x402</a></div>
</div><p class="takeaway">Блокнот содержит выполняемые примеры и документацию использованных библиотек.</p>

<!-- Методичка: § 16 -->
