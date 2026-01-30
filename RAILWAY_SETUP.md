Railway Postgres Setup for Artisan Project

This guide walks you through provisioning a free Railway Postgres instance and configuring your Django project in ~5 minutes.

STEP 1: Sign up and create Railway project (2 min)
1. Go to https://railway.app/
2. Click "Start a New Project"
3. Sign in with GitHub (recommended) or email
4. Click "Provision Postgres" (or search "PostgreSQL" in plugin list)
5. Railway creates a database and shows the dashboard

STEP 2: Get DATABASE_URL (1 min)
1. In Railway dashboard, open the Postgres plugin
2. Click "Connect" tab
3. Copy the entire URL that starts with postgres://...
4. It looks like:
   postgres://postgres.xxxxxxx_user:xxxxxxxxxxxx@gateway.railway.app:5432/railway
5. Save this temporarily in a text editor

STEP 3: Configure project locally (1 min)
1. In your project root, open `.env` (create from `.env.example` if needed)
2. Replace the DATABASE_URL line with your Railway URL from Step 2:
   DATABASE_URL=postgres://postgres.xxxxxxx_user:xxxxxxxxxxxx@gateway.railway.app:5432/railway
3. Save and close

STEP 4: Install deps and migrate (1 min)
```powershell
# Activate venv if not already
.\.venv\Scripts\Activate.ps1

# Install deps
pip install -r requirements.txt

# Run migrations
python manage.py migrate
python manage.py createsuperuser   # optional, creates admin user
```

STEP 5: Test (1 min)
```powershell
python manage.py runserver 0.0.0.0:8000
```
- Open http://127.0.0.1:8000/
- Create a product via admin or site
- Confirm it persists (add a product, refresh page, product still there)

STEP 6: Team setup (each teammate, 1 min each)
1. Pull latest code from GitHub
2. Ask for the Railway DATABASE_URL (share securely, e.g., team chat pinned message)
3. Create `.env` in project root and set:
   DATABASE_URL=<same URL>
4. Run:
   ```powershell
   pip install -r requirements.txt
   python manage.py migrate
   python manage.py runserver
   ```

STEP 7: Verify shared visibility
- Dev A: Create a product
- Dev B (on different machine, same DATABASE_URL): Refresh product list
  → Product added by Dev A appears ✓

---

Security reminders
- NEVER commit `.env` to Git (already in .gitignore)
- NEVER share DATABASE_URL in public channels (use private chat/email)
- Change DJANGO_SECRET_KEY from default in production

---

Troubleshooting
Q: "could not connect" error
A: Copy DATABASE_URL exactly (including all special chars). Check Railway dashboard shows plugin is "Healthy".

Q: "migrate" fails with permission error
A: Run migrations ONCE. Coordinate with teammates to avoid concurrent runs.

Q: Products not visible to other dev
A: Ensure both devs have same DATABASE_URL in `.env`. Check with:
   echo $env:DATABASE_URL

Q: How to switch back to SQLite temporarily?
A: Remove/comment out DATABASE_URL in `.env`. Django falls back to SQLite.

---

Next steps
1. Provision Railway Postgres now
2. Copy DATABASE_URL to `.env`
3. Run migrations
4. Share DATABASE_URL with team securely
5. All teammates set same DATABASE_URL in `.env` and start server
6. Confirm products are shared (add product on one machine, view on another)
