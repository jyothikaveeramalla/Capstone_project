Provisioning a cloud Postgres (Railway / ElephantSQL / Supabase) and configuring the Django project

This guide shows how to provision a free cloud Postgres instance, configure `DATABASE_URL`, run migrations, and migrate data so all team members see the same products.

Options compared briefly
- Railway: Easy to set up, generous free tier, connects to GitHub, provides `DATABASE_URL` quickly.
- Supabase: Full-featured, also provides auth and storage; free tier available.
- ElephantSQL: Simple Postgres-managed service, small free plan.

I’ll show steps for Railway and ElephantSQL (both are quick). After provisioning, set `DATABASE_URL` in your project and run `migrate` (or import data).

---

A. Railway (recommended for quick setup)
1. Sign up at https://railway.app/ (GitHub sign-in recommended).
2. Create a new project and add a PostgreSQL plugin.
   - Click "New Project" → "Provision Postgres" (PostgreSQL plugin)
   - Railway will provision a database and show connection details.
3. Copy the `DATABASE_URL` value from Railway dashboard.
   - It will look like: `postgres://username:password@ep-xxxxx.region.aws.neon.tech:5432/dbname`
4. Locally set `DATABASE_URL` in `.env` (or export env var):

Bash / macOS / Linux:
```bash
export DATABASE_URL="postgres://user:pass@host:5432/dbname"
export DJANGO_SECRET_KEY="change-me"
```
Windows PowerShell:
```powershell
$env:DATABASE_URL = "postgres://user:pass@host:5432/dbname"
$env:DJANGO_SECRET_KEY = "change-me"
```

5. Install dependencies (if not already):
```bash
pip install -r requirements.txt
```

6. Apply migrations once (coordinate among team):
```bash
python manage.py migrate
python manage.py createsuperuser
```

7. Optional: Migrate existing SQLite data to Postgres
- To transfer existing data from `db.sqlite3` to the new Postgres, use `pgloader` or `django-migration` via dump/loaddata:

Export fixtures from old DB:
```bash
python manage.py dumpdata --natural-primary --natural-foreign --exclude auth.permission --exclude contenttypes > db_dump.json
```

Load fixtures into Postgres (after `DATABASE_URL` points to Postgres and migrations applied):
```bash
python manage.py loaddata db_dump.json
```

---

B. ElephantSQL (very simple)
1. Sign up at https://www.elephantsql.com/
2. Create a new instance (Tiny Turtle free plan)
3. Copy the `URL` (the `DATABASE_URL`) from the instance details
4. Set the environment variable locally or in your production environment, then `migrate` as above

---

C. After provisioning (team instructions)
1. Add `DATABASE_URL` and `DJANGO_SECRET_KEY` to `.env` (share with teammates securely, e.g., via pinned issue or private chat). Do NOT commit secrets to Git.
2. Each developer sets `.env` accordingly and runs:
```bash
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```
3. Confirm that products added by any developer appear for all developers.

---

Security and operational notes
- Never commit `.env` or credentials to GitHub. Add `.env` to `.gitignore` (it already exists in repo).
- Use managed DB provider SSL settings when connecting from production.
- Coordinate migrations and backups. For production, use continuous deployment and run migrations as part of deploy pipeline.
- For shared media (product images), configure `django-storages` + S3 (I can add that next).

---

Troubleshooting
- If `psycopg2` fails to install on Windows, use `psycopg2-binary` in `requirements.txt` (already added).
- If `manage.py migrate` fails due to existing constraints, consider dumping and loading fixtures as described.
- If you see "could not connect" errors, ensure IP allowlist and SSL settings are correct on provider.

---

If you want, I can provision a Railway Postgres instance and provide connection steps and a recommended `.env` content (you'll need to confirm you want me to create an account or that I should provide instructions for you to create it).