Development setup: share a single database so all devs see the same products

Choose your approach:

## Option 1: Railway Postgres (Recommended, easiest for teams)
See `RAILWAY_SETUP.md` for step-by-step provisioning (5 min).
Best for: Team collaboration, free, managed service, accessible from anywhere.

## Option 2: Local Docker Postgres (Free, requires Docker)
Run Postgres locally and share via network. Best for: Small teams, same LAN.

1) Install Docker and Docker Compose

2) Start the Postgres DB (run on a host accessible to your team):

```bash
# from project root
docker-compose up -d
```

3) Copy `.env.example` to `.env` and update HOST IP if needed

```bash
cp .env.example .env
# edit .env to set DATABASE_URL if host isn't 127.0.0.1
```

4) Install python deps (create venv first):

```bash
python -m venv .venv
# Windows PowerShell
.\.venv\Scripts\Activate.ps1
# then
pip install -r requirements.txt
```

5) Run migrations and create a superuser (only once):

```bash
python manage.py migrate
python manage.py createsuperuser
```

6) Start the Django development server:

```bash
python manage.py runserver 0.0.0.0:8000
```

7) On other developer machines, set `DATABASE_URL` in `.env` to point to the host running the Postgres container (use host LAN IP). Then follow steps 4-6.

Notes
- Uploaded media are still local (`MEDIA_ROOT`). To share product images you should configure centralized storage (S3 or a shared file server).
- Be careful running migrations from multiple machines at the same time; coordinate who runs `migrate`.
- For production consider managed Postgres (Railway, Heroku Postgres, AWS RDS) and deploying the app so all users hit the same application and DB.

