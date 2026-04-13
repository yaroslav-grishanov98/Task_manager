# 🚀 Task Management System Backend

![Django, DRF, PostgreSQL, Docker](https://img.shields.io/badge/Django-092E20?style=for-the-badge&logo=django&logoColor=green)
![DRF](https://img.shields.io/badge/Django%20REST%20Framework-DD4F0D?style=for-the-badge&logo=html5&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-316192?style=for-the-badge&logo=postgresql&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white)
![Python 3.11](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)

Backend-часть полноценной системы управления задачами, разработанная с использованием современных веб-технологий. Этот проект демонстрирует глубокие знания в бэкенд-разработке, включая создание REST API, работу с базами данных, контейнеризацию и автоматизированное тестирование.

---

## ✨ **Основные возможности (Features)**

*   **Пользовательская аутентификация и авторизация:**
    *   Регистрация новых пользователей.
    *   Вход по Email и получение токена аутентификации.
    *   Активация аккаунта по Email (с отправкой письма в консоль).
    *   Защита API-эндпоинтов, требующая аутентификации пользователя.
*   **Управление задачами (CRUD):**
    *   Создание, просмотр, обновление, удаление деталей задач.
    *   Поля задачи: Заголовок, Описание, Срок выполнения, Приоритет (Низкий/Средний/Высокий), Статус (Новая/В работе/Завершена/Отменена), Владелец.
    *   Автоматическая привязка задачи к текущему пользователю-создателю.
*   **Управление проектами (CRUD):**
    *   Создание, просмотр, обновление, удаление проектов.
    *   Проекты принадлежат пользователям.
    *   Задачи могут быть связаны с конкретным проектом.
*   **Управление комментариями:**
    *   Создание, просмотр, обновление, удаление комментариев к задачам.
    *   Комментарии привязаны к пользователю и задаче.
    *   Комментарии отображаются вложенно при получении деталей задачи.
*   **Расширенная функциональность API:**
    *   **Фильтрация:** Задач по статусу, приоритету, сроку выполнения (`due_date_before`, `due_date_after`), а также по ID проекта.
    *   **Поиск:** Поиск задач по заголовку и описанию.
    *   **Пагинация:** Получение списков задач и проектов частями для повышения производительности.
*   **Автоматическая документация API:**
    *   Интерактивная документация в формате OpenAPI (Swagger UI), доступная по `/api/schema/swagger-ui/`. Предоставляет полную информацию об эндпоинтах, схемах данных и позволяет тестировать запросы прямо из браузера.
*   **Автоматизированные тесты:**
    *   Комплексный набор `Unit/Integration` тестов (22+ теста), покрывающий все основные API-эндпоинты и бизнес-логику, обеспечивающий надежность и предотвращающий регрессии.
*   **Контейнеризация с Docker Compose:**
    *   Проект разворачивается в изолированном окружении Docker, включая контейнеры для Django-приложения и базы данных PostgreSQL.

---

## 🛠️ **Используемые технологии**

*   **Python 3.11**
*   **Django 5.0.x**
*   **Django REST Framework (DRF)**
*   **PostgreSQL 16**
*   **Docker & Docker Compose**
*   **drf-spectacular:** Для автоматической документации OpenAPI
*   **django-filter:** Для фильтрации API
*   **djoser:** (Если ты решил его вернуть) для расширенной аутентификации
*   **Postman:** Для ручного тестирования API
*   **Git & GitHub:** Для контроля версий

---

## 🚀 **Быстрый старт (Quick Start)**

Для запуска проекта на вашей локальной машине:

1.  **Клонируйте репозиторий:**
    ```bash
    git clone https://github.com/yaroslav-grishanov98/Task_manager.git
    cd Task_manager
    ```
2.  **Настройте Docker:**
    *   Убедитесь, что Docker Desktop установлен и запущен.
3.  **Создайте файл `.env`:**
    *   В корневом каталоге проекта создайте файл `.env` со следующим содержимым. **Замени значения на свои (для `EMAIL_HOST` и т.д. используйте 'mailhog' или `console.EmailBackend` если Mailtrap недоступен, как обсуждалось ранее).**
    ```env
    POSTGRES_DB=task_manager_db
    POSTGRES_USER=task_manager_user
    POSTGRES_PASSWORD=mysecretpassword
    POSTGRES_HOST=db
    POSTGRES_PORT=5432

    # Для активации аккаунта (если используете console.EmailBackend, эти можно закомментировать)
    EMAIL_BACKEND='django.core.mail.backends.console.EmailBackend'
    # EMAIL_HOST=smtp.mailtrap.io
    # EMAIL_PORT=2525
    # EMAIL_USE_TLS=True
    # EMAIL_HOST_USER=YOUR_MAILTRAP_USERNAME
    # EMAIL_HOST_PASSWORD=YOUR_MAILTRAP_PASSWORD
    
    SECRET_KEY=ВАШ_СЕКРЕТНЫЙ_КЛЮЧ_ДЛЯ_ДЖАНГО # Сгенерируйте новый!
    ```
4.  **Запустите Docker Compose:**
    ```bash
    docker compose up -d --build
    ```
    *   `--build` гарантирует пересборку образов с учетом последних зависимостей.
5.  **Выполните миграции базы данных:**
    ```bash
    docker compose exec web python manage.py migrate
    ```
6.  **Создайте суперпользователя (для доступа к Django Admin и первоначального тестирования):**
    ```bash
    docker compose exec web python manage.py createsuperuser
    ```
7.  **Получите токен аутентификации для суперпользователя (для тестирования API):**
    ```bash
    docker compose exec web python manage.py drf_create_token <имя_суперпользователя>
    ```
    Сохраните этот токен!

---

## ✅ **Тестирование API**

Проект включает набор автоматических тестов. Вы также можете использовать Postman или Swagger UI.

1.  **Запустите автоматические тесты:**
    ```bash
    docker compose exec web python manage.py test tasks
    ```
2.  **Документация API (Swagger UI):**
    *   Откройте в браузере: `http://localhost:8000/api/schema/swagger-ui/`
    *   Используйте полученный токен для авторизации (`Authorize` -> `Token <ВАШ_ТОКЕН>`).
3.  **Примеры базовых эндпоинтов (с использованием токена в `Authorization: Token <ТОКЕН>`):**
    *   **Регистрация:** `POST http://localhost:8000/api/register/`
        *   Body: `{"username": "newuser", "email": "user@example.com", "password": "password123", "password2": "password123"}`
    *   **Логин (получение токена):** `POST http://localhost:8000/api/login/`
        *   Body: `{"email": "user@example.com", "password": "password123"}`
    *   **Список задач:** `GET http://localhost:8000/api/tasks/`
    *   **Создание задачи:** `POST http://localhost:8000/api/tasks/`
        *   Body: `{"title": "Test Task", "description": "Desc", "due_date": "2026-04-15", "priority": "medium", "status": "new", "project_id_for_write": 1}`
    *   **Список проектов:** `GET http://localhost:8000/api/projects/`
    *   **Список комментариев:** `GET http://localhost:8000/api/comments/`

---

## 👩‍💻 **Дальнейшее развитие (Future Enhancements)**

*   Реализация функционала команд (групп пользователей) и совместной работы над проектами.
*   Добавление системы уведомлений.
*   Возможность прикрепления файлов к задачам.
*   Расширение профиля пользователя.
*   Развертывание (Deployment) проекта с использованием Gunicorn/Nginx.
