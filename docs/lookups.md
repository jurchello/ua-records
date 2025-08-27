# Lookups (довідкові списки для форм)

Цей модуль надає провайдери списків для форм (імена, прізвища, касти, заняття, причини смерті).  
Дані читаються через репозиторії і кешуються у файловому кеші нового проєкту.

## Використання

```python
from ua_records.lookups import (
  set_runtime_db,
  MAN_SURNAMES, ALL_GIVEN, ALL_OCCUPATIONS,
  schedule_refresh_after_save, force_refresh
)

set_runtime_db(db)

surnames = MAN_SURNAMES()       # швидко: читає з кеша; приймає прострочені значення
given = ALL_GIVEN()
occ   = ALL_OCCUPATIONS()
```

## Швидкий старт кеша

- При першому зверненні провайдер читає з кеша з `accept_stale=True`, тому форма відкривається миттєво навіть якщо TTL протух.
- Якщо в кеші MISS — робиться повний скан БД через `PeopleScanner` і одразу пишеться свіже значення.

TTL за замовчуванням: `24h`.

## Оновлення після збереження

Після збереження записів можна тригерити відкладене оновлення:

```python
schedule_refresh_after_save()  # дебаунс 3с, працює у фоні
```

Або примусово:

```python
force_refresh()
```

## Тести

Запуск:

```bash
pytest -q
```
