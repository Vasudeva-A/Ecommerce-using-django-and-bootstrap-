Render deployment steps

1. Ensure environment variables on Render service:
   - `SECRET_KEY` (set a secure value)
   - `DJANGO_DEBUG` -> `False`
   - `ALLOWED_HOSTS` -> space-separated hostnames, e.g. `your-service.onrender.com`

2. Build and start:
   - Render uses the `Procfile` already provided: `web: gunicorn Vasu_project.wsgi --log-file -`
   - Ensure `requirements.txt` contains `gunicorn` and `whitenoise` (already present).

3. Static files:
   - We use Whitenoise; run `python manage.py collectstatic --noinput` during build (Render runs `pip install -r requirements.txt` then calls the start command). You can add a build command in Render settings: `python manage.py collectstatic --noinput`.

4. Database:
   - For production use Postgres or another managed DB; set `DATABASE_URL` and configure `DATABASES` accordingly.

5. After creating the service on Render, set the environment variables and deploy.

Local quick test:

```bash
python -m venv env
env\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```
