# Структура проекта — снимок 2026-10-28

## Рабочие сайты
```text
lendingpro/
├── README.md
├── README_TIMEWEB.txt
├── mikozacid/
│   ├── index.html
│   ├── styles.css
│   ├── editorial.css
│   ├── atmosphere.css
│   ├── motion.css
│   ├── script.js
│   ├── motion.js
│   └── assets/
│       ├── product.png
│       ├── texture.png
│       └── SOURCE.txt
├── hot-ice/
│   └── [аналогичная структура]
├── flebodia/
│   ├── index.html
│   └── assets/
│       ├── hero.webp
│       └── rest.webp
├── releases/
│   └── lendingpro-timeweb-v7-cinematic-motion.zip
├── source-assets/
│   ├── mikozacid-source-photo.jpeg
│   └── hot-ice-source-photo.jpeg
├── tools/v7-sources/
│   └── [скрипты сборки и проверки]
├── docs/
│   ├── PROJECT_MEMORY.md
│   ├── TASKS.md
│   ├── DECISIONS.md
│   ├── CHANGELOG.md
│   ├── LANDING_V7_MOTION.md
│   └── PROJECT_STRUCTURE.md
├── landing-01/ [старый прототип]
└── landing-02/ [старый прототип]
```

## Источник истины
Точная версия файлов релиза **v7** загружена из `lendingpro-timeweb-v7-cinematic-motion.zip` без пересохранения. **Git blob SHA-1 всех 32 переданных файлов совпадает** с локально вычисленными исходными файлами; содержимое фото туб не заменялось. ZIP продублирован в `releases/`.

## Проверка
- Каждая из двух v7 содержит index.html, 4 CSS, 2 JS, assets/product.png и texture.png.
- Оба сайта имеют реальные фото товара, ссылки Ozon/Wildberries, подключение анимаций.
- Сайты статические, сборка для Timeweb не нужна.
- Эти файлы являются архивом рабочего состояния проекта, **не подтверждением работоспособности в новом окружении**. Браузерная проверка v7 нужна после развёртывания.
- `flebodia/` содержимое исходного пакета разработчика, не из изменённой копии на хостинге.
- Рабочие исходники **не** находятся в `landing-01/` и `landing-02/`.
- Исходные тексты о свойствах нужно сверить с этикеткой перед рекламой.
