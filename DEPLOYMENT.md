# Deployment

## Local development

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
$env:DJANGO_DEBUG = "true"
$env:DJANGO_ALLOWED_HOSTS = "127.0.0.1,localhost"
python manage.py migrate
python manage.py runserver
```

## Render or Railway

The repository already contains a `Procfile`. Create a Python web service from the GitHub repository and use:

- Build command: `pip install -r requirements.txt && python manage.py collectstatic --no-input && python manage.py migrate`
- Start command: `gunicorn EmotionMusicRec.wsgi --log-file -`
- `DJANGO_SECRET_KEY`: a long random value
- `DJANGO_DEBUG`: `false`
- `DJANGO_ALLOWED_HOSTS`: the deployed hostname
- `DJANGO_CSRF_TRUSTED_ORIGINS`: the deployed HTTPS origin, such as `https://your-app.onrender.com`
- `DATABASE_URL`: the provider's managed PostgreSQL connection string

The included `render.yaml` can create the web service and PostgreSQL database on Render. The production requirements intentionally exclude TensorFlow so the web service stays deployable on a small instance. The app reports demo mode until `requirements-ml.txt` is installed on a worker with enough memory for model inference.

## GitHub

The Django project lives in this `app` directory and has its own Git repository. Commit the application changes from this directory, then push to the existing `origin` remote.