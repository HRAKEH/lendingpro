# LendingPro: два независимых лендинга

Старт проекта: 27 октября 2026.

В этом репозитории находятся **два независимых сайта** и **вся проектная документация** для переноса работы между чатами или аккаунтами ChatGPT.

## Навигация

- [Лендинг 1](landing-01/index.html) и [его техническое задание](docs/BRIEF_LANDING_01.md)
- [Лендинг 2](landing-02/index.html) и [его техническое задание](docs/BRIEF_LANDING_02.md)
- [PROJECT_MEMORY](docs/PROJECT_MEMORY.md): **главный файл передачи контекста**
- [TASKS](docs/TASKS.md): текущие и следующие задачи
- [DECISIONS](docs/DECISIONS.md): журнал решений и причин
- [CHANGELOG](docs/CHANGELOG.md): журнал выполненных изменений
- [WORKFLOW](docs/WORKFLOW.md): правила работы
- [DESIGN_REVIEW](docs/DESIGN_REVIEW.md): чек-лист визуальной проверки
- [DEPLOYMENT](docs/DEPLOYMENT.md): публикация и SSL

## Быстрый запуск

Два сайта пока **черновые технические страницы**, не утверждённый дизайн. Без сборщиков, на HTML/CSS/JS.

```bash
python -m http.server 8000
```

Откройте http://localhost:8000/landing-01/ и http://localhost:8000/landing-02/.

Проверка структуры: `python tools/check_project.py`.

## Как продолжить в новом ChatGPT

Подключить GitHub к аккаунту ChatGPT, отправить ссылку на этот репозиторий и попросить прочитать `README.md`, `docs/PROJECT_MEMORY.md`, `docs/TASKS.md`, оба `docs/BRIEF_*.md`, `docs/DECISIONS.md`, `docs/CHANGELOG.md`.

Все достоверные решения фиксируются здесь, чтобы проект не зависел от истории чата.

**Безопасность:** репозиторий изначально создан публичным. Рекомендуется сделать приватным до добавления коммерческих данных. Никогда не храните здесь токены, пароли и заявки с персональными данными.
