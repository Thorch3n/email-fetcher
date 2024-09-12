# Email Fetcher

Этот проект предназначен для извлечения и хранения сообщений электронной почты. Он использует Django для веб-интерфейса и PostgreSQL в качестве базы данных.

## Установка

1. **Клонируйте репозиторий:**
   ```bash
   git clone https://github.com/Thorch3n/email-fetcher.git
   cd mail_integration
    ```
2. Создайте и активируйте виртуальное окружение:
```bash
python -m venv .venv
.\.venv\Scripts\activate  # Для Windows
source .venv/bin/activate  # Для Linux/Mac

```
3. Установите зависимости
```bash
pip install -r requirements.txt
```
4. Настройте базу данных PostgreSQL:
   - Убедитесь, что PostgreSQL установлен и работает;
   - Создайте базу данных и пользователя (например, через ```psql```):
   ```sql
    CREATE DATABASE email_fetcher;
    CREATE USER email_user WITH PASSWORD 'yourpassword';
    ALTER ROLE email_user SET client_encoding TO 'utf8';
    ALTER ROLE email_user SET default_transaction_isolation TO 'read committed';
    ALTER ROLE email_user SET timezone TO 'UTC';
    GRANT ALL PRIVILEGES ON DATABASE email_fetcher TO email_user;  
   ```
5. Настройка Redis
Убедитесь, что Redis запущен на вашем компьютере:
```bash
redis-server
```
6. Запуск Daphne для поддержки WebSockets
Daphne используется для обработки WebSockets через Django Channels. Выполните следующую команду для запуска:
```bash
daphne -b 0.0.0.0 -p 8001 mail_integration.asgi:application
```
7. Настройте подключение к базе данных в ```settings.py```: Замените параметры DATABASE на ваши данные:
    ```
   DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'email_fetcher',
        'USER': 'email_user',
        'PASSWORD': 'yourpassword',
        'HOST': 'localhost',
        'PORT': '5432',
         }
    }
   ```
8. Примените миграции
   ```bash
   python manage.py migrate
   ```
9. Создайте суперпользователя (если требуется):
   ```bash
   python manage.py createsuperuser
   ```
10. Запустите сервер разработки:
   ```bash
   python manage.py runserver
   ```
# Использование

1. Перейдите по адресу http://localhost:8000/email-form/, чтобы ввести данные для подключения к электронной почте.
2. После ввода данных, приложение попытается извлечь сообщения и сохранить их в базе данных.
3. Перейдите по адресу http://localhost:8000/messages/, чтобы просмотреть извлеченные сообщения.