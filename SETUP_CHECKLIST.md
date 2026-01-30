Quick Checklist: Shared Database Setup

Use this checklist to complete the shared database setup with your team.

--- INITIAL SETUP (One person, ~5 min) ---

[ ] Provision Railway Postgres
    - Go to https://railway.app/
    - Sign in with GitHub
    - Create new project > Provision Postgres
    
[ ] Copy DATABASE_URL from Railway
    - Open Postgres plugin dashboard
    - Click "Connect" tab
    - Copy full URL (starts with postgres://)
    
[ ] Create `.env` in project root
    - Copy `.env.example` to `.env`
    - Replace DATABASE_URL with your Railway URL
    - Set DJANGO_SECRET_KEY to a random string
    
[ ] Install dependencies
    ```powershell
    pip install -r requirements.txt
    ```
    
[ ] Run migrations
    ```powershell
    python manage.py migrate
    python manage.py createsuperuser
    ```
    
[ ] Test locally
    ```powershell
    python manage.py runserver
    ```
    - Create a product
    - Refresh browser (product persists)
    
[ ] Commit code changes to GitHub
    ```powershell
    git add .
    git commit -m "Add shared database configuration"
    git push origin main
    ```
    (Note: .env is NOT committed; it's in .gitignore)

[ ] Share DATABASE_URL with team securely
    - Post in private team chat (e.g., Discord/Slack)
    - OR send via email
    - NOT in public comments or open issues

--- EACH TEAMMATE (Per person, ~2 min) ---

[ ] Pull latest code
    ```powershell
    git pull origin main
    ```

[ ] Create `.env`
    - Copy `.env.example` to `.env`
    - Ask team lead for DATABASE_URL
    - Paste DATABASE_URL into `.env`
    - Set DJANGO_SECRET_KEY to same value (ask team lead)

[ ] Install dependencies
    ```powershell
    .\.venv\Scripts\Activate.ps1   # if using venv
    pip install -r requirements.txt
    ```

[ ] Run migrations
    ```powershell
    python manage.py migrate
    ```

[ ] Start server
    ```powershell
    python manage.py runserver
    ```

[ ] Test shared visibility
    ```
    Ask team lead to add a product
    Refresh your product list
    Product should appear (same DATABASE_URL means same DB)
    ```

--- VERIFICATION (All team members) ---

[ ] Test 1: Add product on Machine A
    - Create a product (via site or admin)
    - Note down product name
    
[ ] Test 2: View product on Machine B
    - Login to different machine
    - Go to products list
    - Product from A should appear
    
[ ] Test 3: Verify database connection
    ```powershell
    python - <<'PY'
    import os, psycopg2
    url = os.environ.get('DATABASE_URL')
    if url:
        conn = psycopg2.connect(url)
        print('✓ Connected to:', conn.get_dsn_parameters()['dbname'])
        conn.close()
    else:
        print('✗ DATABASE_URL not set')
    PY
    ```

--- DONE ---

Once all tests pass, your team can:
✓ All see the same products across machines
✓ Add/edit products that appear for everyone
✓ No local database conflicts
✓ Ready for production deployment

If issues arise, check:
1. DATABASE_URL is set in `.env` (and same for all devs)
2. Railway Postgres plugin shows "Healthy" status
3. Migrations have run on all machines (`python manage.py migrate`)
4. Network access is not blocked (check Railway IP allowlist if needed)
