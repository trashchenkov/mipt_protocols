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

# Какой протокол для какой задачи

<p class="lead">Задача примера — найти поезд и подобрать продукты в дорогу.</p><div class="grid3"><div class="panel"><h3>MCP</h3><p>Вызов инструментов<br>Чтение ресурсов<br>Получение промптов</p></div><div class="panel"><h3>A2A</h3><p>Отправка задачи<br>другому агенту<br>и получение результата</p></div><div class="panel"><h3>AG-UI / A2UI</h3><p>AG-UI: события агента<br><br>A2UI: компоненты интерфейса</p></div></div><p class="takeaway">ACP передаёт запросы редактора агенту. Навык (Skill) содержит инструкции и вспомогательные файлы.</p>

<!-- Раздел блокнота: § 1 -->


---
section: '§ 1'
---

# MCP: приложение, клиент и сервер

<p class="lead">Приложение (host) создаёт MCP-клиента и передаёт модели описания инструментов. Клиент отправляет вызов серверу, сервер выполняет операцию.</p><div class="figure"><img class="diagram" src="/diagrams/mcp.svg" /></div>

<!-- Раздел блокнота: § 1 -->


---
section: '§ 2'
---

# MCP: инструменты, ресурсы и промпты

<div class="grid3"><div class="panel"><h3>Tools</h3><p>Вызываемые операции с аргументами и результатом.<br><br><code>search_rail</code></p></div><div class="panel"><h3>Resources</h3><p>Данные, которые клиент читает по URI.<br><br><code>course://overview</code></p></div><div class="panel"><h3>Prompts</h3><p>Шаблоны сообщений с параметрами.<br><br><code>prepare_lecture_brief</code></p></div></div><p class="takeaway">В примере клиент получает все три: список инструментов, текст ресурса и сообщения из промпта.</p>

<!-- Раздел блокнота: § 2 -->


---
section: '§ 2'
---

# MCP: как вызывается инструмент

<div class="flow"><div class="panel"><h3>Модель</h3><p>Выбирает инструмент<br>и задаёт аргументы</p></div><div class="arrow">→</div><div class="panel"><h3>Приложение</h3><p>Отправляет MCP-запрос</p></div><div class="arrow">→</div><div class="panel"><h3>Сервер</h3><p>Выполняет операцию</p></div></div><p class="takeaway">В LangChain результат записывается в ToolMessage. Модель получает его при следующем вызове.</p>

<!-- Раздел блокнота: § 2 -->


---
section: '§ 2, 6'
---

# MCP: чтение ресурса по URI

<div class="flow"><div class="panel"><h3>Resource</h3><p>Описание курса по URI</p></div><div class="arrow">→</div><div class="panel"><h3>Host</h3><p>Читает содержимое</p></div><div class="arrow">→</div><div class="panel"><h3>Запрос к модели</h3><p>Содержит текст ресурса</p></div></div><p class="takeaway">Клиент читает описание курса по URI course://overview. Приложение добавляет этот текст в запрос к модели.</p>

<!-- Раздел блокнота: § 2, 6 -->


---
section: '§ 2, 6'
---

# MCP: получение шаблона промпта

<div class="grid2"><div class="panel"><h3>Аргументы</h3><p><code>topic_name="mcp"</code><br><br><code>audience="студенты"</code></p></div><div class="panel"><h3>Результат сервера</h3><p>Сообщения с темой справки, аудиторией и требованиями к ответу</p></div></div><p class="takeaway">Сервер подставляет аргументы в шаблон и возвращает сообщения. Приложение передаёт их модели.</p>

<!-- Раздел блокнота: § 2, 6 -->


---
section: '§ 6'
---

# MCP: ресурс и промпт в запросе к модели

<p class="lead">Приложение передаёт модели описание курса, промпт справки и описания инструментов чтения файлов.</p><div class="figure"><img class="diagram" src="/diagrams/context.svg" /></div>

<!-- Раздел блокнота: § 6 -->


---
section: '§ 3'
---

# MCP: версии спецификации и Python SDK

<div class="grid2"><div class="panel"><h3>Спецификация</h3><p><code>2025-11-25</code><br>↓<br><code>2026-07-28</code></p></div><div class="panel"><h3>Python SDK</h3><p><code>v1</code> → <code>v2</code><br><br>Версия Python-библиотеки</p></div></div><p class="takeaway">Спецификация задаёт формат обмена. Версия SDK определяет Python API для этого обмена.</p>

<!-- Раздел блокнота: § 3 -->


---
section: '§ 3, 7'
---

# MCP: начало обмена до и после обновления

| 2025-11-25 | 2026-07-28 |
|---|---|
| initialize и согласование возможностей | Версия и возможности в _meta запроса |
| HTTP-сессия Mcp-Session-Id | Явные идентификаторы объектов в аргументах |
| Сведения при инициализации | server/discover и метаданные запроса |
<p class="takeaway">В блокноте отправляем tools/call без initialize, затем проверяем подключение клиента предыдущей редакции.</p>

<!-- Раздел блокнота: § 3, 7 -->


---
section: '§ 3'
---

# MCP: запрос дополнительного ввода (MRTR)

<div class="flow"><div class="panel"><h3>Сервер</h3><p>Возвращает input_required</p></div><div class="arrow">→</div><div class="panel"><h3>Приложение</h3><p>Получает ввод пользователя</p></div><div class="arrow">→</div><div class="panel"><h3>Повтор запроса</h3><p>Передаёт inputResponses</p></div></div><p class="takeaway">Подписки: subscriptions/listen. Tasks вынесены в расширение. Roots, Sampling и Logging помечены устаревающими.</p>

<!-- Раздел блокнота: § 3 -->


---
section: '§ 3, 5'
---

# MCP Python SDK: переход с v1 на v2

<div class="grid2"><div class="panel"><h3>Сервер</h3><p><code>FastMCP</code> → <code>MCPServer</code><br><br>Параметры транспорта передаются в run()</p></div><div class="panel"><h3>Клиент</h3><p><code>from mcp import Client</code><br><br>async with сохраняет соединение до выхода из блока</p></div></div><p class="takeaway">На сервере используем декораторы для tools, resources и prompts; на клиенте — async with Client(...).</p>

<!-- Раздел блокнота: § 3, 5 -->


---
section: '§ 3'
---

# MCP в LangChain: новый адаптер

| Прежнее подключение | Используемое подключение |
|---|---|
| langchain-mcp-adapters | langchain[mcp] |
| MultiServerMCPClient | MCPAdapter |
| get_tools() | await adapter.list_tools() |
<p class="takeaway">MCPAdapter подключаем через async with. Ресурсы и промпты читаем клиентом MCP SDK. Модуль langchain.mcp имеет статус beta.</p>

<!-- Раздел блокнота: § 3 -->


---
section: '§ 4'
---

# MCP Туту: список доступных инструментов

<div class="flow"><div class="panel"><h3>Подключение</h3><p>URL MCP-сервера Туту</p></div><div class="arrow">→</div><div class="panel"><h3>Список инструментов</h3><p>list_tools()</p></div><div class="arrow">→</div><div class="panel"><h3>Проверка</h3><p>Имена, описания, схемы</p></div></div><p class="takeaway">Вызываем list_tools() и смотрим имена, описания и схемы аргументов до запуска агента.</p>

<!-- Раздел блокнота: § 4 -->


---
section: '§ 4.1'
---

# MCP Туту: параметры инструмента в JSON Schema

<div class="grid2"><div class="panel"><h3>Описание аргументов</h3><p>Схема задаёт имена и типы аргументов. Список required указывает обязательные поля.</p></div><div class="panel"><h3>Допустимое значение null</h3><p><code>anyOf: [integer, null]</code><br><br>API модели должен принимать такую схему</p></div></div><p class="takeaway">GigaChat API v2 принимает используемые схемы с nullable-полями. Передаём схемы, полученные от MCP-сервера.</p>

<!-- Раздел блокнота: § 4.1 -->


---
section: '§ 4.2'
---

# MCP Туту: подключение к Deep Agent

```python
tools = await adapter.list_tools()
agent = create_deep_agent(model=model, tools=tools)
result = await agent.ainvoke({"messages": messages})
```
<p class="takeaway">Передаём инструменты из MCPAdapter в create_deep_agent. Модель выбирает инструмент и задаёт аргументы вызова.</p>

<!-- Раздел блокнота: § 4.2 -->


---
section: '§ 4.3'
---

# MCP Туту: вызов и результат в истории

<div class="flow"><div class="panel"><h3>AIMessage</h3><p>search_rail и аргументы</p></div><div class="arrow">→</div><div class="panel"><h3>ToolMessage</h3><p>Ответ Туту</p></div><div class="arrow">→</div><div class="panel"><h3>AIMessage</h3><p>Поезд, время и цена</p></div></div><p class="takeaway">Сопоставляем ответ агента с ToolMessage: дату, направление, отсутствие пересадок, время и цену.</p>

<!-- Раздел блокнота: § 4.3 -->


---
section: '§ 5'
---

# MCP: сервер для чтения учебных материалов

<div class="grid3"><div class="panel"><h3>Resources</h3><p>Описание курса<br>Сведения о темах</p></div><div class="panel"><h3>Prompt</h3><p>Справка по теме<br>Заданная аудитория</p></div><div class="panel"><h3>Tools</h3><p>Список файлов<br>Чтение начала файла</p></div></div><p class="takeaway">Сервер читает файлы из data/course и предоставляет tools, resources и prompts для подготовки справки.</p>

<!-- Раздел блокнота: § 5 -->


---
section: '§ 5.1'
---

# MCP по stdio: запуск сервера из клиента

<div class="flow"><div class="panel"><h3>MCP-клиент</h3><p>Запускает Python</p></div><div class="arrow">→</div><div class="panel"><h3>stdin / stdout</h3><p>Сообщения JSON-RPC</p></div><div class="arrow">→</div><div class="panel"><h3>Сервер</h3><p>Читает учебные файлы</p></div></div><p class="takeaway">Вход в async with Client(...) запускает сервер. Выход из блока закрывает соединение и завершает процесс.</p>

<!-- Раздел блокнота: § 5.1 -->


---
section: '§ 6'
---

# MCP: агент готовит справку по теме

<div class="flow"><div class="panel"><h3>До запуска</h3><p>Resource + prompt</p></div><div class="arrow">→</div><div class="panel"><h3>Во время запуска</h3><p>Список файлов → чтение</p></div><div class="arrow">→</div><div class="panel"><h3>После запуска</h3><p>Справка и история</p></div></div><p class="takeaway">В блокноте выводим сообщения перед вызовом модели, вызовы инструментов и готовую справку.</p>

<!-- Раздел блокнота: § 6 -->


---
section: '§ 7'
---

# MCP по HTTP: запрос и ответ

<p class="lead">Запускаем сервер учебных материалов по Streamable HTTP. В блокноте смотрим отправленный запрос и ответ.</p><div class="grid2"><div class="panel"><h3>Запрос</h3><p>Метод tools/call<br>Аргументы операции<br>Версия и возможности в _meta</p></div><div class="panel"><h3>Ответ</h3><p>Результат операции<br>resultType<br>Метаданные сервера</p></div></div><p class="takeaway">Streamable HTTP может передавать SSE. Отдельный старый транспорт HTTP+SSE помечен устаревающим.</p>

<!-- Раздел блокнота: § 7 -->


---
section: '§ 8'
---

# MCP: один агент с Туту и ВкусВиллом

<div class="figure"><img class="diagram" src="/diagrams/dualmcp.svg" /></div><p class="takeaway">Один Deep Agent получает инструменты обоих MCP-серверов и выбирает вызовы для поиска поезда и продуктов.</p>

<!-- Раздел блокнота: § 8 -->


---
section: '§ 8.1'
---

# MCP ВкусВилла: от поиска к корзине

<div class="flow"><div class="panel"><h3>Поиск</h3><p>Названия и id продуктов</p></div><div class="arrow">→</div><div class="panel"><h3>Выбор</h3><p>3–4 позиции перекуса</p></div><div class="arrow">→</div><div class="panel"><h3>Корзина</h3><p>products: id + количество</p></div></div><p class="takeaway">Результат — ссылка на корзину с выбранными продуктами. Оформление и оплату оставляем пользователю.</p>

<!-- Раздел блокнота: § 8.1 -->


---
section: '§ 8.2'
---

# MCP и OAuth: доступ к личным данным

<div class="flow"><div class="panel"><h3>Приложение</h3><p>Начинает авторизацию<br>с PKCE</p></div><div class="arrow">→</div><div class="panel"><h3>Пользователь</h3><p>Подтверждает доступ</p></div><div class="arrow">→</div><div class="panel"><h3>Сервис</h3><p>Выдаёт токен<br>доступа</p></div></div><p class="takeaway">Личный кабинет требует OAuth-авторизации пользователя. В примерах вызываем публичные операции Туту и ВкусВилла.</p>

<!-- Раздел блокнота: § 8.2 -->


---
section: '§ 8.2'
---

# Практика MCP: добавить инструмент на сервер

<div class="grid2"><div class="panel"><h3>Добавить</h3><p>Инструмент подсчёта учебных файлов по расширению</p></div><div class="panel"><h3>Проверить</h3><p>list_tools → ручной вызов → вызов агентом</p></div></div><p class="takeaway">Доступ к файлам остаётся ограничен папкой data/course.</p>

<!-- Раздел блокнота: § 8.2 -->


---
layout: corporate-section-bg
section: '§ 9–17'
---

# A2A, AG-UI, A2UI и ACP

<p>Задачи между агентами, события для приложения и работа с редактором · 45 минут</p>

<!-- Раздел блокнота: § 9–17 -->


---
section: '§ 9, 12'
---

# A2A: координатор и агент поездок

<div class="figure"><img class="diagram" src="/diagrams/a2a.svg" /></div><p class="takeaway">Координатор отправляет задачу по A2A. Агент поездок вызывает MCP Туту и возвращает результат; координатор подбирает продукты через MCP ВкусВилла.</p>

<!-- Раздел блокнота: § 9, 12 -->


---
section: '§ 9, 10'
---

# A2A: адрес и возможности агента в Agent Card

<div class="grid3"><div class="panel"><h3>Описание агента</h3><p>Имя и назначение<br>Версия реализации</p></div><div class="panel"><h3>Интерфейс</h3><p>URL<br>JSONRPC, protocolVersion</p></div><div class="panel"><h3>Возможности</h3><p>Skills<br>Форматы сообщений<br>Capabilities</p></div></div><p class="takeaway">Поле skills перечисляет задачи агента. Формат SKILL.md с инструкциями разбираем в дополнительном разделе.</p>

<!-- Раздел блокнота: § 9, 10 -->


---
section: '§ 10.1'
---

# A2A: сообщение, задача и результат

<div class="flow"><div class="panel"><h3>SendMessage</h3><p>Запрос пользователя</p></div><div class="arrow">→</div><div class="panel"><h3>Task</h3><p>Статус выполнения</p></div><div class="arrow">→</div><div class="panel"><h3>Artifacts</h3><p>Полученные результаты</p></div></div><p class="takeaway">В ответе проверяем статус completed и читаем текст поездки из artifacts.</p>

<!-- Раздел блокнота: § 10.1 -->


---
section: '§ 10–11'
---

# A2A: два сервера с одним агентом

<div class="grid2"><div class="panel"><h3>Общая логика</h3><p>Deep Agents + GigaChat<br>Один системный промпт<br>Одни инструменты Туту по MCP</p></div><div class="panel"><h3>Две реализации</h3><p>Сервер на a2a-sdk<br><br>LangGraph Agent Server</p></div></div><p class="takeaway">Оба сервера запускают агента из agents/travel.py. Отправляем им одинаковый запрос одним клиентом.</p>

<!-- Раздел блокнота: § 10–11 -->


---
section: '§ 10'
---

# A2A, способ A: сервер на a2a-sdk

<div class="flow"><div class="panel"><h3>Agent Card</h3><p>Описываем интерфейс</p></div><div class="arrow">→</div><div class="panel"><h3>AgentExecutor</h3><p>Запускаем общий граф</p></div><div class="arrow">→</div><div class="panel"><h3>TaskUpdater</h3><p>Статус и результат</p></div></div><p class="takeaway">AgentExecutor получает A2A-запрос, вызывает агента и через TaskUpdater возвращает статус и результат.</p>

<!-- Раздел блокнота: § 10 -->


---
section: '§ 11'
---

# A2A, способ B: LangGraph Agent Server

```python
from agents.travel import travel_graph

graph = travel_graph
```

```json
{"graphs": {"travel": "./servers/agent_server.py:graph"}}
```
<p class="takeaway">langgraph dev запускает сервер с A2A-адресом для графа travel. Соединение агента с MCP Туту открыто во время выполнения.</p>

<!-- Раздел блокнота: § 11 -->


---
section: '§ 11.1'
---

# A2A: сравнение двух серверов

| Проверяем | Оба варианта |
|---|---|
| Создание агента | Одна и та же функция |
| Источник данных | MCP Туту |
| Вход | Одинаковый запрос о поездке |
| Выход | Завершённая задача и текст в artifacts |
<p class="takeaway">Для обоих ответов проверяем дату, направление и соответствие данным Туту. Цена и формулировки могут меняться между запросами.</p>

<!-- Раздел блокнота: § 11.1 -->


---
section: '§ 11.2'
---

# A2A: совместимость клиента и сервера

<div class="grid2"><div class="panel"><h3>Наблюдение</h3><p>Клиент a2a-sdk с protobuf-моделями отклоняет дополнительное поле kind в ответе Agent Server</p></div><div class="panel"><h3>Учебный клиент</h3><p>JSON-RPC через HTTP<br>Статус задачи и текст из artifacts</p></div></div><p class="takeaway">Поэтому в блокноте используем JSON-RPC-клиент, который принимает ответы обоих серверов.</p>

<!-- Раздел блокнота: § 11.2 -->


---
section: '§ 12'
---

# A2A и MCP: поездка и продукты в одном запросе

<div class="flow"><div class="panel"><h3>travel_agent</h3><p>A2A-запрос о поездке</p></div><div class="arrow">→</div><div class="panel"><h3>MCP ВкусВилла</h3><p>Поиск и ссылка на корзину</p></div><div class="arrow">→</div><div class="panel"><h3>Ответ</h3><p>Поезд и продукты</p></div></div><p class="takeaway">Повторяем запрос с адресом второго A2A-сервера. Координатор по-прежнему получает поездку и ссылку на корзину.</p>

<!-- Раздел блокнота: § 12 -->


---
section: '§ 13'
---

# AG-UI: события для приложения

<div class="figure"><img class="diagram" src="/diagrams/agui.svg" /></div><p class="takeaway">Ячейка блокнота запускает HTTP-сервер отдельным процессом, отправляет запрос и читает SSE-события.</p>

<!-- Раздел блокнота: § 13 -->


---
section: '§ 13.1'
---

# AG-UI: как клиент отображает события

| Событие | Действие клиента |
|---|---|
| RUN_STARTED | Индикатор работы |
| TOOL_CALL_START / TOOL_CALL_RESULT | Название инструмента и его результат |
| TEXT_MESSAGE_CONTENT | Добавление фрагмента ответа |
| RUN_FINISHED / RUN_ERROR | Завершение или сообщение об ошибке |


<!-- Раздел блокнота: § 13.1 -->


---
section: '§ 14'
---

# A2UI: описание интерфейса

<div class="figure"><img class="diagram" src="/diagrams/a2ui.svg" /></div><p class="takeaway">Агент возвращает JSON с компонентами из каталога. Клиент строит по нему интерфейс.</p>

<!-- Раздел блокнота: § 14 -->


---
section: '§ 14.1'
---

# A2UI: от JSON к карточке поезда

<div class="grid2"><div class="panel"><h3>Структура</h3><p>createSurface<br>updateComponents<br>root → Card → Text</p></div><div class="panel"><h3>Данные</h3><p>Номер поезда<br>Отправление и прибытие<br>Цена</p></div></div><p class="takeaway">Используем A2UI v0.9. В блокноте выводим JSON и строим из него статическую карточку поезда.</p>

<!-- Раздел блокнота: § 14.1 -->


---
section: '§ 15'
---

# ACP: редактор и агентный процесс

<div class="figure"><img class="diagram" src="/diagrams/acp.svg" /></div><p class="takeaway">Ячейка блокнота запускает ACP-сервер и обменивается с ним JSON-RPC через stdin и stdout.</p>

<!-- Раздел блокнота: § 15 -->


---
section: '§ 15'
---

# ACP: создание сессии и отправка запроса

<div class="flow"><div class="panel"><h3>initialize</h3><p>Версия и возможности</p></div><div class="arrow">→</div><div class="panel"><h3>session/new</h3><p>Рабочий каталог</p></div><div class="arrow">→</div><div class="panel"><h3>session/prompt</h3><p>Запрос пользователя</p></div></div><p class="takeaway">Агент присылает session/update и завершает ответ с stopReason=end_turn. JSON-RPC идёт в stdout, логи — в stderr.</p>

<!-- Раздел блокнота: § 15 -->


---
section: '§ 16'
---

# Покупка через агента: участники и согласие

<div class="flow"><div class="panel"><h3>Пользователь</h3><p>Выбирает товар<br>и разрешает покупку</p></div><div class="arrow">→</div><div class="panel"><h3>Агент и продавец</h3><p>Уточняют покупку</p></div><div class="arrow">→</div><div class="panel"><h3>Платёжный сервис</h3><p>Проверяет разрешение</p></div></div><p class="takeaway">Обзор протоколов: как передать заказ и подтвердить согласие на оплату. В блокноте платежей нет.</p>

<!-- Раздел блокнота: § 16 -->


---
section: '§ 16'
---

# Протоколы покупки и оплаты

| Протокол | Назначение |
|---|---|
| Agentic Commerce Protocol | Данные оформления заказа между агентом и продавцом |
| UCP | Поиск, корзина, оформление, работа с заказом |
| AP2 | Подтверждения полномочий агента и согласия на оплату |
| x402 | Оплата доступа к HTTP-ресурсу |
<p class="takeaway">Agent Client Protocol и Agentic Commerce Protocol имеют одинаковую аббревиатуру ACP.</p>

<!-- Раздел блокнота: § 16 -->


---
section: '§ 17'
---

# Контрольные вопросы

<div class="grid2"><div class="panel"><h3>Инструменты и контекст</h3><p>Кто читает ресурс?<br>Что возвращает промпт?<br>Где выполняется инструмент?</p></div><div class="panel"><h3>Агенты и приложение</h3><p>Кто выполняет поиск по A2A?<br>Кто отображает компоненты A2UI?<br>Что передаёт stdout ACP?</p></div></div>

<!-- Раздел блокнота: § 17 -->


---
section: 'ДЗ'
---

# Домашнее задание: расширить MCP-сервер

<div class="grid2"><div class="panel"><h3>Реализовать</h3><p>Инструмент подсчёта файлов<br>Ресурс статистики<br>Промпт обзора для аудитории</p></div><div class="panel"><h3>Проверить и сдать</h3><p>Три списка MCP и прямые вызовы<br>Вызов инструмента агентом<br>Сервер + homework.ipynb</p></div></div><p class="takeaway">Условия и критерии: HOMEWORK.md. Дополнительно — опубликовать агента по A2A.</p>

<!-- Раздел блокнота: ДЗ -->


---
layout: corporate-section-bg
section: '§ 18'
---

# Skills: дополнительный материал

<p>Пример навыка: создать QR-код, прочитать его и проверить содержимое</p>

<!-- Раздел блокнота: § 18 -->


---
section: '§ 18'
---

# Skills: содержимое папки навыка

<div class="grid2"><div class="panel"><h3>SKILL.md</h3><p>name: qr-code — имя папки<br>Описание и инструкция<br>Автор и источник в metadata</p></div><div class="panel"><h3>Файлы</h3><p>scripts/qr_generate.py<br>scripts/qr_read.py</p></div></div><p class="takeaway">По имени и описанию агент выбирает навык, читает SKILL.md и выполняет указанные шаги.</p>

<!-- Раздел блокнота: § 18 -->


---
section: '§ 18.1–18.2'
---

# Skills: создание и чтение QR-кода

<div class="figure"><img class="diagram" src="/diagrams/qr.svg" /></div><p class="takeaway">Агент создаёт QR-код и читает его обратно. В отдельной ячейке проверяем, что декодированная строка совпадает с исходной.</p>

<!-- Раздел блокнота: § 18.1–18.2 -->


---
section: '§ 18.3'
---

# Skills: поиск и загрузка в LangChain

<div class="flow"><div class="panel"><h3>list_skills</h3><p>Краткие описания</p></div><div class="arrow">→</div><div class="panel"><h3>load_skill</h3><p>Полный SKILL.md</p></div><div class="arrow">→</div><div class="panel"><h3>Агент</h3><p>План выполнения</p></div></div><p class="takeaway">В этом примере агент находит навык через list_skills и читает SKILL.md через load_skill. Запуск скриптов показан в предыдущем примере с Deep Agents.</p>

<!-- Раздел блокнота: § 18.3 -->


---
section: '§ 18.1 · README'
---

# Skills: установка QR-библиотек на разных ОС

| ОС | Нативная библиотека |
|---|---|
| Windows x64 | DLL в pyzbar; при ошибке — Visual C++ Runtime 2013 x64 |
| macOS | brew install zbar |
| Debian/Ubuntu | apt-get install libzbar0 |
<p class="takeaway">После uv sync запускаем check_env.py --qr: он создаёт и читает QR-код, проверяя доступность zbar.</p>

<!-- Раздел блокнота: § 18.1 · README -->


---
section: '§ 1–15'
---

# Спецификации и документация

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

<!-- Раздел блокнота: § 1–15 -->


---
section: '§ 16'
---

# Документация протоколов покупки и оплаты

<div class="sources">
<div class="source-card"><a href="https://www.agenticcommerce.dev/">Agentic Commerce Protocol</a><a href="https://ucp.dev/">Universal Commerce Protocol</a></div>
<div class="source-card"><a href="https://ap2-protocol.org/">Agent Payments Protocol</a><a href="https://x402.org/">x402</a></div>
</div><p class="takeaway">Ссылки на документацию также приведены в блокноте.</p>

<!-- Раздел блокнота: § 16 -->
