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

<div class="grid4"><div class="panel"><h3>MCP</h3><p>Агент вызывает функцию сервиса: поиск поездов или продуктов.</p></div><div class="panel"><h3>A2A</h3><p>Один агент поручает задачу другому и получает результат.</p></div><div class="panel"><h3>AG-UI</h3><p>Приложение получает ход работы агента и показывает поиск, вызовы и части ответа.</p></div><div class="panel"><h3>A2UI</h3><p>Приложение строит экран по описанию агента: карточку поезда с временем и ценой.</p></div></div><p class="takeaway">ACP: приложение-клиент создаёт сессии, отправляет агенту запросы и получает ответы и уведомления.</p>

<!-- Раздел блокнота: § 1 -->


---
section: '§ 1'
---

# MCP: хост, клиент и сервер

<p class="lead">Хост (приложение) запускает агента и создаёт MCP-клиент для каждого сервера. Агент выбирает действие; клиент передаёт запрос и получает результат.</p><div class="figure"><img class="diagram" src="/diagrams/mcp.svg" /></div>

<!-- Раздел блокнота: § 1 -->


---
section: '§ 2'
---

# MCP: инструменты, ресурсы и промпты

<div class="grid3"><div class="panel"><h3>Tools: инструменты</h3><p>Функции, которые клиент вызывает с аргументами.<br><br><code>search_rail</code>: поиск поездов</p></div><div class="panel"><h3>Resources: ресурсы</h3><p>Данные с адресом URI, например описание курса.<br><br><code>course://overview</code></p></div><div class="panel"><h3>Prompts: промпты</h3><p>Шаблоны сообщений, например запрос справки по теме.<br><br><code>prepare_lecture_brief</code></p></div></div><p class="takeaway">Сервер предоставляет три вида возможностей. Хост (приложение) получает ресурсы и промпты через MCP-клиент; агент выбирает вызов инструмента.</p>

<!-- Раздел блокнота: § 2 -->


---
section: '§ 2'
---

# MCP: как вызывается инструмент

<div class="figure"><img class="diagram" src="/diagrams/mcp.svg" /></div><p class="takeaway">Хост передаёт выбранный агентом вызов MCP-клиенту, а результат возвращает агенту как ToolMessage. Агент продолжает решение задачи с полученными данными.</p>

<!-- Раздел блокнота: § 2 -->


---
section: '§ 2, 6'
---

# MCP: чтение ресурса по URI

<div class="flow"><div class="panel"><h3>Resource</h3><p>Описание курса по URI</p></div><div class="arrow">→</div><div class="panel"><h3>Хост</h3><p>Читает через<br>MCP-клиент</p></div><div class="arrow">→</div><div class="panel"><h3>Запрос к модели</h3><p>Содержит текст ресурса</p></div></div><p class="takeaway">URI — адрес ресурса в MCP. Клиент читает course://overview, а хост добавляет полученное описание курса в запрос к модели.</p>

<!-- Раздел блокнота: § 2, 6 -->


---
section: '§ 2, 6'
---

# MCP: получение шаблона промпта

<div class="grid2"><div class="panel"><h3>Аргументы</h3><p><code>topic_name="mcp"</code><br><br><code>audience="студенты"</code></p></div><div class="panel"><h3>Результат сервера</h3><p>«Подготовь справку по MCP для студентов; укажи назначение и пример применения»</p></div></div><p class="takeaway">Сервер подставляет тему и аудиторию в шаблон. Для получения ответа хост отдельно вызывает модель с этими сообщениями.</p>

<!-- Раздел блокнота: § 2, 6 -->


---
section: '§ 6'
---

# MCP: ресурс и промпт в запросе к модели

<p class="lead">Хост (приложение) собирает контекст: описание курса из resource, задачу из prompt и инструменты для чтения файлов.</p><div class="figure"><img class="diagram" src="/diagrams/context.svg" /></div>

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

| Что передаётся | 2025-11-25 | 2026-07-28 |
|---|---|---|
| Версия и возможности | В отдельном initialize | В _meta каждого запроса |
| Идентификаторы состояния | HTTP-сессия Mcp-Session-Id | Идентификаторы объектов в аргументах |
| Сведения о сервере | В ответе на initialize | Через server/discover |
<p class="takeaway">В блокноте отправляем tools/call без initialize, затем проверяем подключение клиента предыдущей редакции.</p>

<!-- Раздел блокнота: § 3, 7 -->


---
section: '§ 3'
---

# MCP: сервер запрашивает недостающие данные

<div class="flow"><div class="panel"><h3>Сервер</h3><p>input_required:<br>нужен ввод пользователя</p></div><div class="arrow">→</div><div class="panel"><h3>Хост</h3><p>Показывает вопрос<br>и получает ответ</p></div><div class="arrow">→</div><div class="panel"><h3>Повтор запроса</h3><p>inputResponses:<br>передаёт ответ серверу</p></div></div><p class="takeaway">Так устроен многошаговый обмен MRTR: приложение получает недостающий ввод и повторяет вызов инструмента.</p>

<!-- Раздел блокнота: § 3 -->


---
section: '§ 3.4, 5.1'
---

# MCP Python SDK: переход с v1 на v2

| Сторона / действие | SDK v1 | SDK v2 |
|---|---|---|
| Сервер: основной класс | `FastMCP` | `MCPServer` |
| Клиент: подключение | Открыть транспорт → `ClientSession`<br>→ `await session.initialize()` | `async with Client(url) as client:`<br>или `Client(params)` для stdio |
| Клиент: каталог инструментов | `await session.list_tools()` | `await client.list_tools()` |
<p class="takeaway">В v2 Client открывает транспорт и выбирает совместимую редакцию протокола. ClientSession остаётся низкоуровневым API.</p>

<!-- Раздел блокнота: § 3.4, 5.1 -->


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

<div class="grid2"><div class="panel"><h3>Описание аргументов</h3><p>Схема задаёт имена и типы аргументов. Список required указывает обязательные поля.</p></div><div class="panel"><h3>Допустимое значение null</h3><p><code>anyOf: [integer, null]</code><br><br>API модели должен принимать такую схему</p></div></div><p class="takeaway">Допустимое null и необязательное поле — разные свойства схемы. GigaChat API v2 принимает используемые здесь схемы MCP.</p>

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
<p class="takeaway">messages — список сообщений пользователя. ainvoke запускает агента: модель выбирает MCP-инструмент и получает результат его вызова.</p>

<!-- Раздел блокнота: § 4.2 -->


---
section: '§ 4.3'
---

# MCP Туту: вызов и результат в истории

<div class="flow"><div class="panel"><h3>Запрос модели</h3><p>AIMessage:<br>search_rail и аргументы</p></div><div class="arrow">→</div><div class="panel"><h3>Результат вызова</h3><p>ToolMessage:<br>ответ сервиса Туту</p></div><div class="arrow">→</div><div class="panel"><h3>Ответ пользователю</h3><p>AIMessage:<br>поезд, время и цена</p></div></div><p class="takeaway">Сопоставляем ответ агента с ToolMessage: дату, направление, отсутствие пересадок, время и цену.</p>

<!-- Раздел блокнота: § 4.3 -->


---
section: '§ 5'
---

# MCP: сервер для чтения учебных материалов

<div class="grid3"><div class="panel"><h3>Resources</h3><p>Описание курса<br>Сведения о темах</p></div><div class="panel"><h3>Prompt</h3><p>Справка по теме<br>Заданная аудитория</p></div><div class="panel"><h3>Tools</h3><p>Список файлов<br>Чтение начала файла</p></div></div><p class="takeaway">Сервер читает файлы из data/course и предоставляет tools, resources и prompts для подготовки справки.</p>

<!-- Раздел блокнота: § 5 -->


---
section: '§ 5–7'
---

# MCP: транспорты stdio и Streamable HTTP

<div class="grid2"><div class="panel"><h3>stdio</h3><p>Хост через клиент запускает сервер как дочерний процесс.<br><br>JSON-RPC передаётся через stdin/stdout; журнал — через stderr.</p></div><div class="panel"><h3>Streamable HTTP</h3><p>Клиент обращается к отдельному серверу по URL /mcp: локально или по сети.<br><br>Ответ — JSON или поток SSE.</p></div></div><p class="takeaway">Меняется способ доставки сообщений, а tools, resources и prompts остаются теми же. В § 5 используем stdio, в § 7 — HTTP.</p>

<!-- Раздел блокнота: § 5–7 -->


---
section: '§ 6'
---

# MCP: агент готовит справку по теме

<div class="flow"><div class="panel"><h3>Контекст</h3><p>Описание курса<br>и запрос справки</p></div><div class="arrow">→</div><div class="panel"><h3>Инструменты</h3><p>Агент находит файл<br>и читает его начало</p></div><div class="arrow">→</div><div class="panel"><h3>Результат</h3><p>Справка по теме<br>и история вызовов</p></div></div><p class="takeaway">В блокноте выводим сообщения перед вызовом модели, вызовы инструментов и готовую справку.</p>

<!-- Раздел блокнота: § 6 -->


---
section: '§ 7'
---

# MCP по HTTP: запрос и ответ

<p class="lead">Запускаем сервер учебных материалов по Streamable HTTP. В блокноте смотрим отправленный запрос и ответ.</p><div class="grid2"><div class="panel"><h3>Запрос</h3><p>Метод tools/call<br>Аргументы операции<br>Версия и возможности в _meta</p></div><div class="panel"><h3>Ответ</h3><p>Результат операции<br>resultType: тип результата<br>Сведения о сервере</p></div></div><p class="takeaway">SSE передаёт сообщения потоком в HTTP-ответе. Streamable HTTP заменил старый транспорт HTTP+SSE; поддержка SSE в новом транспорте сохраняется.</p>

<!-- Раздел блокнота: § 7 -->


---
section: '§ 8'
---

# MCP: один агент с Туту и ВкусВиллом

<div class="figure"><img class="diagram" src="/diagrams/dualmcp.svg" /></div><p class="takeaway">В одном хосте Deep Agent использует два MCP-клиента: один для сервера Туту, другой — для ВкусВилла. Агент выбирает инструменты для поездки и перекуса.</p>

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

<div class="flow"><div class="panel"><h3>Приложение</h3><p>Открывает страницу<br>входа и разрешений</p></div><div class="arrow">→</div><div class="panel"><h3>Пользователь</h3><p>Подтверждает доступ</p></div><div class="arrow">→</div><div class="panel"><h3>Сервис</h3><p>Выдаёт токен<br>доступа</p></div></div><p class="takeaway">OAuth позволяет пользователю разрешить приложению доступ и получить токен. В блокноте используются публичные операции без входа в личный кабинет.</p>

<!-- Раздел блокнота: § 8.2 -->


---
section: '§ 8.2'
---

# Практика MCP: добавить инструмент на сервер

<div class="grid2"><div class="panel"><h3>Добавить</h3><p>Инструмент подсчёта учебных файлов по расширению</p></div><div class="panel"><h3>Проверить</h3><p>Найти инструмент в list_tools<br>Вызвать клиентом<br>Попросить агента посчитать файлы</p></div></div><p class="takeaway">Доступ к файлам остаётся ограничен папкой data/course.</p>

<!-- Раздел блокнота: § 8.2 -->


---
layout: corporate-section-bg
section: '§ 9–17'
---

# A2A, AG-UI, A2UI и ACP

<p>Задачи между агентами, интерфейс приложения и управление сессией агента · 45 минут</p>

<!-- Раздел блокнота: § 9–17 -->


---
section: '§ 9, 12'
---

# A2A: координатор и агент поездок

<div class="figure"><img class="diagram" src="/diagrams/a2a.svg" /></div><p class="takeaway">Координатор обращается через A2A-клиент. A2A-сервер запускает агента поездок и возвращает результат. У каждого агента свои инструменты.</p>

<!-- Раздел блокнота: § 9, 12 -->


---
section: '§ 9–10'
---

# A2A: возможности агента в Agent Card

<div class="grid2"><div class="panel"><h3>Адрес и обмен</h3><p>URL, версия протокола<br>Форматы входа и ответа<br>Авторизация и streaming</p></div><div class="panel"><h3>Skills: задачи агента</h3><p>Имя, описание, примеры запросов<br><br>Например: поиск поездки<br>Список инструментов можно не раскрывать</p></div></div><p class="takeaway">Skills помогают клиенту выбрать исполнителя. Это описания возможностей, а не инструкции SKILL.md и не отдельные вызываемые методы.</p>

<!-- Раздел блокнота: § 9–10 -->


---
section: '§ 9, 10.1'
---

# A2A: что возвращает сервер

<div class="grid2"><div class="panel"><h3>Message</h3><p>Ответ или уточняющий вопрос<br><br>Подходит для непосредственного обмена сообщениями</p></div><div class="panel"><h3>Task и artifacts</h3><p>Идентификатор, состояние задачи<br>Результаты: текст, данные, файлы<br><br>Возможны обновления по ходу работы</p></div></div><p class="takeaway">В нашем опыте клиент получает завершённую Task с текстом в artifacts. Статус completed сообщает о завершении, но не доказывает качество результата.</p>

<!-- Раздел блокнота: § 9, 10.1 -->


---
section: '§ 9–12'
---

# A2A: два варианта сервера агента поездок

<div class="grid2"><div class="panel"><h3>Кто отправляет запрос</h3><p>Сначала проверяем сервер:<br>Python-код отправляет заданный вопрос.<br><br>Затем подключаем координатора:<br>агент поручает поиск через тот же A2A-клиент.</p></div><div class="panel"><h3>Кто выполняет задачу</h3><p>Агент поездок за A2A-сервером:<br><br>A — сервер на a2a-sdk<br>B — LangGraph Agent Server</p></div></div><p class="takeaway">В обоих вариантах логика агента из agents/travel.py одинакова. Меняется реализация A2A-сервера; клиент отправляет тот же запрос.</p>

<!-- Раздел блокнота: § 9–12 -->


---
section: '§ 10'
---

# A2A: протокол и реализация сервера

<div class="grid2"><div class="panel"><h3>Что задаёт протокол</h3><p>Сервер принимает сообщения<br>и возвращает Message или Task,<br>состояние и результаты.<br><br>Внутренний цикл работы агента<br>протокол не определяет.</p></div><div class="panel"><h3>Как устроен наш сервер</h3><p>AgentExecutor передаёт текст<br>агенту поездок на сервере<br>как сообщение user.<br><br>Ответ оформляет как artifact<br>и завершает Task.</p></div></div><p class="takeaway">AgentExecutor — класс Python SDK. Отдельный обработчик и передача текста как user внутри агента не являются требованиями A2A.</p>

<!-- Раздел блокнота: § 10 -->


---
section: '§ 11'
---

# A2A, способ B: LangGraph Agent Server

<p class="small">servers/agent_server.py</p>

```python
from agents.travel import travel_graph

graph = travel_graph
```

<p class="small">langgraph.json</p>

```json
{"graphs": {"travel": "./servers/agent_server.py:graph"}}
```
<p class="takeaway">langgraph.json указывает серверу функцию создания агента. Команда langgraph dev публикует его по A2A; MCP-соединение открыто во время поиска.</p>

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
<p class="takeaway">Проверяем маршрут, дату, прямой поезд и источник цены. Клиентский код пока проверяет только завершение и наличие текста; содержательную проверку выполняем при разборе.</p>

<!-- Раздел блокнота: § 11.1 -->


---
section: '§ 10.1, 11.2'
---

# A2A: что видит клиент

<div class="grid2"><div class="panel"><h3>Публичный обмен</h3><p>Agent Card и описания skills<br>Сообщения, состояние Task<br>Artifacts с результатами</p></div><div class="panel"><h3>Не раскрывается автоматически</h3><p>Внутренние вызовы модели<br>Инструменты и MCP-серверы<br>Запуски субагентов</p></div></div><p class="takeaway">Для проверки качества нужны проверяемые результаты: данные, источники, тесты. Журнал сервера и API состояния LangGraph в блокноте — отдельные средства разбора.</p>

<!-- Раздел блокнота: § 10.1, 11.2 -->


---
section: '§ 12.1–12.2'
---

# A2A: ожидание или фоновая задача

<div class="grid2"><div class="panel"><h3>Выполняемый пример</h3><p>SendMessage → ждём итог<br>travel_agent возвращает текст<br><br>При await другие задачи Python<br>могут работать; этот вызов ждёт ответ</p></div><div class="panel"><h3>Возможность протокола</h3><p>returnImmediately: true<br>Получить taskId и продолжить работу<br>Позже: GetTask, подписка или push<br><br>Например, искать продукты, пока подбирается поезд</p></div></div><p class="takeaway">Фоновая работа требует поддержки сервера и организации работы координатора. В блокноте этот режим описан, но отдельного фонового запуска нет.</p>

<!-- Раздел блокнота: § 12.1–12.2 -->


---
section: '§ 13'
---

# AG-UI: события для приложения

<div class="figure"><img class="diagram" src="/diagrams/agui.svg" /></div><p class="takeaway">AG-UI передаёт приложению ход выполнения: агент начал работу, вызвал инструмент, дописал текст, завершил ответ. Блокнот получает эти события потоком SSE по HTTP.</p>

<!-- Раздел блокнота: § 13 -->


---
section: '§ 13.1'
---

# AG-UI: как клиент отображает события

| Событие | Действие клиента |
|---|---|
| RUN_STARTED | Показать, что агент начал работу |
| TOOL_CALL_START / TOOL_CALL_RESULT | Название инструмента и его результат |
| TEXT_MESSAGE_CONTENT | Дописать полученную часть ответа |
| RUN_FINISHED / RUN_ERROR | Завершение или сообщение об ошибке |


<!-- Раздел блокнота: § 13.1 -->


---
section: '§ 14'
---

# A2UI: описание интерфейса

<div class="figure"><img class="diagram" src="/diagrams/a2ui.svg" /></div><p class="takeaway">A2UI передаёт описание экрана: типы элементов, тексты и связи между ними. Рендерер — код приложения, который строит экран по этому описанию.</p>

<!-- Раздел блокнота: § 14 -->


---
section: '§ 14.1'
---

# A2UI: от JSON к карточке поезда

<div class="grid2"><div class="panel"><h3>Структура</h3><p>createSurface: создать экран<br>updateComponents: задать элементы<br>Card → Text: текст внутри карточки</p></div><div class="panel"><h3>Данные</h3><p>Номер поезда<br>Отправление и прибытие<br>Цена</p></div></div><p class="takeaway">В примере A2UI v0.9 описывает карточку с данными поезда. Блокнот показывает исходный JSON и полученное статическое изображение интерфейса.</p>

<!-- Раздел блокнота: § 14.1 -->


---
section: '§ 15'
---

# ACP: приложение общается с агентом

<div class="figure"><img class="diagram" src="/diagrams/acp.svg" /></div><p class="takeaway">ACP задаёт интерфейс приложения к агенту. Клиентом может быть IDE, терминальное или веб-приложение. В примере клиент — блокнот, обмен идёт через stdin/stdout.</p>

<!-- Раздел блокнота: § 15 -->


---
section: '§ 15'
---

# ACP: создание сессии и отправка запроса

<div class="flow"><div class="panel"><h3>initialize</h3><p>Версия и возможности</p></div><div class="arrow">→</div><div class="panel"><h3>session/new</h3><p>Создать диалог<br>и задать рабочую папку</p></div><div class="arrow">→</div><div class="panel"><h3>session/prompt</h3><p>Отправить задачу<br>в эту сессию</p></div></div><p class="takeaway">session/update передаёт части ответа; stopReason=end_turn означает завершение. Сообщения JSON-RPC идут в stdout, диагностические сообщения — в stderr.</p>

<!-- Раздел блокнота: § 15 -->


---
section: '§ 16'
---

# Покупка через агента: участники и согласие

<p class="lead">Пример: агент подбирает продукты. Перед оплатой нужно согласовать состав заказа, сумму и разрешение пользователя.</p><div class="flow"><div class="panel"><h3>Пользователь</h3><p>Выбирает товар<br>и разрешает покупку</p></div><div class="arrow">→</div><div class="panel"><h3>Агент и продавец</h3><p>Уточняют покупку</p></div><div class="arrow">→</div><div class="panel"><h3>Платёжный сервис</h3><p>Проверяет разрешение</p></div></div><p class="takeaway">Протоколы описывают обмен данными заказа и подтверждение права на оплату. В блокноте обсуждаем этот обмен без выполнения платежей.</p>

<!-- Раздел блокнота: § 16 -->


---
section: '§ 16'
---

# Протоколы покупки и оплаты

| Протокол | Назначение |
|---|---|
| Agentic Commerce Protocol | Состав, стоимость и оформление заказа между агентом и продавцом |
| UCP | Поиск товара, корзина, оформление и работа с заказом |
| AP2 | Подтверждение полномочий агента и согласия пользователя на оплату |
| x402 | HTTP-ответ 402 с условиями оплаты; повторный запрос с подтверждением |
<p class="takeaway">Agent Client Protocol и Agentic Commerce Protocol имеют одинаковую аббревиатуру ACP.</p>

<!-- Раздел блокнота: § 16 -->


---
section: '§ 17'
---

# Контрольные вопросы

<div class="grid2"><div class="panel"><h3>Инструменты и контекст</h3><p>Кто читает ресурс MCP?<br>Что возвращает промпт MCP?<br>Где выполняется инструмент?</p></div><div class="panel"><h3>Агенты и приложение</h3><p>Кто ищет поездку по A2A?<br>Кто строит экран из A2UI?<br>Как ACP возвращает ответ?</p></div></div>

<!-- Раздел блокнота: § 17 -->


---
section: 'ДЗ'
---

# Домашнее задание: RAG и MCP

<div class="grid2"><div class="panel"><h3>Собрать</h3><p>Свой корпус → локальные эмбеддинги<br>Индекс и готовый MCP-сервер поиска<br>Агент возвращает top-k и источники</p></div><div class="panel"><h3>Проверить и сдать</h3><p>15–20 запросов и ручная оценка<br>document_id, chunk_id, source<br>Код, конфигурация и инструкция запуска</p></div></div><p class="takeaway">Полные условия и критерии: <a href="https://github.com/trashchenkov/mipt_protocols/blob/main/homework_mcp_knowledge_base.pdf">PDF задания в репозитории</a>. По желанию: передать вопрос и top-k фрагменты в LLM; получить ответ со ссылками на источники.</p>

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

<div class="grid2"><div class="panel"><h3>SKILL.md</h3><p>name: qr-code — как имя папки<br>description: когда применять<br>Инструкция: какие шаги выполнить</p></div><div class="panel"><h3>Файлы</h3><p>scripts/qr_generate.py — создать PNG<br>scripts/qr_read.py — прочитать QR</p></div></div><p class="takeaway">По имени и описанию агент выбирает навык, читает SKILL.md и выполняет указанные шаги.</p>

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

# Skills: встроенный SkillsMiddleware

```python
agent = create_deep_agent(
    model=model, backend=backend,
    skills=[skills_dir.as_posix()],
)
```
<div class="flow"><div class="panel"><h3>SkillsMiddleware</h3><p>Имена, описания<br>и пути к навыкам</p></div><div class="arrow">→</div><div class="panel"><h3>read_file</h3><p>Агент читает<br>выбранный SKILL.md</p></div><div class="arrow">→</div><div class="panel"><h3>execute</h3><p>Агент запускает<br>скрипты навыка</p></div></div><p class="takeaway">SkillsMiddleware показывает модели описания навыков. В блокноте проверьте, какой SKILL.md агент прочитал и какие команды выполнил.</p>

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
<p class="takeaway">pyzbar — Python-обёртка над декодером ZBar. После установки выполните uv run python tools/check_env.py --qr: он создаёт и читает QR-код.</p>

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
