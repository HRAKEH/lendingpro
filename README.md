# LendingPro — товарные лендинги ЗДРАВА

## 🎬 Актуальная v8.3 Cinematic Product Story
- **Сайты:** `next-v8/mikozacid/`, `next-v8/hot-ice/`
- **[Готовый ZIP Timeweb](releases/ZDRAVA_v8_3_CINEMATIC_FIXED.zip)** — 2 новых лендинга, оригинальные PNG упаковок, анимация в коде; 15 файлов.
- **[Документация v8.3](docs/MOTION_V8_3.md)** — scroll-driven Canvas 2D сцены, проверка браузером, исправленные отступы карточек состава.
- v7/v8/v8.1 зарезервированы в отдельных архивных ветках.
- **На Timeweb ничего не опубликовано**, страницы сохраняют noindex до проверки контента.


## ✨ Актуальная v8.2 Kinetic Editorial (28.10.2026)

Два новых сайта на `main/next-v8/` теперь содержат дополнительную анимацию, прорисовку декоративных SVG, типографическую ленту, разделы glass-rail и интерактивные 3D/магнитные hover. Подлинные упаковки без изменений.

- [**ZIP для Timeweb: v8.2**](releases/zdrava-v8-2-kinetic-editorial-timeweb.zip)
- [**Документация v8.2 и QA**](docs/MOTION_V8_2.md)
- [**Архив v8.1**](https://github.com/HRAKEH/lendingpro/tree/archive/v8-1-motion-studio)

На Timeweb ничего не менялось. Анимации GSAP при доступном CDN и SEO после снятия noindex требуют дополнительной проверки.

## Историческая версия v8.1 Motion Studio (28.10.2026)

- **Актуальная v8.1**: `next-v8/mikozacid/`, `next-v8/hot-ice/` — улучшенная анимация, стеклянные слои и scroll-ритуал.
- **[Готовый ZIP для Timeweb](releases/zdrava-v8-motion-studio-timeweb.zip)**.
- **[Описание анимаций и честный статус QA](docs/MOTION_V8_1.md)**.
- **[Архив исходной v8](https://github.com/HRAKEH/lendingpro/tree/archive/v8-first-rebuild)** и **[архив v7](https://github.com/HRAKEH/lendingpro/tree/archive/v7-cinematic-motion)**.
- На Timeweb ничего не публиковалось; версии `mikozacid/` и `hot-ice/` в корне остались без изменений.

## Историческая разработка v8 (28.10.2026)
- [**Микозацид v8**](next-v8/mikozacid/index.html) — полностью новый responsive HTML, оригинальный PNG, OG, анимации, SEO.
- [**Горячий лёд v8**](next-v8/hot-ice/index.html) — полностью новый responsive HTML, оригинальный PNG, OG, анимации, SEO.
- [**Скачать ZIP для тестирования на Timeweb**](releases/zdrava-next-v8-timeweb.zip) — обе новые страницы вместе.
- [**Полное описание v8 и ограничения**](docs/LANDING_V8_REBUILD.md).
- [**Исходное мастер-ТЗ**](docs/MASTER_TZ_2026_10_28.txt).
- [**Отдельная архивная ветка полной v7**](https://github.com/HRAKEH/lendingpro/tree/archive/v7-cinematic-motion).

**Важно:** действующие каталоги `mikozacid/` и `hot-ice/` пока остаются v7; `next-v8/` — кандидат на замену после браузерной проверки и проверки состава. На Timeweb ничего не меняли.


**Актуальное состояние: 28 октября 2026.** В репозитории сохранены исходники **трёх реальных статических сайтов**, файлы изображений, история дизайнерских решений и технический ZIP последней v7.

## Исходники сайтов
| Товар | Каталог | Состояние |
|---|---|---|
| **Микозацид** | [`mikozacid/`](mikozacid/) | **v7 Cinematic Motion** — HTML/CSS/JS и оригинальный PNG упаковки |
| **Горячий лёд** | [`hot-ice/`](hot-ice/) | **v7 Cinematic Motion** — HTML/CSS/JS и оригинальный PNG упаковки |
| **Флебодиа** | [`flebodia/`](flebodia/) | Исходная одностраничная статическая версия HTML + WebP |

**Для Timeweb:** готовый архив двух новых лендингов [`releases/lendingpro-timeweb-v7-cinematic-motion.zip`](releases/lendingpro-timeweb-v7-cinematic-motion.zip). В нём две папки `mikozacid/` и `hot-ice/`; помещать их **рядом** с основным `index.html` в **проверенный** корень сайта, не перезаписывая главную страницу ЗДРАВА.

## Что где лежит
- `mikozacid/` и `hot-ice/` — работающий код последней v7: `index.html`, `styles.css`, `editorial.css`, `atmosphere.css`, `motion.css`, `script.js`, `motion.js` и `assets/`.
- `flebodia/` — исходный лендинг из архива разработчика с `assets/hero.webp` и `assets/rest.webp`.
- `source-assets/` — исходные присланные изображения упаковок; в лендингах используются обработанные, **не перерисованные** вырезанные тубы.
- `tools/v7-sources/` — вспомогательные скрипты подготовки и статической проверки.
- `releases/` — архив готовой v7 для переноса на Timeweb.
- `docs/` — решения, брифы, дизайн-системы, ограничения и история.
- `landing-01/`, `landing-02/` — **исторические экспериментальные прототипы**, не путать с актуальными сайтами.

## Начать работу в новом чате
Открой [PROJECT_MEMORY](docs/PROJECT_MEMORY.md), [LANDING_V7_MOTION](docs/LANDING_V7_MOTION.md), [PROJECT_STRUCTURE](docs/PROJECT_STRUCTURE.md), [TASKS](docs/TASKS.md). Работать с исходниками в `mikozacid/` и `hot-ice/`, а не с историческими заглушками.

## Шрифты и стиль
Оба новых сайта используют только **Onest + Golos Text**, кнопки **Ozon и Wildberries**, номера шагов **1, 2, 3** и оригинальные изображения упаковок. Никаких вымышленных медицинских утверждений; текущие страницы имеют `noindex,nofollow`.

## Статус публикации и проверки
**Сохранено в GitHub ≠ опубликовано на Timeweb.** Хостинг этой операцией не менялся. Проверка v7 по структуре/синтаксису была успешной, но полноценная браузерная QA v7 и проверка состава/этикеток ещё требуются. Репозиторий **публичный** — не добавлять токены, пароли, закрытые таблицы заказчика и персональные данные.

