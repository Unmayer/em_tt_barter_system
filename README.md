# Тестовое задание. Разработка проекта: Платформа для обмена вещами (бартерная система)

## Развёртывание
1. Клонирование репозитория:
```
git clone https://github.com/Unmayer/em_tt_barter_system.git
```
2. Переход в директорию проекта:
  
```
cd em_tt_barter_system
```

3. Установка зависимостей poetry:
  
```
poetry install
```

4. Активируйте виртуальное окружение poetry:
  
```
poetry shell
```
5. Выполнение миграций:
  
```
python manage.py migrate
```
6. Создайте суперпользователя:
  
```
python manage.py createsuperuser
```
7. Запуск проекта:

```
python manage.py runserver
```

8. Перейдите по адресу http://127.0.0.1:8000/


9. Перейдите по адресу http://127.0.0.1:8000/admin и войдите в админ-панель под суперпользователем


10. Для запуска тестов:

```
pytest -v
```

## Результаты
В ходе разработки были реализованы следующие аспекты:
- Веб-интерфейс для осуществления бизнес-процессов бартерной системы.
- Фильтрация по различным критериям предметной области.
- Пагинация
- REST API для бартерной системы
- Создана автоматическая документация API
- Были протестированы ключевые функции бартерной системы