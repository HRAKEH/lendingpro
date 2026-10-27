# LendingPro — управление товарными лендингами

Репозиторий: https://github.com/HRAKEH/lendingpro

## Проекты
- **Флебодиа** — ранее передан готовый сайт из ZIP. Согласован путь `zdrava.ru/flebodia/`. Структура: [LANDING_01_ARCHITECTURE.md](docs/LANDING_01_ARCHITECTURE.md); размещение: [DEPLOY_FLEBODIA_ZDRAVA.md](docs/DEPLOY_FLEBODIA_ZDRAVA.md). Оригинальные HTML/WebP пока не заменили заглушку в GitHub; публикация не подтверждена.
- **Микозацид** — новый товарный лендинг; **утверждена дизайн-система** [Clinical Minimal, C1/F1](docs/DESIGN_SYSTEM_MIKOZACID.md), разработка полной страницы впереди.
- **Горячий лёд** — новый товарный лендинг; **утверждена дизайн-система** [Ice Premium, C2/F1](docs/DESIGN_SYSTEM_HOT_ICE.md), разработка полной страницы впереди.

## Актуальное состояние
- [PROJECT_MEMORY](docs/PROJECT_MEMORY.md) — **начать здесь при переходе в новый чат**.
- [TASKS](docs/TASKS.md) — следующие шаги.
- [DECISIONS](docs/DECISIONS.md) — всё утверждённое пользователем.
- [CHANGELOG](docs/CHANGELOG.md) — история изменений.
- [PRODUCT_SHORTLIST](docs/PRODUCT_SHORTLIST.md) — предварительный аналитический отбор товаров.
- [DESIGN_REVIEW_ROUND_02](docs/DESIGN_REVIEW_ROUND_02.md) — сравнение вариантов перед утверждением.
- [Брифы](docs/BRIEF_LANDING_01.md) и [BRIEF_LANDING_02](docs/BRIEF_LANDING_02.md) — исторические документы; учитывайте более новые дизайн-системы и PROJECT_MEMORY.

## Реальные файлы и технические прототипы
`landing-01/` и `landing-02/` — **пока старые технические демонстрации**, их нельзя выдавать за законченные лендинги Микозацида или Горячего льда. Утверждённые переменные дизайна находятся в `design-system/mikozacid/tokens.css` и `design-system/hot-ice/tokens.css`, без изменения работающего хостинга.

Тест технических прототипов:
```bash
python tools/check_project.py
```

**Безопасность:** ранее репозиторий был публичным; хранить здесь нельзя пароли, токены, приватную таблицу заказчика, заявки и внутренние коммерческие данные.
